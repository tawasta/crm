from openerp.osv import osv
from openerp import tools
from openerp import SUPERUSER_ID
import re
from openerp.addons.mail.mail_message import decode

import logging
_logger = logging.getLogger(__name__)

def decode_header(message, header, separator=' '):
    return separator.join(map(decode, filter(None, message.get_all(header, []))))

class mail_thread(osv.Model):

    _inherit = 'mail.thread'

    def message_route(self, cr, uid, message, message_dict, model=None, thread_id=None,
                      custom_values=None, context=None):
        
        res = super(mail_thread, self).message_route(cr, uid, message, message_dict, model, thread_id, custom_values, context)

        ''' Try matching by the claim number '''
        try:
            ''' A try-block if res is empty for some reason '''
            _logger.warn(res)
            if res[0][0] == 'crm.claim' and res[0][1] == False:
                ''' Could not match the claim with header information. Trying to match by subject '''
                claim_number_re = re.compile("[0-9]{5}[^0-9]", re.UNICODE)
                number_re = re.compile("[0-9]+", re.UNICODE)
                
                message_subject = decode_header(message, 'Subject')
                match = claim_number_re.search(message_subject)
                
                claim_number = match and match.group(0)
                ''' Strip all but numbers'''
                claim_number = number_re.search(claim_number).group(0)

                claim_id = self.pool.get('crm.claim').search(cr, SUPERUSER_ID, [('claim_number', '=', claim_number)])

                ''' Rewrite the res tuple '''
                lst = list(res[0])
                lst[1] = claim_id[0]
                res[0] = tuple(lst)
                _logger.info('Matched a message "%s" to claim "#%s" using message subject', message_subject, claim_number)
                
        except Exception, e:
            ''' TODO: FIX "Error while matching a claim: expected string or buffer" '''

            _logger.warn('Error while matching a claim: %s', e)
            
        return res

    '''
    def _find_partner_from_emails(self, cr, uid, id, emails, model=None, context=None, check_followers=True):
        res = super(mail_thread, self)._find_partner_from_emails(cr, uid, id, emails, model, context=context, check_followers=check_followers)
        
        for email in emails:
            partner_obj = self.pool.get('res.partner')
            email_address = tools.email_split(email)[0]
            # Escape special SQL characters in email_address to avoid invalid matches
            email_address = (email.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_'))
            email_brackets = "<%s>" % email_address
            # exact, case-insensitive match
            ids = partner_obj.search(cr, SUPERUSER_ID,
                                     [('email', '=ilike', email_address),
                                      ('user_ids', '!=', False)],
                                     limit=1, context=context)
            
            if not ids:
                # if no match with addr-spec, attempt substring match within name-addr pair
                ids = partner_obj.search(cr, SUPERUSER_ID,
                                         [('email', 'ilike', email_brackets),
                                          ('user_ids', '!=', False)],
                                         limit=1, context=context)
            
            if not ids:
                _logger.warn("%s not found. Creating", email)
                partner_id = partner_obj.create(cr, uid, {'name': email_address, 'email': email})
                res.append(partner_id)
        
        return res
    '''

    '''
    def message_parse(self, cr, uid, message, save_original=False, context=None):
        res = super(mail_thread, self).message_parse(cr, uid, message, save_original, context=context)
        
        _logger.warn(context)
        _logger.warn(res)
        
        return res
    '''

    '''
    def message_new(self, cr, uid, msg_dict, custom_values=None, context=None):
        _logger.warn("self: %s" % self)
        _logger.warn("msg: %s" % msg_dict)
        _logger.warn("cust: %s" % custom_values)
        _logger.warn("ctx: %s" % context)

        return super(mail_thread, self).message_new(self, cr, uid, msg_dict, custom_values, context)
    '''
        
    '''
    def message_process(self, cr, uid, model, message, custom_values=None,
                        save_original=False, strip_attachments=False,
                        thread_id=None, context=None):
        
        _logger.warn("model: %s" % model)
        _logger.warn("msg: %s" % message)
        _logger.warn("cust: %s" % custom_values)
        _logger.warn("ctx: %s" % context)
    
        return super(mail_thread, self).message_process(cr, uid, model, message, custom_values, save_original, strip_attachments, thread_id, context)
    '''