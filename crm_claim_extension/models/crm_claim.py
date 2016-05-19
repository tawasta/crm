# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import tools, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
logger = logging.getLogger(__name__)


class CrmClaim(models.Model):

    # 1. Private attributes
    _inherit = 'crm.claim'

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

    # 5. Constraints and onchanges
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
    def create(self, vals):
        if not vals.get('claim_number'):
            vals['claim_number'] = self.env['ir.sequence'].get('crm.claim')
        return super(CrmClaim, self).create(vals)

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
            logger.debug("Setting claim number for #%s", claim.claim_number)

    @api.multi
    def message_post(self, **kwargs):
        res = super(CrmClaim, self).message_post(**kwargs)

        if 'type' in kwargs and kwargs['type'] == 'comment' and self.email_cc:
            # Make a message about cc-recipients

            msg = _("Previous message was sent to '%s' as a copy.") % self.email_cc
            self.message_post(body=msg)

        return res
