# -*- coding: utf-8 -*-
from openerp import models, api

import logging
_logger = logging.getLogger(__name__)


class CrmMakeSale(models.TransientModel):
    _inherit = "crm.make.sale"

    @api.multi
    def makeOrder(self):
        res = super(CrmMakeSale, self).makeOrder()

        if res and res['res_model'] == 'sale.order':
            sale_order = self.env['sale.order'].browse(res['res_id'])
            lead = self.env['crm.lead'].browse(self._context['active_id'])

            # Create references
            sale_order.lead = lead.id
            lead.sale_order = sale_order.id

            # Move the description
            sale_order.description = lead.description

            # Move the header
            sale_order.header_text = lead.name

            # Fix the partners, if necessary
            sale_order.onchange_partner()

        return res
