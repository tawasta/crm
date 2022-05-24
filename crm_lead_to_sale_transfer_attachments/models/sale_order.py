from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.model
    def create(self, values):
        """
        If the sale order creation was triggered from an opportunity,
        duplicate the opportunity's attachments to the new SO
        """
        res = super(SaleOrder, self).create(values)

        if (
            self._context.get("default_opportunity_id", False)
            and self._context.get("active_model", False) == "crm.lead"
        ):

            args = [
                ("res_model", "=", "crm.lead"),
                ("res_id", "=", self._context["default_opportunity_id"]),
            ]
            lead_attachments = self.env["ir.attachment"].search(args)

            for lead_attachment in lead_attachments:
                sale_attachment = lead_attachment.copy()
                sale_attachment.write({"res_id": res.id, "res_model": "sale.order"})

        return res
