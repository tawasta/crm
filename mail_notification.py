from openerp.osv import osv, fields

import logging
_logger = logging.getLogger(__name__)

class mail_notification(osv.Model):
    _inherit = 'mail.notification'

    def get_signature_footer(self, cr, uid, user_id, res_model=None, res_id=None, context=None, user_signature=True):
        model = context.get('default_model')
        if not model:
            model = context.get('default_res_model')
        
        if model and model=='crm.claim':
            ''' Remove signature footer from claim messages ("this claim was sent by x using Odoo") '''
            return ""
    
        return super(mail_notification, self).get_signature_footer(cr, uid, user_id, res_model, res_id, context, user_signature)
    
    def get_partners_to_email(self, cr, uid, ids, message, context=None):
        notify_pids = super(mail_notification, self).get_partners_to_email(cr, uid, ids, message, context)
        
        ''' Send helpdesk messages even if partner has notifications disabled '''
        if message.model == "crm.claim":
            for notification in self.browse(cr, uid, ids, context=context):
                partner = notification.partner_id
                
                if partner.notify_email == 'none':
                    notify_pids.append(partner.id)
        
        return notify_pids