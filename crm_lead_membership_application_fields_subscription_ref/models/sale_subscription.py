from odoo import api, models


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    @api.model_create_multi
    def create(self, vals_list):
        # subscription_oca's create_subscription() has no hook for the values,
        # so add the order's customer reference here
        self._add_order_invoice_ref(vals_list)
        return super().create(vals_list)

    @api.model
    def _add_order_invoice_ref(self, vals_list):
        """Use the origin sale order's customer reference, unless the
        subscription already gets a reference"""
        sale_order_obj = self.env["sale.order"]
        for vals in vals_list:
            if vals.get("invoice_ref") or not vals.get("sale_order_id"):
                continue
            order = sale_order_obj.browse(vals["sale_order_id"])
            if order.client_order_ref:
                vals["invoice_ref"] = order.client_order_ref
