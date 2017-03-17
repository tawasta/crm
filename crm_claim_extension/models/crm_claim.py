# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import tools, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
_logger = logging.getLogger(__name__)

class CrmClaim(models.Model):

    # 1. Private attributes
    _inherit = 'crm.claim'
    _order = "write_date DESC"

    # 2. Fields declaration
    claim_number = fields.Char('Claim number')
    company_id = fields.Many2one('res.company', string='Company', required=True)
    stage = fields.Char('Claim Stage', function='_get_stage_string')
    reply_to = fields.Char('Reply to', size=128, help="Provide reply to address for message thread.")
    sla = fields.Selection(
        [
            ('0', '-'),
            ('1', 'Taso 1'),
            ('2', 'Taso 2'),
            ('3', 'Taso 3'),
            ('4', 'Taso 4'),
        ],
        'Service level',
        select=True
    )
    email_to = fields.Char('Email to', help='Email recipient')
    email_cc = fields.Char('Email CC', help='Carbon copy message recipients')
    email_from_readonly = fields.Char('Recipient email', readonly=True)
    date_start = fields.Datetime('Start date')
    date_waiting = fields.Datetime('Waiting date')
    date_settled = fields.Datetime('Settled date')
    date_rejected = fields.Datetime('Rejected date')
    attachment_ids = fields.Many2many('ir.attachment',  string='Attachments')
    stage_change_ids = fields.One2many('crm.claim.stage.change', 'claim_id', string='Stage changes', readonly=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _get_stage_string(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        result = {}

        for rec in records:
            result[rec.id] = rec.stage_id.name

        return result

    @api.model
    def _get_reply_to(self):
        claim_reply = self.env['crm_claim.reply'].search([('company_id', '=', self.company_id.id)], limit=1)

        if claim_reply:
            res = claim_reply.reply_to
        else:
            res = self.reply_to

        return res

    # 5. Constraints and onchanges
    @api.onchange('partner_id')
    @api.multi
    def onchange_partner_id(self):
        for record in self:
            record.email_from_readonly = record.partner_id.email
            record.email_from = record.partner_id.email

    @api.onchange('email_from')
    def onchange_email(self):
        # Validates email

        if self.email_from:
            valid_email = tools.single_email_re.match(self.email_from)

            result = dict()

            if not valid_email:
                result['warning'] = {
                    'title': 'Warning!',
                    'message': 'The email address "%s" is not valid.' % self.email_from
                }

            self.email_from_readonly = self.email_from

            return result

    # 6. CRUD methods
    @api.model
    def create(self, values):
        if not values.get('claim_number'):
            values['claim_number'] = self.env['ir.sequence'].get('crm.claim')

        res = super(CrmClaim, self).create(values)

        res.message_subscribe([res.partner_id.id])

        return res

    @api.multi
    def write(self, values):
        claim_stage_model = self.env['crm.claim.stage'].search([('new_reply_stage', '=', True)], limit=1)

        for record in self:
            if values.get('message_last_post'):
                stage_id = record.stage_id.id

                # Check if a closed ticket gets a new message.
                # If so, mark the ticket as new
                if stage_id in [3, 4]:
                    values['stage_id'] = claim_stage_model.id
                    msg_body = _("Re-opening claim due to a new message.")
                    record.message_post(body=msg_body)

        return super(CrmClaim, self).write(values)

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default['claim_number'] = self.env['ir.sequence'].get('crm.claim')
        return super(CrmClaim, self).copy(default)

    # 7. Action methods

    # 8. Business methods
    @api.model
    def _init_claim_numbers(self):
        # When the module is installed, fetch all claims without a number and assign them one

        claims = self.search([('claim_number', '=', False)])

        for claim in claims:
            claim.claim_number = self.env['ir.sequence'].get('crm.claim')
            _logger.debug("Setting claim number for #%s", claim.claim_number)

    @api.multi
    def message_post(self, **kwargs):
        res = super(CrmClaim, self).message_post(**kwargs)

        if 'type' in kwargs and kwargs['type'] == 'comment' and self.email_cc:
            # Make a message about cc-recipients

            msg = _("Previous message was sent to '%s' as a copy.") % self.email_cc
            self.message_post(body=msg)

        return res

    @api.model
    def message_new(self, msg, custom_values):

        result = super(CrmClaim, self).message_new(msg=msg, custom_values=custom_values)

        return result

        msg = False
        if 'msg' in kwargs:
            msg = kwargs['msg']

        email_cc = msg.get('to')

        if msg.get('cc'):
            email_cc = email_cc + "," + msg.get('cc')

        defaults = {
            'email_cc': email_cc
        }

        return result

    @api.model
    def _fetch_partner(self, vals):
        email_from = vals.get('email_from')
        name_regex = re.compile("^[^<]+")
        email_regex = re.compile("[\w\.-]+@[\w\.-]+")

        _logger.info("Fetching partner for email %s", email_from)

        try:
            name = name_regex.findall(email_from)[0]
            email = email_regex.findall(email_from)[0]
        except IndexError:
            # The email has no name information
            name = email_from
            email = email_from

        email = re.sub(r'[<>]', "", email)
        name = re.sub(r'["]', "", name)

        partner_object = self.env['res.partner']
        existing_partner = partner_object.search([('email', 'ilike', email)], limit=1)
        if existing_partner:
            partner_id = existing_partner.id
        else:
            _logger.info("No partner found. Creating %s", name)

            partner_vals = dict()
            partner_vals['name'] = name
            partner_vals['email'] = email
            partner_vals['claim_autogenerated'] = True
            partner_id = partner_object.create(partner_vals)

        return partner_id

    @api.model
    def _claim_send_autoreply(self, claim_id):
        # Checks if a partner is applicable for sending a mail
        claim = self.browse([claim_id])
        partner = claim.partner_id

        # All claims for the partner within the last 15 minutes
        timestamp_search = datetime.strftime(datetime.now() - relativedelta(minutes=15), '%Y-%m-%d %H:%M:%S')
        claims_count = self.sudo().search([('partner_id', '=', partner.id), ('create_date', '>=', timestamp_search)], count=True)

        if claims_count > 3:
            _logger.warn("This partner has more than three new claims in last 15 minutes. Autoreply is disabled")
            msg_body = _("<strong>Autoreply was not sent.</strong>") + "<br/>"
            msg_body += _('This partner has more than three claims in the last 15 minutes.') + "<br/>"
            msg_body += _('Sending autoreply is disabled for this partner to prevent an autoreply-loop.') + "<br/>"
            msg_body += _('Please wait a while before creating new ticket, or mark some tickets as started.') + "<br/>"
            claim.message_post(body=msg_body)

            return False

        #self._claim_created_mail(claim_id=claim_id)
        return True

    @api.model
    def get_claim_received_vals(self, values):
        # Creates and sends a "claim created" mail to the partner
        mail_message = self.env['mail.message']

        subject = _("Claim") + " #" + str(self.claim_number) + ": " + self.name
        email = self._get_reply_to()

        if not self.description:
            self.description = ''

        body = values['body'] or ''

        #description = self.description.replace('\n', '<br />').encode('ascii', 'ignore')
        #description = self.description

        # values['body'] = "<p style='font-weight: bold;'>" + subject + "</p>"
        values['body'] = "<p><span style='font-weight: bold;'>" + _("Claim has been received") + ":</span></p>"
        values['body'] += "<p><div dir='ltr' style='margin-left: 2em;'>" + str(body) + "</div></p>"

        values['author_id'] = False
        values['record_name'] = subject
        values['subject'] = subject
        #values['email_from'] = email
        values['reply_to'] = email

        return values
