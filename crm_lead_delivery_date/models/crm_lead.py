from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    delivery_date = fields.Date(
        store=True,
        copy=True,
        help="Estimated delivery date of first deliverable.",
    )
