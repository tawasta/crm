# -*- coding: utf-8 -*-
from openerp import models, api


class Partner(models.Model):

    _inherit = 'res.partner'

    @api.multi
    def unlink(self):
        ''' Deactivates the partner instead of deleting,
        unless the partner is already inactive '''

        for record in self:
            if record.active:
                record.active = False
            else:
                super(Partner, self).unlink()

        return True
