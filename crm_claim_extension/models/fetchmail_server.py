# -*- coding: utf-8 -*-
from openerp import api, fields, models


class FetchmailServer(models.Model):

    _inherit = 'fetchmail.server'

    # The point of company id in fetchmail servers is to allow matching the claims to a correct company in a
    # multi-company environment
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True
    )
