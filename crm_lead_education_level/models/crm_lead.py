from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    education_level_ids = fields.Many2many(
        comodel_name="res.education.level",
        string="Education Levels",
    )
    # Same name and type as on res.partner, so the value can be copied to
    # the partner with crm_lead_to_partner_field_mapping
    other_education_or_degree = fields.Char("Other Education or Degree")
