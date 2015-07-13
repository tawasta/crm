# -*- coding: utf-8 -*-
from openerp import models, fields


class CrmLead(models.Model):
    _inherit = "crm.lead"

    sale_order = fields.Many2one('sale.order', "Related sale")
