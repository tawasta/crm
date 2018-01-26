# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import tools, _
from openerp import SUPERUSER_ID

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
_logger = logging.getLogger(__name__)


class CrmClaim(models.Model):

    # 1. Private attributes
    _inherit = 'crm.claim'
    _order = "stage_id ASC, date DESC"

    _sql_constraints = [
        ('claim_number', 'unique(claim_number)', _('This claim number is already in use.'))
    ]

    # 2. Fields declaration
    claim_number = fields.Char('Claim number')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self._default_get_company(),
    )
    stage = fields.Char('Claim Stage', compute='compute_stage_string')
    stage_id = fields.Many2one(default=1)
    reply_to = fields.Char(
        string='Reply to',
        size=128,
        default=lambda self: self._get_reply_to(),
        help="Provide reply to address for message thread."
    )
    sla = fields.Selection(
        [
            ('0', '-'),
            ('1', 'Level 1'),
            ('2', 'Level 2'),
            ('3', 'Level 3'),
            ('4', 'Level 4'),
        ],
        'Service level',
        select=True,
        default='1',
    )
    email_to = fields.Char('Email to', help='Email recipient')
    email_cc = fields.Char('Email CC', help='Carbon copy message recipients')
    email_from_readonly = fields.Char('Recipient email', readonly=True)

    # Change the description type
    description = fields.Html('Description')

    # Dates for logging
    date_start = fields.Datetime('Start date')
    date_waiting = fields.Datetime('Waiting date')
    date_settled = fields.Datetime('Settled date')
    date_rejected = fields.Datetime('Rejected date')

    attachment_ids = fields.Many2many('ir.attachment',  string='Attachments')
    stage_change_ids = fields.One2many('crm.claim.stage.change', 'claim_id', string='Stage changes', readonly=True)

    time_open = fields.Float('Time open', compute='compute_time_open', store=True)

    # 3. Default methods
    def _default_get_company(self):
        if self.company_id:
            company_id = self.company_id.id
        else:
            company_id = self.env['res.users'].browse([self._uid]).company_id.id

        return company_id

    def _default_get_reply_settings(self, company_id=None):
        if not company_id:
            company_id = self._default_get_company()

        reply_settings = self.env['crm_claim.reply'].search([
            ('company_id', '=', company_id)
        ], limit=1)

        return reply_settings

    def _default_get_reply_header(self, company_id=None):
        res = False
        reply_settings = self._default_get_reply_settings(company_id)

        if reply_settings:
            res = reply_settings.header

        return res

    def _default_get_reply_footer(self, company_id=None,):
        res = False
        reply_settings = self._default_get_reply_settings(company_id)

        if reply_settings:
            res = reply_settings.footer

        return res

    def _default_get_reply_aliases(self, company_id=None):
        res = False
        reply_settings = self._default_get_reply_settings(company_id)

        if reply_settings:
            res = reply_settings.reply_alias_ids

        return res

    def _get_exclude_list(self, company_id=None):
        mail_ids = self._default_get_reply_aliases(company_id)

        res = []

        for mail_id in mail_ids:
            res.append(mail_id.name)

        return res

    # 4. Compute and search fields, in the same order that fields declaration
    @api.multi
    def compute_stage_string(self):
        for record in self:
            record.stage = record.with_context(lang=False).stage_id.name

    @api.model
    def _get_reply_to(self, company_id=None):
        if not company_id:
            company_id = self._default_get_company()

        claim_reply = self.env['crm_claim.reply'].search([
            ('company_id', '=', company_id),
            ('reply_to', '!=', False),
        ], limit=1)

        if claim_reply:
            res = claim_reply.reply_to
        else:
            res = self.reply_to

        return res

    @api.multi
    @api.depends('stage_change_ids')
    def compute_time_open(self):
        for record in self:
            # Skip this if there are less than two stage changes
            if len(record.stage_change_ids) < 2:
                continue

            stage_changes = record.stage_change_ids.sorted(key=lambda r: r.create_date, reverse=True)
            time_open = 0.00

            for stage_change in stage_changes:
                # Don't calculate closed stage changes
                if stage_change.stage.closed:
                    continue

                time_open += stage_change.hours

            record.time_open = time_open

    # 5. Constraints and onchanges
    @api.onchange('partner_id')
    @api.depends('partner_id')
    @api.multi
    def onchange_partner_id_update_email(self):
        for record in self:
            record.email_from = record.partner_id.email
            record.email_from_readonly = record.partner_id.email

    @api.onchange('email_from')
    def onchange_email_validate_email(self):
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
        # Set claim number
        if not values.get('claim_number'):
            values['claim_number'] = self.env['ir.sequence'].get('crm.claim')

            if values.get('email_from'):
                values['email_from_readonly'] = values.get('email_from')

        # If partner doesn't exist, we'll need to create one
        if not values.get('partner_id'):
            values['partner_id'] = self._fetch_partner(values)

        # Get the reply-to address based on the fetchmail server instance owner
        if self._context.get('fetchmail_server_id'):
            fetchmail_server = self.env['fetchmail.server'].browse([self._context.get('fetchmail_server_id')])

            if fetchmail_server:
                company_id = fetchmail_server.company_id.id
                reply_to = self._get_reply_to(company_id=company_id)
                values['company_id'] = company_id
                values['reply_to'] = reply_to
                values['user_id'] = False

        claim = super(CrmClaim, self).create(values)

        # Remove the helpdesk email and its aliases from cc emails
        if claim.email_cc:
            email_regex = re.compile("[\w\.-]+@[\w\.-]+")
            email_list = email_regex.findall(claim.email_cc)

            try:
                email_raw = email_regex.findall(claim._get_reply_to())[0]
                email_raw = re.sub(r'[<>]', "", email_raw)

                reply_to = email_raw

                exclude_list = self._get_exclude_list(claim.company_id.id) + [reply_to]

                for exclude in exclude_list:
                    match = [s for s in email_list if exclude in s]

                    if match:
                        email_list.pop(email_list.index(match[0]))

                    match = False

                _logger.info("Using email CCs: %s", email_list)
                email_cc = ','.join(email_list)
                self.email_cc = email_cc

            except Exception, e:
                _logger.error('Could not set email CCs: %s', e)

        if claim.create_uid.id != SUPERUSER_ID and claim.company_id:
            # Create a "claim received" message
            message = claim.message_post(
                subject=claim.name,
                body=claim.description,
                type='comment',
                subtype='mt_comment'
            )

        claim.message_subscribe([claim.partner_id.id])

        # Unsubscribe the company from followers
        claim.message_unsubscribe([claim.company_id.partner_id.id])

        return claim

    @api.multi
    def write(self, values):
        claim_stage_model = self.env['crm.claim.stage']
        claim_state_new_reply = claim_stage_model.search([('new_reply_stage', '=', True)], limit=1)

        for record in self:
            if values.get('message_last_post'):
                # Check if a closed or waiting ticket gets a new message
                # and reopen it if necessary
                if record.stage_id.closed or record.stage_id.waiting:
                    values['stage_id'] = claim_state_new_reply.id
                    msg_body = _("Re-opening claim due to a new message.")
                    record.message_post(body=msg_body)

        # When a claim stage changes, save the date
        # TODO: make this modular (not bound to ids)
        if values.get('stage_id'):
            stage_id = values.get('stage_id')

            if stage_id:
                values['stage_change_ids'] = [(0, _, {'stage': stage_id})]

            if stage_id == 2:
                # In progress
                values['date_start'] = datetime.now().replace(microsecond=0)
                if not self.user_id:
                    values['user_id'] = self._uid
            if stage_id == 3:
                # Settled
                values['date_settled'] = datetime.now().replace(microsecond=0)
            if stage_id == 4:
                # Rejected
                values['date_rejected'] = datetime.now().replace(microsecond=0)
            if stage_id == 5:
                # Waiting
                values['date_waiting'] = datetime.now().replace(microsecond=0)

        if values.get('partner_id'):
            # Partner is being changed. Update followers

            # Remove current partner
            self.message_unsubscribe([self.partner_id.id])
            # Set the new partner as follower
            self.message_subscribe([values.get('partner_id')])

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

        if 'type' in kwargs and kwargs['type'] == 'comment' \
                and 'subtype' in kwargs and kwargs['subtype'] == 'mail.mt_comment' \
                and self.email_cc:
            # Make a message about cc-recipients

            msg = _("Previous message was sent to '%s' as a copy.") % self.email_cc
            self.sudo().message_post(body=msg)

        return res

    @api.model
    def _fetch_partner(self, vals):
        email_from = vals.get('email_from')
        name_regex = re.compile("^[^<]+")
        email_regex = re.compile("[\w\.-]+@[\w\.-]+")

        try:
            name = name_regex.findall(email_from)[0]
            email = email_regex.findall(email_from)[0].lower()
        except IndexError:
            # The email has no name information
            name = email_from
            email = email_from

        email = re.sub(r'[<>]', "", email).lower()
        name = re.sub(r'["]', "", name)

        _logger.info("Fetching partner for email %s", email)

        partner_object = self.env['res.partner']
        existing_partner = partner_object.search([('email', '=ilike', email)], limit=1)
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

        # self._claim_created_mail(claim_id=claim_id)
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

        values['body'] = "<p><span style='font-weight: bold;'>" + _("Claim has been received") + ":</span></p>"
        values['body'] += "<p><div dir='ltr' style='margin-left: 2em;'>" + str(body) + "</div></p>"

        values['author_id'] = SUPERUSER_ID
        values['record_name'] = subject
        values['subject'] = subject
        values['reply_to'] = email

        return values

    @api.model
    def message_new(self, msg, custom_values=None):
        # Overwrites the plain text description with html description (the field type has been changed)

        if not custom_values:
            custom_values = dict()

        custom_values['description'] = msg.get('body') if msg.get('body') else ''
        res = super(CrmClaim, self).message_new(msg=msg, custom_values=custom_values)

        return res
