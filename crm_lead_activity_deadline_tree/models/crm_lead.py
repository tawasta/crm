from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = "crm.lead"

    activity_date_deadline_stored = fields.Date(
        string="Next Activity Deadline (Stored)",
        compute="_compute_deadline",
        store=True,
    )

    @api.depends("activity_ids.date_deadline", "activity_ids.date_done", "activity_ids")
    def _compute_deadline(self):
        for lead in self:
            dates = lead.activity_ids.filtered(lambda a: not a.date_done).mapped(
                "date_deadline"
            )
            lead.activity_date_deadline_stored = min(dates) if dates else False
