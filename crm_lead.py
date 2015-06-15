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
            
    @api.multi
    @api.depends('action', 'partner_id')
    def handle_partner_assignation(self, action, context):                     
        partner_ids = {}
        
        for lead in self:
            if lead.partner_id and not lead.contact_name:
                partner_ids[lead.id] = lead.partner_id.id
                continue
            
            if lead.partner_id and lead.contact_name:
                partner_id = self._create_lead_partner(lead)
                
            if not lead.partner_id and action == 'create':
                partner_id = self._create_lead_partner(lead)
                self.env.res_partner.write({'section_id': lead.section_id and lead.section_id.id or False})
                
            if partner_id:
                lead.write({'partner_id': partner_id[0]})
            partner_ids[lead.id] = partner_id
        
        return partner_ids
    
    @api.one
    def _create_lead_partner(self, lead):
        partner_id = False
        
        if self.partner_id and self.contact_name:
            partner_id = self._lead_create_contact(lead, self.contact_name, False, self.partner_id.id)
        else:
            partner_id = super(CrmLead, self)._create_lead_partner()
            
        return partner_id
