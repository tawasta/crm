# -*- coding: utf-8 -*-
from openerp import models, api, fields

class CrmLead(models.Model):
    
    _inherit = 'crm.lead'
    
    show_all = fields.Boolean('Show all fields')
    
    LEAD_FIELDS = {
        'name': 'partner_name',
        'street': 'street', 
        'city': 'city', 
        'zip': 'zip', 
        'state_id': 'state_id', 
        'country_id': 'country_id',
        #'email': 'email_from', 
        #'phone': 'phone', 
        #'mobile': 'mobile', 
        #'fax': 'fax',
        #'function': 'function'
        #'title': 'title', 
    }
    
    @api.one
    @api.onchange('partner_id')
    def partner_id_onchange(self):        
        def value_or_id(val):
            return val if isinstance(val, (bool, int, long, float, basestring)) else val.id
        
        values = dict((value, value_or_id(self.partner_id[key])) for key, value in self.LEAD_FIELDS.iteritems())

        print values

        for key, value in values.iteritems():
            setattr(self, key, value)