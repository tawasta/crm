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
    def create(self, vals):
        if 'personal_customer' in vals and vals['personal_customer']:
            vals['is_company'] = False

        return super(ResPartner, self).create(vals)

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
