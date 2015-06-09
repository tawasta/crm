# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class TokenKey(models.Model):
    
    _name = 'crm.tokenkey'
    _order = 'create_date DESC'

    ''' Columns '''
    name = fields.Char("Name / description")
    company_name = fields.Char("Company name")
    email = fields.Char("Email")
    key = fields.Char("Token key")
    database_name = fields.Char("Database name")
    type = fields.Selection( selection=[('demo', 'Demo'), ('game', 'Game'), ('production', 'Production')], string='Type', default='demo')
    
    date_reclaim = fields.Datetime("Key reclaim date")
    date_expiration = fields.Datetime("Key expiration date")
    date_database_created = fields.Datetime("Database create date")