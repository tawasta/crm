# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class CrmLead(models.Model):
    # 1. Private attributes
    _inherit = 'crm.lead'

    # 2. Fields declaration
    next_event_id = fields.Many2one(
        comodel_name='calendar.event',
        string='Next activity',
        copy=False,
    )
    next_event_start = fields.Datetime(
        string='Activity start',
        related='next_event_id.start_datetime',
    )
    next_event_duration = fields.Float(
        string='Activity duration',
        related='next_event_id.duration',
    )

    # 3. Default methods

    # 4. Compute and search fields

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
