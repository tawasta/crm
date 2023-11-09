from odoo import fields, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    distributor_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Distributor Partner",
        domain=[("is_distributor_partner", "=", True)],
        help="""The distributor partner responsible for this Lead/Opportunity""",
    )
