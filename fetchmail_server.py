from openerp.osv import osv, fields

class mail_thread(osv.Model):
    ''' Add a company for fetchmail servers so we can match the claims for a correct company '''
    _inherit = 'fetchmail.server'
    
    _columns = {
        'company_id': fields.many2one('res.company', string='Company', required=True),
    }

    