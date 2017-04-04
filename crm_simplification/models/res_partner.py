# -*- coding: utf-8 -*-
from openerp import models, api, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    show_all = fields.Boolean(
        'Show all fields',
        help="Some of the lesser used fields are hidden by default"
    )

    # This field is only a helper for "is company"
    private_customer = fields.Boolean(
        'Private Customer',
        help="A customer that's not a company",
    )

    # Deprecated
    personal_customer = fields.Boolean(
        'Private Customer',
        help="A customer that's not a company"
    )

    @api.multi
    @api.depends('is_company', 'personal_customer')
    def compute_private_customer(self):
        for record in self:
            record.private_customer = not record.is_company

    @api.model
    def create(self, values):
        if 'private_customer' in values and values['private_customer']:
            values['is_company'] = False

        if 'contact_id' in values and values['contact_id']:
            values['is_company'] = False
            values['private_customer'] = True

        return super(ResPartner, self).create(values)

    @api.onchange('private_customer')
    def private_customer_onchange(self):
        self.is_company = not self.private_customer
        self.businessid_shown = not self.private_customer

    @api.onchange('is_company')
    def is_company_onchange_update_private_customer(self):
        self.private_customer = not self.is_company

