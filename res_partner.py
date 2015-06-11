# -*- coding: utf-8 -*-
from openerp import models, api, fields

class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    show_all = fields.Boolean('Show all fields')
    
    # This field is only a helper for "is company"
    personal_customer = fields.Boolean('Personal Customer', domain={('invisible','=',True)}, help="A customer that's not a company")
    
    @api.onchange('personal_customer')
    def personal_customer_onchange(self):
        if self.personal_customer:
            self.is_company = False
        else:
            self.is_company = True
            
    @api.onchange('is_company')
    def is_company_onchange(self):
        if self.is_company:
            self.personal_customer = False
        else:
            self.personal_customer = True