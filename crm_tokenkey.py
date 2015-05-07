# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.tools.translate import _

class TokenKey(models.Model):
    
    _name = 'crm.tokenkey'

    ''' Columns '''
    name = fields.Char("Name / description")
    company_name = fields.Char("Company name")
    email = fields.Char("Email")
    key = fields.Char("Token key")
    date_reclaim = fields.Date("Key reclaim date")
    date_expiration = fields.Date("Key expiration date")
    date_database_created = fields.Date("Database create date")