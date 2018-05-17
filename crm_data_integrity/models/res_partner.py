# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import models, api

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ResPartner(models.Model):

    # 1. Private attributes
    _inherit = 'res.partner'

    # 2. Fields declaration
    @api.multi
    def unlink(self):
        # Deactivates the partner instead of deleting,
        # Only sysadmins can actually delete records

        for record in self:
            if record.active:
                record.active = False
            elif self.env.user.has_group('base.group_system'):
                super(ResPartner, self).unlink()

        return True
