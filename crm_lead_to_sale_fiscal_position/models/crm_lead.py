import logging

from odoo import models

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _prepare_opportunity_quotation_context(self):
        # Add fiscal position to default values when SO form opens
        self.ensure_one()

        res = super()._prepare_opportunity_quotation_context()

        if self.partner_id:
            fiscal_position_obj = self.env["account.fiscal.position"].with_company(
                self.env.user.company_id
            )

            res[
                "default_fiscal_position_id"
            ] = fiscal_position_obj._get_fiscal_position(self.partner_id).id

        return res
