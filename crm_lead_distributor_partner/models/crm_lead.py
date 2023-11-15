from odoo import fields, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    distributor_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Sales Partner",
        domain=[("is_distributor_partner", "=", True)],
        help="""The Sales Partner responsible for this Lead/Opportunity""",
    )
