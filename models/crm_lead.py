# -*- coding: utf-8 -*-
from openerp import models, fields, api


class CrmLead(models.Model):
    _inherit = "crm.lead"

    sale_order = fields.Many2one('sale.order', "Related sale")
    sale_order_state = fields.Char('Order state', compute='_get_sale_order_state')

    @api.depends('sale_order')
    @api.one
    def _get_sale_order_state(self):
        if self.sale_order.state:
            states = dict(self.sale_order.fields_get(['state'])['state']['selection'])
            self.sale_order_state = states[self.sale_order.state]
