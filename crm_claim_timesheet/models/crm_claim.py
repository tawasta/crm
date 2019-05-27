
# 1. Standard library imports:
from datetime import datetime

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class CrmClaim(models.Model):
    
    # 1. Private attributes
    _inherit = 'crm.claim'

    # 2. Fields declaration
    timesheet_records = fields.One2many('hr.analytic.timesheet', 'crm_claim', 'Work done')
    suggested_analytic_account = fields.Many2one(
        'account.analytic.account',
        'Suggested analytic account',
        compute='compute_suggested_analytic_account'
    )
    suggested_task = fields.Many2one('project.task', 'Suggested task', compute='compute_suggested_task')
    suggested_time = fields.Float('Suggested time', compute='compute_suggested_time')
    suggested_message = fields.Char('Suggested message', compute='compute_suggested_message')

    time_recorded = fields.Float('Time recorded', compute='compute_time_recorded', store=True)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.multi
    def compute_suggested_analytic_account(self):
        analytic_account_model = self.env['account.analytic.account']
        for record in self:
            account_name = "Tuki %s" % datetime.now().year  # TODO: claim conf for smarter search

            record.suggested_analytic_account = analytic_account_model.search([
                ('name', 'ilike', account_name),
                ('company_id', '=', record.company_id.id)
            ], limit=1)

    @api.multi
    def compute_suggested_task(self):
        task_model = self.env['project.task']
        for record in self:
            record.suggested_task = task_model.search([
                ('project_id.analytic_account_id', '=', record.suggested_analytic_account.id),
                ('stage_id.closed', '=', False),
                ('stage_id', '!=', 1),
            ], limit=1)

    @api.multi
    def compute_suggested_time(self):
        for record in self:
            if hasattr(record, 'stage_change_ids'):
                # Sort the record set so we can be sure it will suggest the latest stage change
                stage_changes = record.stage_change_ids.sorted(key=lambda r: r.create_date)

                if len(stage_changes) < 2:
                    continue

                record.suggested_time = round(stage_changes[1].hours, 2)

    @api.multi
    def compute_suggested_message(self):
        for record in self:
            partner = record.partner_id.parent_id.name or record.partner_id.name
            msg = "%s (#%s): " % (partner, record.claim_number)

            record.suggested_message = msg

    @api.multi
    @api.depends('timesheet_records')
    def compute_time_recorded(self):
        for record in self:
            time_recorded = 0.00
            for time in record.timesheet_records:
                time_recorded += time.unit_amount

            record.time_recorded = time_recorded

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
