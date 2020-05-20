<<<<<<< HEAD

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models


# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
=======
from odoo import fields, models
>>>>>>> 12.0


class CrmLead(models.Model):
    _inherit = 'crm.lead'

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
