from openerp.osv import osv, fields

class mail_notification(osv.Model):
    _inherit = 'mail.notification'

    def get_signature_footer(self, cr, uid, user_id, res_model=None, res_id=None, context=None, user_signature=True):
        model = context.get('default_model')
        if model and model=='crm.claim':
            return ""
    
        return super(mail_notification, self).get_signature_footer(cr, uid, user_id, res_model, res_id, context, user_signature)