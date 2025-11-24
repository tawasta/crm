from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    sharepoint_link = fields.Char(string="SharePoint / Customer")
