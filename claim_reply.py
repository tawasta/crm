from openerp.osv import osv, fields

class crm_claim_reply(osv.osv):
    
    _name='crm_claim.reply'
    _columns={
        'company_id': fields.many2one('res.company', 'Company'),
        'reply_to': fields.char('Helpdesk reply to address', size=128, ),
    }

crm_claim_reply()