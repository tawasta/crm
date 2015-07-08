# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    sale_order_id = fields.Many2one('sale.order', "Related sale")
