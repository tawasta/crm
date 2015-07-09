# -*- coding: utf-8 -*-
from openerp import models, api, fields


class CrmLead2Opportunity(models.Model):
    _inherit = 'crm.lead2opportunity.partner'

    opportunity_ids = fields.Many2many(readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(CrmLead2Opportunity, self).default_get(fields)

        # Change the default action to convert
        res['name'] = 'convert'

        return res
