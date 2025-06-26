from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    instrument_need = fields.Text()
