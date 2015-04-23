# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    
    _inherit = 'res.partner'

    TYPES_ARRAY = ( ('contact', _('Contact')), ('delivery', _('Shipping')), ('einvoice', _('eInvoice')))
    
    def _get_display_name(self):
        ''' Returns a name with a complete hierarchy '''
        
        for record in self:
            record.display_name = self._get_recursive_name(record)
    
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
            _logger.warn(child_ids)
            record.address_contact_recursive_ids = self.search(['&',('id','in', child_ids ), ('type','=', 'contact')])

    ''' TODO: this function might be very heavy with large customer bases '''
    def _get_recursive_child_ids(self, record):
        child_ids = []
        
        for child in self.search([('parent_id','=', record.id )]):
            child_ids.append(child.id)
        
            if self.search([('parent_id','=', child.id )]):
                child_ids += self._get_recursive_child_ids(child)

        return child_ids
    
    '''
    # fnct_inv for dealing with saving functional field values
    def _set_contacts(self, cr, uid, ids, name, field_values, inv_arg, context):
        partner_obj = self.pool.get('res.partner')
        
        # Iterate through all of the document ids and see if they've been
        #  flagged by OE for create, write or unlink
        # See http://help.openerp.com/question/28714/how-to-insert-value-to-a-one2many-field-in-table-with-create-method/?answer=28771#post-id-28771
        for line in field_values:
            if line[0] == 0: # add
                line_id = line[1]
                partner_obj.create(cr, uid, line[2], context)
            elif line[0] == 1: # update
                line_id = line[1]
                partner_obj.write(cr, uid, [line_id], line[2], context)                
            elif line[0] == 2: # delete
                line_id = line[1]
                partner_obj.unlink(cr, uid, [line_id], context)
        return True
    '''

    ''' Columns '''
    type = fields.Selection(TYPES_ARRAY, 'Address Type')
    display_name = fields.Char(string='Name', compute='_get_display_name')
                
    #'address_contact_recursive_ids': fields.One2many(_get_contacts, fnct_inv=_set_contacts, relation="res.partner", method=True, type="one2many", string=_("Contacts")),
    address_contact_recursive_ids = fields.One2many('res.partner', 'parent_id', string=_('Contact'), compute='_get_contacts')
    address_einvoice_ids = fields.One2many('res.partner', 'parent_id', string=_('e-Invoice'), domain=[('type', '=', 'einvoice')])
    address_delivery_ids = fields.One2many('res.partner', 'parent_id', string=_('Delivery'), domain=[('type', '=', 'delivery')])
        
    edicode = fields.Char(string='Edicode')
    einvoice_operator = fields.Char(string='eInvoice operator')
    
    is_company = fields.Boolean(default=True)
    