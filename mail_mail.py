from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import re
import datetime
import pytz
import logging
_logger = logging.getLogger(__name__)

class ir_mail_server(osv.Model):
    _inherit = 'ir.mail_server'
    
    def send_email(self, cr, uid, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False,
                   context=None):
        ''' Send a BCC message to an address every time a mail is sent '''

        # Set a BCC recipient. This only works if one is not already set
        message['Bcc'] = "testi@vizucom.com"
        
        return super(ir_mail_server, self).send_email(cr, uid, message, mail_server_id, smtp_server, smtp_port,
                   smtp_user, smtp_password, smtp_encryption, smtp_debug,
                   context=context)

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
            
            # get users timezone
            user_pool = self.pool.get('res.users')
            user = user_pool.browse(cr, SUPERUSER_ID, uid)
            tz = pytz.timezone(user.partner_id.tz) or pytz.utc
            
            for child_id in message_child_ids:
                child_message = message_model.browse(cr, uid, [ child_id ])
                message_date = pytz.utc.localize( datetime.datetime.strptime( child_message.date , '%Y-%m-%d %H:%M:%S' ) ).astimezone(tz)
                
                messages_history += "<p>" + message_date.strftime('%d.%m.%Y %H:%M:%S') + ", " + child_message.email_from + " :</p>"
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
        