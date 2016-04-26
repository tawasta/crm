# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):
    
    # 1. Private attributes
    _inherit = 'res.partner'

    # 2. Fields declaration
    last_salesperson = fields.Many2one(
        'res.users',
        string='Latest salesperson',
        compute='_compute_last_salesperson',
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_last_salesperson(self):
        sale_order = self.env['sale.order']

        for record in self:
            parent = record._get_recursive_parent()

            if not parent:
                parent = record
            else:
                parent = record[0]

            # Search latest saleperson
            last_saleorder = sale_order.search(
                [('partner_id', 'in', (parent.id, record.id))],
                order='date_order DESC',
                limit=1,
            )

            if last_saleorder:
                record.last_salesperson = last_saleorder.user_id

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
