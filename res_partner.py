# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    
    _inherit = 'res.partner'

    TYPES_ARRAY = ( ('contact', _('Contact')), ('delivery', _('Shipping')), ('einvoice', _('eInvoice')))
    
    '''
    def _get_full_name(self, cr, uid, ids, field_name, arg, context=None):
        records = self.browse(cr, uid, ids)
        result = {}
        for record in records:
            if hasattr(record, 'lvl2_name') and hasattr(record, 'lvl3_name'):
                result[record.id] = record.lvl2_name + " / " + record.lvl3_name + " / " + record.name
            else:
                result[record.id] = record.name
        
        return result
    
    def _get_contacts(self, cr, uid, ids, name, arg, context=None):
        record = self.browse(cr, uid, ids, context=context)[0]
        
        result = {}
        records = self.browse(cr, uid, ids)
        
        # Fetch two levels of children
        domain = ['&', '|',('parent_id','=',record.id),('parent_id.parent_id','=',record.id),('type', '=', 'contact')]
        contact_ids = self.search(cr, uid, args=domain, context=context)
        
        for record in records:
            result[record.id] = contact_ids
        
        return result
    
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
                
    #'address_contact_recursive_ids': fields.One2many(_get_contacts, fnct_inv=_set_contacts, relation="res.partner", method=True, type="one2many", string=_("Contacts")),
    address_contact_recursive_ids = fields.One2many('res.partner', 'parent_id', string=_('e-Invoice'), domain=[('type', '=', 'contact')])
    address_einvoice_ids = fields.One2many('res.partner', 'parent_id', string=_('e-Invoice'), domain=[('type', '=', 'einvoice')])
    address_delivery_ids = fields.One2many('res.partner', 'parent_id', string=_('Delivery'), domain=[('type', '=', 'delivery')])
        
    edicode = fields.Char(string='Edicode')
    einvoice_operator = fields.Char(string='eInvoice operator')
    
    is_company = fields.Boolean(default=True)
    