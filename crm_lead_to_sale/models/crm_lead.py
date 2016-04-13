# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class CrmLead(models.Model):

    # 1. Private attributes
    _inherit = "crm.lead"

    # 2. Fields declaration
    sale_order = fields.Many2one('sale.order', "Related sale", copy=False)
    sale_order_state = fields.Char('Order state', compute='_get_sale_order_state', copy=False)
    sale_order_sent = fields.Char('Order sent', compute='_get_sale_order_sent', copy=False)

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.one
    @api.depends('sale_order')
    def _get_sale_order_state(self):
        if self.sale_order.state:
            states = dict(self.sale_order.fields_get(['state'])['state']['selection'])
            self.sale_order_state = states[self.sale_order.state]

    @api.one
    @api.depends('sale_order')
    def _get_sale_order_sent(self):
        if self.sale_order:
            self.sale_order_sent = self.sale_order.date_sent

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def action_quotation_send(self):
        res = self.sale_order.action_quotation_send()

        msg = _("Email for quotation")
        msg += " <b>%s</b> " % self.sale_order.name
        msg += _("sent")
        self.message_post(msg)

        return res

    # 8. Business methods
