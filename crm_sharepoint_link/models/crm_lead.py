from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sharepoint_link = fields.Char(string="SharePoint / Customer")
