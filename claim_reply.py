from openerp.osv import osv, fields

class crm_claim_reply(osv.osv):
    
    _name='crm_claim.reply'
    _columns={
        'company_id': fields.many2one('res.company', 'Company'),
        'reply_to': fields.char('Helpdesk reply to address', size=128, ),
        'message_received': fields.text('Message to be sent when a claim is created'), # not used
        'message_completed': fields.text('Message to be sent when a claim is completed'), # not used
        'message_rejected': fields.text('Message to be sent when a claim is rejected'), # not used
        'header': fields.text('Header message'),
        'footer': fields.text('Footer message'),
    }

crm_claim_reply()