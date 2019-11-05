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
    parent_partners = fields.Many2many(
        'res.partner',
        'res_partner_contacts_relation',
        'parent_partners',
        'child_partners',
        string="Belongs to",
        #  domain=[('is_company', '=', True)],
    )
    child_partners = fields.Many2many(
        'res.partner',
        'res_partner_contacts_relation',
        'child_partners',
        'parent_partners',
        string="Contacts",
        domain=[('is_company', '=', False), ('customer', '=', True)]
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
