from odoo import api, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["type"] = "opportunity"
        return super().create(vals_list)
