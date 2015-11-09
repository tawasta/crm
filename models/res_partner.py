# -*- coding: utf-8 -*-
from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):

    _inherit = 'res.partner'

    ''' TODO
        ORDER BY:
            parent
                parent contacts
            child
                child contacts
            child2
                child2 contact
    '''
    _order = 'display_name ASC'

    TYPES_ARRAY = (('contact', 'Contact'),
                   ('delivery', 'Affiliate'),
                   ('invoice', 'e-Invoice address'))

    # street_address = fields.Char('Street address')

    @api.one
    @api.depends('name', 'parent_id.name')
    def _get_display_name(self):
        # Returns a name with a complete hierarchy

        self.display_name = self._get_recursive_name(self)

    @api.one
    def _set_name(self):
        # Updates all children display names

        child_ids = self._get_recursive_child_ids(self)
        children = self.search([('id', 'in', child_ids)])

        for record in children:
            record.display_name = self._get_recursive_name(record)

    def _get_recursive_name(self, record):
        # Returns a recursive partner name

        if record.parent_id:
            record.display_name = "%s, %s"\
                % (self._get_recursive_name(record.parent_id), record.name)
        else:
            record.display_name = record.name

        return record.display_name

    def _get_contacts(self):
        for record in self:
            child_ids = self._get_recursive_child_ids(record)
            record.address_contact_recursive_ids = \
                self.search(['&', ('id', 'in', child_ids),
                             ('type', '=', 'contact')])

    ''' NOTE: this function might be pretty heavy to
    run with large customer bases '''

    ''' TODO: optimization '''
    def _get_recursive_child_ids(self, record):
        child_ids = []

        for child in self.search([('parent_id', '=', record.id)]):
            child_ids.append(child.id)

            if self.search([('parent_id', '=', child.id)]):
                child_ids += self._get_recursive_child_ids(child)

        return child_ids

    @api.one
    def _set_contacts(self):
        # There's probably a smarter way to do this

        new_contacts = []

        for contact in self.address_contact_recursive_ids:
            if isinstance(contact.id, models.NewId):
                contact_values = {}
                for attr in contact._columns:
                    val = getattr(contact, attr, False)
                    if getattr(val, 'id', False):
                        val = val.id

                    if val:
                        contact_values[attr] = val

                contact_values['parent_id'] = self.id,

                new_contacts.append(contact_values)

        for new_contact in new_contacts:
            self.create(new_contact)

    @api.one
    @api.onchange('use_parent_address')
    def onchange_use_parent_address(self):
        ''' Updates address values from the parent '''

        def value_or_id(val):
            """ return val or val.id if val is a browse record """
            return val if isinstance(val, (bool, int, long, float, basestring))\
                else val.id

        if self.parent_id and self.use_parent_address:
            values = dict((key, value_or_id(self.parent_id[key]))
                          for key in self._address_fields())

            ''' Can't use self.write, as it doesn't update the fields '''
            # self.write(values)

            ''' Set the address fields from the parent '''
            for key, value in values.iteritems():
                setattr(self, key, value)

    ''' Columns '''
    type = fields.Selection(TYPES_ARRAY, 'Address Type')

    name = fields.Char(inverse='_set_name')
    display_name = fields.Char(compute='_get_display_name')

    address_contact_recursive_ids = fields.One2many(
        'res.partner',
        'parent_id',
        string='Contact',
        compute='_get_contacts',
        inverse='_set_contacts'
    )
    address_einvoice_ids = fields.One2many(
        'res.partner',
        'parent_id',
        string='e-Invoice',
        domain=[('type', '=', 'invoice')]
    )
    address_affiliate_ids = fields.One2many(
        'res.partner',
        'parent_id',
        string='Affiliate',
        domain=[('type', '=', 'delivery')]
    )

    edicode = fields.Char(string='Edicode')
    einvoice_operator = fields.Char(string='e-Invoice operator')

    is_company = fields.Boolean(default=True)
