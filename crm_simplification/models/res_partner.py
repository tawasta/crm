# -*- coding: utf-8 -*-
from openerp import models, api, fields


class ResPartner(models.Model):

    _inherit = 'res.partner'

    show_all = fields.Boolean(
        'Show all fields',
        help="Some of the lesser used fields are hidden by default"
    )

    # This field is only a helper for "is company"
    personal_customer = fields.Boolean(
        'Private Customer',
        help="A customer that's not a company"
    )

    @api.model
    def create(self, values):
        if 'personal_customer' in values and values['personal_customer']:
            values['is_company'] = False

        if 'contact_id' in values and values['contact_id']:
            values['is_company'] = False
            values['personal_customer'] = True

        return super(ResPartner, self).create(values)

    @api.onchange('personal_customer')
    def personal_customer_onchange(self):
        if self.personal_customer:
            self.is_company = False
            self.businessid_shown = False
        else:
            self.is_company = True
            self.businessid_shown = True

    @api.onchange('is_company')
    def is_company_onchange(self):
        if self.is_company:
            self.personal_customer = False
        else:
            self.personal_customer = True
