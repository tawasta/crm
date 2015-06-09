# -*- coding: utf-8 -*-
from openerp import models, fields, api, _

class TokenKey(models.Model):
    
    _name = 'crm.tokenkey'
    _order = 'create_date DESC'

    ''' Columns '''
    name = fields.Char("Key name", required=True)
    company_name = fields.Char("Company name", required=True)
    email = fields.Char("Email", required=True)
    partner_id = fields.Many2one('res.partner', domain=[('customer','=',True)])
    
    key = fields.Char("Token key", required=True)
    database_name = fields.Char("Database name")
    type = fields.Selection( 
        selection=[('demo', 'Demo'), ('game', 'Game'), ('production', 'Production')], 
        string='Type', 
        default='demo', 
        required=True
    )
    
    date_reclaim = fields.Datetime("Key reclaim date")
    date_expiration = fields.Datetime("Key expiration date")
    date_database_created = fields.Datetime("Database create date")