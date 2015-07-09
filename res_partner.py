# -*- coding: utf-8 -*-
from openerp import models, api


class Partner(models.Model):

    _inherit = 'res.partner'

    @api.multi
    def unlink(self):
        ''' Deactivates the partner instead of deleting '''

        self.write({'active': False})

        return True
