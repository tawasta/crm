import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CrmStage(models.Model):

    _inherit = "crm.stage"

    is_lost = fields.Boolean(
        string="Is Lost Stage?",
        help="Opportunities moved to this stage will be archived and have their "
        "Days to Close value calculated.",
    )

    @api.model
    def create(self, values):
        res = super().create(values)
        lost_stages = self.env["crm.stage"].search([("is_lost", "=", True)])

        if len(lost_stages) > 1:
            lost_stage_names = [s.name for s in lost_stages]
            raise ValidationError(
                _(
                    "Only a single Stage is allowed to have the 'Is Lost Stage?' "
                    " attribute. The following stages have it: %s ",
                    ", ".join(lost_stage_names),
                )
            )

        return res

    def write(self, vals):

        res = super().write(vals)
        lost_stages = self.env["crm.stage"].search([("is_lost", "=", True)])

        if len(lost_stages) > 1:
            lost_stage_names = [s.name for s in lost_stages]
            raise ValidationError(
                _(
                    "Only a single Stage is allowed to have the 'Is Lost Stage?' "
                    " attribute. The following stages have it: %s ",
                    ", ".join(lost_stage_names),
                )
            )

        return res
