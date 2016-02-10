# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
logger = logging.getLogger(__name__)

class CrmClaim(models.Model):

    # 1. Private attributes
    _inherit = 'crm.claim'

    # 2. Fields declaration
    claim_number = fields.Char('Claim number')

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def create(self, vals):
        if not vals.get('claim_number'):
            vals['claim_number'] = self.env['ir.sequence'].get('crm.claim')
        return super(CrmClaim, self).create(vals)

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default['claim_number'] = self.env['ir.sequence'].get('crm.claim')
        return super(CrmClaim, self).copy(default)

    # 7. Action methods

    # 8. Business methods
    @api.model
    def _init_claim_numbers(self):
        # When the module is installed, fetch all claims without a number and assign them one

        claims = self.search([('claim_number', '=', False)])

        for claim in claims:
            claim.claim_number = self.env['ir.sequence'].get('crm.claim')
            logger.debug("Setting claim number for #%s", claim.claim_number)
