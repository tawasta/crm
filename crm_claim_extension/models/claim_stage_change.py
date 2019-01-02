# -*- coding: utf-8 -*-

# 1. Standard library imports:
from datetime import datetime

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ClaimStageChange(models.Model):

    # 1. Private attributes
    _name = 'crm.claim.stage.change'
    _rec_name = 'stage'
    _order = 'create_date DESC'

    # 2. Fields declaration
    stage = fields.Many2one('crm.claim.stage', 'New stage')
    claim_id = fields.Many2one('crm.claim', 'Claim')
    hours = fields.Float("Hours", compute="_compute_hours")
    claim_partner_id = fields.Many2one(related='claim_id.partner_id', string='Claim partner', store=True)
    claim_date = fields.Datetime(related='claim_id.date', string='Claim received', store=True)
    claim_date_closed = fields.Datetime(related='claim_id.date_closed', string='Claim closed')
    claim_message_last_post = fields.Datetime(related='claim_id.message_last_post', string='Claim last message')
    claim_sla = fields.Selection(
        [   
            ('0', '-'),
            ('1', 'Level 1'),
            ('2', 'Level 2'),
            ('3', 'Level 3'),
            ('4', 'Level 4'),
        ],
        string='Claim SLA',
        related='claim_id.sla',
   )
    claim_company_id = fields.Many2one(related='claim_id.company_id', string='Claim company')
    
    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.multi
    def _compute_hours(self):
        all_records = self.sorted(key=lambda stage_change: stage_change.create_date, reverse=True)
        format = '%Y-%m-%d %H:%M:%S'

        previous_record = False
        for record in all_records:
            this_date = datetime.strptime(record.create_date, format)

            if not previous_record:
                previous_record = record
                previous_date = datetime.now()
            else:
                previous_date = datetime.strptime(previous_record.create_date, format)

            difference = previous_date-this_date

            record.hours = difference.total_seconds() / 3600

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
