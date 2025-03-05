# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class Lead(models.Model):
    # 1. Private attributes
    _inherit = "crm.lead"

    # 2. Fields declaration
    event_start_date = fields.Date(
        help="Start Date of the event, if one is organized based on this lead."
    )

    event_end_date = fields.Date(
        help="End Date of the event, if one is organized based on this lead."
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
