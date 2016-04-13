from openerp.osv import osv
from openerp import _

class InviteWizard(osv.osv_memory):

    _inherit = 'mail.wizard.invite'
    
    def default_get(self, cr, uid, fields, context=None):
        
        res = super(InviteWizard, self).default_get(cr, uid, fields, context=context)

        model = res.get('res_model')

        if model == 'crm.claim':        
            user_name = self.pool.get('res.users').name_get(cr, uid, [uid], context=context)[0][1]
            
            res_id = res.get('res_id')
            
            document_name = self.pool[model].browse(cr, uid, [res_id], context=context).claim_number
    
            header = _("Hello")
            message = _("%s has invited you to follow claim #%s" % (user_name, document_name) )
    
            res['message'] = "<p>%s!</p><p>%s.</p>" % (header, message)
        
        return res