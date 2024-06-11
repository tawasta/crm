import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):

    _inherit = "crm.lead"

    def write(self, vals):
        """
        If opportunity is moved to a stage where 'Is Lost Stage' = true, then also
        set its closing date, archive it, and mark its probability to 0%
        """
        res = super().write(vals)

        if vals.get("stage_id"):

            lost_stage_ids = self.env["crm.stage"].search([("is_lost", "=", True)])

            if vals.get("stage_id") in [s.id for s in lost_stage_ids]:
                self.date_closed = fields.Datetime.now()
                self.action_archive()

        return res

    def action_set_lost(self, **additional_values):
        """
        When Set as Lost is clicked, move the opportunity to the
        stage that has been configured with Is Lost Stage?. Probability
        needs to be set at this step to 0, or its recalculation will trigger.
        """

        is_lost_stage = self.env["crm.stage"].search([("is_lost", "=", True)], limit=1)

        if len(is_lost_stage) > 0:
            additional_values["stage_id"] = is_lost_stage[0].id
            additional_values["probability"] = 0.00

        return super().action_set_lost(**additional_values)
