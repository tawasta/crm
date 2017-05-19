# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):

    # 1. Private attributes
    _inherit = 'res.partner'
    _order = 'name_order'

    TYPES_ARRAY = (
        ('contact', 'Contact'),
        ('delivery', 'Affiliate'),
        ('invoice', 'e-Invoice address')
    )

    # 2. Fields declaration
    type = fields.Selection(TYPES_ARRAY, 'Address Type')

    name = fields.Char(inverse='_set_name')
    display_name = fields.Char(compute='_get_display_name')
    name_order = fields.Char(compute='_get_name_order', store=True)

    street_address = fields.Char('Street address')

    address_contact_ids = fields.One2many(
        'res.partner',
        'parent_id',
        string='Contact',
        domain=[('type', '=', 'contact')]
    )
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

    is_company = fields.Boolean(default=True)

    # 3. Default methods
    @api.multi
    @api.depends('name', 'parent_id')
    def name_get(self):
        # Use display name instead of name
        res = []

        for record in self:
            name = record.display_name
            res.append((record.id, name))

        return res

    # 4. Compute and search fields, in the same order that fields declaration
    @api.one
    @api.depends('name', 'parent_id.name')
    def _get_display_name(self):
        # Returns a name with a complete hierarchy
        self.display_name = self._get_recursive_name(self)

    @api.one
    @api.depends('name', 'display_name', 'type')
    def _get_name_order(self):
        self.name_order = self._get_recursive_name_order(self)

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

    def _get_recursive_name_order(self, record):
        if record.parent_id:
            ordering_type = record.type if record.type == 'contact' else ''

            record.name_order = "%s, %s %s" % (
                self._get_recursive_name_order(record.parent_id),
                record.type,
                record.name
            )
        else:
            record.name_order = record.name

        return record.name_order

    def _get_contacts(self):
        for record in self:
            child_ids = self._get_recursive_child_ids(record)
            record.address_contact_recursive_ids = \
                self.search([
                    ('id', 'in', child_ids),
                    ('type', '=', 'contact')
                ])

    @api.one
    def _set_contacts(self):
        for record in self:
            self.address_contact_ids = self.address_contact_recursive_ids

    # 5. Constraints and onchanges
    @api.one
    @api.onchange('use_parent_address')
    def onchange_use_parent_address(self):
        # Updates address values from the parent

        def value_or_id(val):
            # return val or val.id if val is a browse record
            return val if isinstance(val, (bool, int, long, float, basestring))\
                else val.id

        if self.parent_id and self.use_parent_address:
            values = dict((key, value_or_id(self.parent_id[key]))
                          for key in self._address_fields())

            # Can't use self.write, as it doesn't update the fields
            # self.write(values)

            # Set the address fields from the parent
            for key, value in values.iteritems():
                setattr(self, key, value)

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
