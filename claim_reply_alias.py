from openerp.osv import osv, fields

class crm_claim_reply_alias(osv.osv):
    ''' Claim reply alias to remove support emails from claim CC-field.'''
    ''' NOT IMPLEMENTED '''
    
    _name='crm_claim.reply.alias'
    
    _columns={
        'reply_id': fields.many2one('crm_claim.reply', 'Reply id'),
        'name': fields.char('Address'),
        'description': fields.char('Description'),
    }