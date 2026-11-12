from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    subscription_invoice_ref = fields.Char(
        string="Subscription Invoice Reference",
        help="Customer reference of the quotation created from this lead, "
        "passed on to its subscription's invoices",
    )

    def _prepare_opportunity_quotation_context(self):
        quotation_context = super()._prepare_opportunity_quotation_context()
        if self.subscription_invoice_ref:
            quotation_context[
                "default_client_order_ref"
            ] = self.subscription_invoice_ref
        return quotation_context
