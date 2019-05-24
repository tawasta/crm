# 1. Standard library imports:
import re

# 2. Known third party imports:
from bs4 import BeautifulSoup

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ClaimToOpportunity(models.TransientModel):

    # 1. Private attributes
    _name = 'claim.to.opportunity'

    # 2. Fields declaration
    partner = fields.Many2one('res.partner', 'Partner', required=True)
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    user = fields.Many2one('res.users', 'User')

    # 3. Default methods
    @api.model
    def default_get(self, fields):
        res = super(ClaimToOpportunity, self).default_get(fields)

        active_id = self._context['active_id']

        claim = self.env['crm.claim'].browse([active_id])

        # Replace possible br-elements with line breaks
        description = re.sub('<br\s*[\/]?>', '\n', claim.description or '')

        res['name'] = "%s - %s" % (claim.partner_id.name, claim.name)
        # Strip possible html elements
        res['description'] = BeautifulSoup(description, 'lxml').text
        res['partner'] = claim.partner_id.id
        res['user'] = self._uid

        return res

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def create_opportunity(self):
        self.ensure_one()
        context = self._context

        values = {
            'partner_id': self.partner.id,
            'name': self.name,
            'description': self.description,
            'type': 'opportunity',
        }

        opportunity = self.env['crm.lead'].create(values)

        # Add user after creating to trigger an auto-message
        if self.user:
            opportunity.user_id = self.user.id

        if 'active_id' in context:
            active_id = context['active_id']
            claim = self.env['crm.claim'].browse([active_id])

            opportunity.claim = claim.id

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'crm.lead',
            'target': 'current',
            'res_id': opportunity.id,
            'type': 'ir.actions.act_window',
        }

    # 8. Business methods
