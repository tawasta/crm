# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp import SUPERUSER_ID


class SaleOrder(models.Model):

    # 1. Private attributes
    _inherit = "sale.order"

    # 2. Fields declaration
    lead = fields.Many2one('crm.lead', "Related case")
    date_sent = fields.Datetime('Order sent')

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.v7
    def init(self, cr):
        # Creates lead references for existing sale orders
        lead_object = self.pool.get('crm.lead')

        lead_ids = lead_object.search(
            cr, SUPERUSER_ID,
            [('sale_order', '=', False)])
        leads = lead_object.browse(cr, SUPERUSER_ID, lead_ids)

        for lead in leads:
            if lead.ref:
                lead.sale_order = lead.ref
                lead.ref.lead = lead.id

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.one
    def write(self, values):
        # Update the date sent
        if 'state' in values and values['state'] == 'sent':
            values['date_sent'] = fields.Datetime.now()

        return super(SaleOrder, self).write(values)

    # 7. Action methods

    # 8. Business methods
