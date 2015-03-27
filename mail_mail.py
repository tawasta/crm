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
        ''' Send a BCC message to an address every time a mail is sent. This is for debugging purposes only. '''

        ''' Set a BCC recipient. This only works if one is not already set '''
        message['Bcc'] = "testi@vizucom.com"
        
        return super(ir_mail_server, self).send_email(cr, uid, message, mail_server_id, smtp_server, smtp_port,
                   smtp_user, smtp_password, smtp_encryption, smtp_debug,
                   context=context)

class mail_mail(osv.Model):
    _inherit = 'mail.mail'
    
    def create(self, cr, uid, values, context=None):
        ''' Override the default create '''
        
        ''' Always "send" a notification '''
        ''' TODO: Why is this necessary'''
        if 'notification' not in values and values.get('mail_message_id'):
            values['notification'] = True
       
        if context is None:
            context = {}

        model = context.get('default_model')
        if model and model=='crm.claim' and 'mail_message_id' in values:
            ''' Only send these kind of messages for claim model message instances '''
            message_model = self.pool.get('mail.message')
            message_instance = message_model.browse(cr, SUPERUSER_ID, [ values.get('mail_message_id') ])
            
            ''' Get message history from parent and grandparent (lower levels shouldn't exists on claims) '''
            mail_parent_id = message_instance.parent_id.id
            mail_grandparent_id = message_instance.parent_id.parent_id.id if message_instance.parent_id.parent_id.id else mail_parent_id
            message_child_ids = message_model.search(cr, SUPERUSER_ID, ['|',('parent_id', '=', mail_parent_id), ('parent_id', '=', mail_grandparent_id), ('subtype_id', '=', 1), ('id', '!=', message_instance.id),('parent_id', '!=', False)])
            
            ''' Get the current claim instance '''
            claim_model = self.pool.get('crm.claim')
            claim_instance = claim_model.browse(cr, SUPERUSER_ID, [ message_instance.res_id ])
            
            ''' Write a html-formatted messages history from previous message thread messages '''
            messages_history = '<div dir="ltr" style="color: grey;">'
            
            ''' Get users timezone '''
            user_pool = self.pool.get('res.users')
            user = user_pool.browse(cr, SUPERUSER_ID, uid)
            tz = pytz.timezone(user.partner_id.tz) or pytz.utc
            
            ''' Indentation level '''
            level = 1
            
            for child_id in message_child_ids:
                ''' Format child messages with incementing indentation '''
                ''' TODO: Should we use '>' for indentation instead of CSS? '''
                child_message = message_model.browse(cr, uid, [ child_id ])
                message_date = pytz.utc.localize( datetime.datetime.strptime( child_message.date , '%Y-%m-%d %H:%M:%S' ) ).astimezone(tz)
                
                level += 1
                messages_history += "<div style='padding-left: %sem;'>" % level
                messages_history += "<p>" + message_date.strftime('%d.%m.%Y %H:%M:%S') + ", " + child_message.email_from + " :</p>"
                messages_history += child_message.body
                messages_history += "</div>"
            
            messages_history += '</div>'
           
            ''' Get message header from reply_to settings '''
            header = claim_model._default_get_reply_header(cr, uid, context, claim_instance.company_id.id)
           
            ''' Get message footer from reply_to settings '''
            footer = claim_model._default_get_reply_footer(cr, uid, context, claim_instance.company_id.id)

            ''' If we have a message to show before header, it can be set in context. e.g. "Your claim has been received" before header '''
            if context.get('pre_header'):
                header = context.get('pre_header') + "<br/>" + header

            ''' Get message recipients from claim '''
            values['reply_to'] = claim_instance.reply_to
            values['email_from'] = claim_instance.reply_to
            values['email_cc'] = claim_instance.email_cc

            ''' Message subject '''
            values['record_name'] = "#" + str(claim_instance.claim_number) + ": " + claim_instance.name
            
            ''' A "static" header that's fetched from company-spesific settings '''
            static_header = "<p><small>" + str( header ) + "</small></p><hr style='margin: 1em 0 1em 0;'/>"
            static_header += '<p>#' + str(claim_instance.claim_number) + ": " + claim_instance.name + "</p>"
            static_header += '<p>'
            
            ''' The body_html is in html-format. We'll replace the heading <p>-tag with our own header '''
            values['body_html'] = re.sub(r'(^<p>)', static_header, values['body_html'])
            
            values['body_html'] += "<p><small>"
            values['body_html'] += "--<br/>"
            
            ''' Don't sign the message with sender name, if the message was sent by admin (e.g. automatic messages) '''
            if message_instance.create_uid.id != SUPERUSER_ID:
                values['body_html'] += str( message_instance.create_uid.partner_id.name )
                values['body_html'] += "<br/>"
            values['body_html'] += str( footer )
            values['body_html'] += "</small></p>"
            
            ''' Include messages history on the bottom of the message, under a horizontal line '''
            values['body_html'] += "<hr style='margin: 1em 0 1em 0;' />"
            values['body_html'] += messages_history
            values['body_html'] += "<br/>"

        return super(mail_mail, self).create(cr, uid, values, context=context)
        