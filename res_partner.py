# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class Partner(models.Model):
    
    _inherit = 'res.partner'
    
    @api.multi
    def unlink(self):
        ''' Deactivates the partner instead of deleting '''
        
        self.active = False
        
        return True