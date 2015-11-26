# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class claim_settings(osv.osv):
    ''' A model for storing the claim settings (next number) '''

    _name = "crm_claim.settings"
    _rec_name = 'next_number'

    _columns = {
        'next_number': fields.integer('The next claim number'),
    }
