from odoo import fields, models


class CrmStage(models.Model):
    _inherit = "crm.stage"

    customer_replied = fields.Boolean(
        string="Customer Replied Stage",
        help=(
            "When a new incoming customer email is posted on a CRM lead, "
            "move the lead to this stage."
        ),
    )
