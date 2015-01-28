from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import re
import logging
_logger = logging.getLogger(__name__)

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
        