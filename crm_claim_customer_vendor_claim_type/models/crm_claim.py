from odoo import fields, models


class CrmClaim(models.Model):

    _inherit = "crm.claim"

    claim_type = fields.Selection(
        selection=[
            ("customer", "Customer"),
            ("vendor", "Vendor"),
        ],
        string="Claim Type",
        store=True,
        copy=False,
    )
