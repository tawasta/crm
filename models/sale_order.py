# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import SUPERUSER_ID


class SaleOrder(models.Model):
    _inherit = "sale.order"

    lead = fields.Many2one('crm.lead', "Related case")

    @api.v7
    def init(self, cr):
        # Creates lead references for existing sale orders
        lead_object = self.pool.get('crm.lead')

        lead_ids = lead_object.search(cr, SUPERUSER_ID,
                                      [('sale_order', '=', False)])
        leads = lead_object.browse(cr, SUPERUSER_ID, lead_ids)

        for lead in leads:
            if lead.ref:
                lead.sale_order = lead.ref
                lead.ref.lead = lead.id
