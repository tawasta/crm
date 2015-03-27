from openerp.osv import osv, fields

class crm_claim_reply(osv.osv):
    ''' Claim reply settings '''
    ''' TODO: rename this. It's evolved into a company-spesific claim settings instead of just plain reply-to address '''
    
    _name='crm_claim.reply'
    _columns={
        'company_id': fields.many2one('res.company', 'Company'),
        'reply_to': fields.char('Helpdesk reply to address', size=128, ),
        'reply_alias_ids': fields.one2many('crm_claim.reply.alias', 'reply_id', 'Reply aliases'),
        'message_received': fields.text('Message to be sent when a claim is created'), # not used
        'message_completed': fields.text('Message to be sent when a claim is completed'), # not used
        'message_rejected': fields.text('Message to be sent when a claim is rejected'), # not used
        'header': fields.text('Header message'),
        'footer': fields.text('Footer message'),
    }

crm_claim_reply()