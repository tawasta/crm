# -*- coding: utf-8 -*-
from openerp import models, api


class CrmLead2Opportunity(models.Model):
    _inherit = 'crm.lead2opportunity.partner'

    @api.model
    def default_get(self, fields):
        res = super(CrmLead2Opportunity, self).default_get(fields)

        # Change the default action to convert
        res['name'] = 'convert'

        return res
