# -*- coding: utf-8 -*-
from openerp import models, api, fields

import logging
_logger = logging.getLogger(__name__)

class CrmClaimReport(models.Model):
    
    _inherit = 'crm.claim.report'
    
    def _select(self):
        new_fields = ""
        new_fields += ""
        
        return super(CrmClaimReport, self)._select() + new_fields
    
    def _from(self):
        new_fields = ""
        new_fields += ""
        
        return super(CrmClaimReport, self)._from() + new_fields
    
    def _group_by(self):
        new_fields = ""
        new_fields += ""
        
        return super(CrmClaimReport, self)._group_by() + new_fields