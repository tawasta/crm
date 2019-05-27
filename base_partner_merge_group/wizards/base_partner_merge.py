# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class MergePartnerAutomatic(models.TransientModel):

    _inherit = 'base.partner.merge.automatic.wizard'

    def _merge(self, partner_ids, dst_partner=None):
        if self.env.user.has_group('sales_team.group_sale_manager'):
            self = self.sudo()

        super(MergePartnerAutomatic, self)._merge(
            partner_ids=partner_ids,
            dst_partner=dst_partner,
        )
