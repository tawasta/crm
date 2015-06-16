# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class CrmMakeSale(models.TransientModel):
    _inherit = "crm.make.sale"
    
    @api.multi
    def makeOrder(self):
        res = super(CrmMakeSale, self).makeOrder()
        
        if res['res_model'] == 'sale.order':
            sale_order = self.env['sale.order'].browse( res['res_id'] )
            lead = self.env['sale.order'].browse(self._context['active_id'])
            
            sale_order.lead_id = lead.id
            lead.sale_order_id = sale_order.id
        
        return res