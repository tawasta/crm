# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class CrmMakeSale(models.TransientModel):
    _inherit = "crm.make.sale"
    
    @api.multi
    def makeOrder(self):
        _logger.warn(self)
        
        res = super(CrmMakeSale, self).makeOrder()
        
        _logger.warn(res)
        
        return res