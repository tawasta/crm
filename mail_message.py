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
       
        if context is None:
            context = {}

        model = context.get('default_model')
        if model and model=='crm.claim' and 'mail_message_id' in values:
            message_model = self.pool.get('mail.message')
            message_instance = message_model.browse(cr, SUPERUSER_ID, [ values.get('mail_message_id') ])
            mail_parent_id = message_instance.parent_id.id
            mail_grandparent_id = message_instance.parent_id.parent_id.id
            message_child_ids = message_model.search(cr, SUPERUSER_ID, ['|',('parent_id', '=', mail_parent_id), ('parent_id', '=', mail_grandparent_id), ('subtype_id', '=', 1), ('id', '!=', message_instance.id)])
            
            claim_model = self.pool.get('crm.claim')
            claim_instance = claim_model.browse(cr, SUPERUSER_ID, [ message_instance.res_id ])
            
            messages_history = '<div dir="ltr" style="color: grey;">'
            
            for child_id in message_child_ids:
                child_message = message_model.browse(cr, SUPERUSER_ID, [ child_id ])
                
                messages_history += "<p>" + child_message.date + ", " + child_message.email_from + " :</p>"
                messages_history += child_message.body
            
            messages_history += '</div>'
            
            
            # TODO: clean up this mess:
            values['record_name'] = "#" + claim_instance.claim_number + ": " + claim_instance.name
            values['body_html'] = re.sub(r'(^<p>)', r'<p>#' + claim_instance.claim_number + ": " + claim_instance.name + "</p><p>", values['body_html']) + messages_history
        
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