# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    
    _inherit = 'res.partner'

    TYPES_ARRAY = ( ('contact', _('Contact')), ('delivery', _('Affiliate')), ('invoice', _('e-Invoice')))
    
    @api.one
    def _get_display_name(self):
        ''' Returns a name with a complete hierarchy '''
        
        for record in self:
            display_name = self._get_recursive_name(record)
            record.write({'display_name': display_name, 'full_name': display_name})
    
    def _get_recursive_name(self, record):
        ''' Returns a recursive partner name '''
        
        if not record.parent_id:
            record.display_name = record.name
        else:
            record.display_name = "%s, %s" % (self._get_recursive_name(record.parent_id), record.name)
        
        return record.display_name
    
    def _get_contacts(self):
        for record in self:
            child_ids = self._get_recursive_child_ids(record)
            record.address_contact_recursive_ids = self.search(['&',('id','in', child_ids ), ('type','=', 'contact')])

    ''' NOTE: this function might be pretty heavy to run with large customer bases '''
    ''' TODO: optimization '''
    def _get_recursive_child_ids(self, record):
        child_ids = []
        
        for child in self.search([('parent_id','=', record.id )]):
            child_ids.append(child.id)
        
            if self.search([('parent_id','=', child.id )]):
                child_ids += self._get_recursive_child_ids(child)

        return child_ids

    @api.model
    def _set_contacts(self):
        for record in self:
            for contact in record.address_contact_recursive_ids:
                if isinstance(contact.id, models.NewId):
                    ''' TODO: there must be a smarter way to do this '''
                    contact_values = {
                        'name': contact.name,
                        'phone': contact.phone, 
                        'email': contact.email, 
                        'title': contact.title.id, 
                        'parent_id': record.id,
                        'type': contact.type, 
                        'is_company': contact.is_company,
                        'use_parent_address': contact.use_parent_address,
                    }
                    self.create(contact_values)

    ''' Columns '''
    type = fields.Selection(TYPES_ARRAY, 'Address Type')
    
    ''' TODO: For some reason the display_name isn't being overridden '''
    display_name = fields.Char(string='Name', compute='_get_display_name')
    full_name = fields.Char(string='Name', compute='_get_display_name')
                
    address_contact_recursive_ids = fields.One2many('res.partner', 'parent_id', string=_('Contact'), compute='_get_contacts', inverse='_set_contacts')
    address_einvoice_ids = fields.One2many('res.partner', 'parent_id', string=_('e-Invoice'), domain=[('type', '=', 'invoice')])
    address_affiliate_ids = fields.One2many('res.partner', 'parent_id', string=_('Affiliate'), domain=[('type', '=', 'delivery')])
        
    edicode = fields.Char(string='Edicode')
    einvoice_operator = fields.Char(string='e-Invoice operator')
    
    is_company = fields.Boolean(default=True)
    