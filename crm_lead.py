# -*- coding: utf-8 -*-
from openerp import models, api, fields

class CrmLead(models.Model):
    
    _inherit = 'crm.lead'
    
    show_all = fields.Boolean('Show all fields')
    
    @api.onchange('partner_id')
    def partner_id_onchange(self):
        pass
        '''
        'partner_name': partner.parent_id.name if partner.parent_id else partner.name,
        'contact_name': partner.name if partner.parent_id else False,
        'title': partner.title and partner.title.id or False,
        'street': partner.street,
        'street2': partner.street2,
        'city': partner.city,
        'state_id': partner.state_id and partner.state_id.id or False,
        'country_id': partner.country_id and partner.country_id.id or False,
        'email_from': partner.email,
        'phone': partner.phone,
        'mobile': partner.mobile,
        'fax': partner.fax,
        'zip': partner.zip,
        'function': partner.function,
        '''