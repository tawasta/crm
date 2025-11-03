import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    high_priority_activities = fields.Boolean(
        compute="_compute_high_priority_activities", store=True, default=False
    )

    @api.depends("activity_ids", "activity_ids.high_priority")
    def _compute_high_priority_activities(self):
        """
        Mark the lead as having high priority activities, for
        searching/filtering
        """
        for record in self:
            record.high_priority_activities = any(
                activity.high_priority for activity in record.activity_ids
            )
