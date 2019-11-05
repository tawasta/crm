from odoo import fields, models


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
