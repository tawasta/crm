# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    lead_id = fields.Many2one('crm.lead', "Related case")