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
        # 'email': 'email_from',
        # 'phone': 'phone',
        # 'mobile': 'mobile',
        # 'fax': 'fax',
        # 'function': 'function'
        # 'title': 'title',
    }

    @api.one
    def write(self, vals):
        if vals.get('partner_id'):
            partner = self.partner_id

            vals['street'] = partner.street
            vals['street2'] = partner.street2
            vals['city'] = partner.city
            vals['zip'] = partner.zip
            vals['country_id'] = partner.country_id.id

        return super(CrmLead, self).write(vals)

    @api.one
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        def value_or_id(val):
            return val if isinstance(val, (bool, int, long, float, basestring)) \
                else val.id

        if self.partner_id:
            values = dict((value, value_or_id(self.partner_id[key]))
                          for key, value in self.LEAD_FIELDS.iteritems())

            for key, value in values.iteritems():
                setattr(self, key, value)

    @api.multi
    @api.depends('action', 'partner_id')
    def handle_partner_assignation(self, action, partner_id=False):
        partner_ids = {}

        for lead in self:
            if lead.partner_id and not lead.contact_name:
                partner_ids[lead.id] = lead.partner_id.id
                continue

            if lead.partner_id and lead.contact_name:
                partner_id = self._create_lead_partner(lead)[0]

            if not lead.partner_id and action == 'create':
                partner_id = self._create_lead_partner(lead)[0]
                self.env['res.partner'].write({'section_id': lead.section_id
                                               and lead.section_id.id
                                               or False})

            if partner_id:
                lead.write({'partner_id': partner_id})

            partner_ids[lead.id] = partner_id

        return partner_ids

    @api.one
    def _create_lead_partner(self, lead):
        partner_id = False

        if self.partner_id and self.contact_name:
            partner_id = self._lead_create_contact(lead, self.contact_name,
                                                   False, self.partner_id.id)
        else:
            partner_id = super(CrmLead, self)._create_lead_partner(lead)

        return partner_id

    @api.one
    def action_view_quotation(self):
        return self.env.ref('sale.view_order_form')

        return {
            'name': 'Sale order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'res_id': self.id,
            'view_id': False,
            'views': [(1, 'form')],
            'type': 'ir.actions.act_window',
        }
