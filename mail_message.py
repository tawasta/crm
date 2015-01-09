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
            mail_grandparent_id = message_instance.parent_id.parent_id.id if message_instance.parent_id.parent_id.id else mail_parent_id
            message_child_ids = message_model.search(cr, SUPERUSER_ID, ['|',('parent_id', '=', mail_parent_id), ('parent_id', '=', mail_grandparent_id), ('subtype_id', '=', 1), ('id', '!=', message_instance.id),('parent_id', '!=', False)])
            
            claim_model = self.pool.get('crm.claim')
            claim_instance = claim_model.browse(cr, SUPERUSER_ID, [ message_instance.res_id ])
            
            messages_history = '<div dir="ltr" style="color: grey;">'
            
            for child_id in message_child_ids:
                child_message = message_model.browse(cr, uid, [ child_id ])
                
                messages_history += "<p>" + child_message.date + ", " + child_message.email_from + " :</p>"
                messages_history += child_message.body
            
            messages_history += '</div>'
           
            footer = claim_model._default_get_reply_footer(cr, uid, context, claim_instance.company_id.id)
            signature = claim_model._default_get_reply_signature(cr, uid, context, claim_instance.company_id.id)

            values['reply_to'] = claim_instance.reply_to
            values['email_from'] = claim_instance.reply_to
            values['email_cc'] = claim_instance.email_cc

            # TODO: clean up this mess:
            values['record_name'] = "#" + str(claim_instance.claim_number) + ": " + claim_instance.name
            values['body_html'] = re.sub(r'(^<p>)', r'<p>#' + str(claim_instance.claim_number) + ": " + claim_instance.name + "</p><p>", values['body_html'])
            
            values['body_html'] += messages_history
            
            values['body_html'] += "<p>--</p>"
            values['body_html'] += "<p><small>" + signature + "</small></p>"
            values['body_html'] += "<p><small>" + footer + "</small></p>"
        
        return super(mail_mail, self).create(cr, uid, values, context=context)

class mail_message(osv.Model):
    _inherit = 'mail.message'
    
    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        model = context.get('thread_model')

        if model and model=='crm.claim':
            ''' TODO: Get rid of this hack.
                For some reason the author_id is False if new partner was created
            '''
            if values.get('author_id') == False:
                email_from = values.get('email_from')
                email_regex = re.compile("[<][^>]+[>]")
                
                email = email_regex.findall(email_from)[0]
                email = re.sub(r'[<>]', "", email)

                values['author_id'] = self.get_author_by_email(cr, uid, values, context)
                
            
        return super(mail_message, self).create(cr, uid, values, context=context)
    
    def get_author_by_email(self, cr, uid, values, context=None):
        email_from = values.get('email_from')
        email_regex = re.compile("[<][^>]+[>]")
        
        email = email_regex.findall(email_from)[0]
        email = re.sub(r'[<>]', "", email)
    
        author = self.pool.get('res.partner').search(cr, uid, [('email','=',email)])[0]
        
        return author
        