import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MailActivitySchedule(models.TransientModel):
    _inherit = "mail.activity.schedule"

    high_priority = fields.Boolean()

    def _action_schedule_activities(self):
        """
        Add the high priority field contents to the scheduled activities.

        Note that the core method does not facilitate inheriting, so it is simply
        overridden with one extra field added in.
        """

        return self._get_applied_on_records().activity_schedule(
            activity_type_id=self.activity_type_id.id,
            automated=False,
            summary=self.summary,
            note=self.note,
            user_id=self.activity_user_id.id,
            date_deadline=self.date_deadline,
            high_priority=self.high_priority,
        )
