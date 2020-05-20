from odoo import api, models, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    @api.multi
    def action_set_lost(self):
        for lead in self:
            stage_id = lead._stage_find(domain=[('probability', '=', 0),
                                                ('on_change', '=', True),
                                                ('fold', '=', True)])
            if not stage_id:
                raise ValidationError(
                    _("""Missing a stage with these settings:
                         - Folded in Pipeline: True
                         - Change Probability Automatically: True
                         - Probability: 0.00

                         Please modify/add a stage to have these values.""")
                )
            lead.write({'stage_id': stage_id.id, 'probability': 0})
        return True
