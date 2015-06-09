# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class ResPartner(models.Model):
    
    _inherit = 'res.partner'
    
    tokenkey_ids = fields.One2Many('crm.tokenkey')