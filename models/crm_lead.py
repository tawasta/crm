# -*- coding: utf-8 -*-
from openerp import models, fields


class CrmLead(models.Model):
    _inherit = "crm.lead"

    sale_order = fields.Many2one('sale.order', "Related sale")
    sale_order_state = fields.Char('Order state', compute='_get_sale_order_state')

    def _get_sale_order_state(self):
        self.sale_order_state = self.sale_order.state