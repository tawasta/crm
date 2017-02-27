# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import tools, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
logger = logging.getLogger(__name__)


class CrmClaimStage(models.Model):

    # 1. Private attributes
    _inherit = 'crm.claim.stage'

    # 2. Fields declaration
    new_reply_stage = fields.Boolean("New reply stage", help="Claim will be returned to this stage on new message")

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
