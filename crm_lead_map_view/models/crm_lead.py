from odoo import api, fields, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    customer_latitude = fields.Float(
        string="Latitude", related="partner_id.partner_latitude"
    )
    customer_longitude = fields.Float(
        string="Longitude", related="partner_id.partner_longitude"
    )
