# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ClaimToOpportunity(models.TransientModel):
    
    # 1. Private attributes
    _name = 'claim.to.opportunity'

    # 2. Fields declaration
    partner = fields.Many2one('res.partner', 'Partner')
    name = fields.Char('Name')
    description = fields.Text('Description')
    user = fields.Many2one('res.users', 'User')

    # 3. Default methods
    @api.model
    def default_get(self, fields):
        res = super(ClaimToOpportunity, self).default_get(fields)

        active_id = self._context['active_id']

        claim = self.env['crm.claim'].browse([active_id])

        res['name'] = claim.name
        res['description'] = claim.description
        res['partner'] = claim.partner_id.id
        res['type'] = 'opportunity'

        return res

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def action_create_opportunity(self):
        pass

    # 8. Business methods
