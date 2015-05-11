# -*- coding: utf-8 -*-
from openerp import models, api, fields

class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    show_all= fields.Boolean('Show all fields')