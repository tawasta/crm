from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import re
import logging
_logger = logging.getLogger(__name__)

class mail_mail(osv.Model):
    _inherit = 'mail.mail'
    
    def create(self, cr, uid, values, context=None):
        if 'notification' not in values and values.get('mail_message_id'):
            values['notification'] = True
       
        if 'mail_message_id' in values:
            message_model = self.pool.get('mail.message')
            message_instance = message_model.browse(cr, SUPERUSER_ID, [ values['mail_message_id'] ])
            message_child_ids = message_model.search(cr, SUPERUSER_ID, [('parent_id', '=', message_instance.parent_id.id), ('subtype_id', '=', 1), ('id', '!=', message_instance.id)])
            
            messages_history = '<br/>'
            
            for child_id in message_child_ids:
                child_message = message_model.browse(cr, SUPERUSER_ID, [ child_id ])
                
                messages_history += "<p>" + child_message.email_from + " " + child_message.date + ":</p>" +  child_message.body 
            
            values['body_html'] = re.sub(r'(</p>)', r'</p><p>'+messages_history, values['body_html'])
        
        return super(mail_mail, self).create(cr, uid, values, context=context)

class mail_message(osv.Model):
    """ Update of mail_message class, to restrict mail access. """
    _inherit = 'mail.message'

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        model = context.get('default_model')
        if model and model=='crm.claim':
            res_id =  context.get('default_res_id')
            claim = self.pool[model].browse(cr,uid,res_id)
            if 'reply_to' not in values:
                values['reply_to'] = claim.reply_to if claim.reply_to else False

        newid = super(mail_message, self).create(cr, uid, values, context)
    
        return newid