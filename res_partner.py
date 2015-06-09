# -*- coding: utf-8 -*-
from openerp import models, api, fields

class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    show_all = fields.Boolean('Show all fields')
    
    # This field is only a helper for "is company"
    retail_customer = fields.Boolean('Retail Customer')
    
    @api.onchange('retail_customer')
    def retail_customer_onchange(self):
        if self.retail_customer:
            self.is_company = False
        else:
            self.is_company = True
            
    @api.onchange('is_company')
    def is_company_onchange(self):
        if self.is_company:
            self.retail_customer = False
        else:
            self.retail_customer = True