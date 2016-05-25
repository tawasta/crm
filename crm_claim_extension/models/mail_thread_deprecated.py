from openerp.osv import osv
from openerp import tools
from openerp import SUPERUSER_ID

import logging
_logger = logging.getLogger(__name__)


class mail_thread(osv.Model):

    _inherit = 'mail.thread'
    
    def _find_partner_from_emails(self, cr, uid, id, emails, model=None, context=None, check_followers=True):
        res = super(mail_thread, self)._find_partner_from_emails(
            cr, uid, id, emails, model, context=context, check_followers=check_followers
        )

        for email in emails:
            partner_obj = self.pool.get('res.partner')
            email_address = tools.email_split(email)[0]
            # Escape special SQL characters in email_address to avoid invalid matches
            email_address = (email.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_'))
            email_brackets = "<%s>" % email_address

            _logger.warn("Using '%s' for partner matching", email_address)

            # Skip empty emails
            if not email_address:
                continue

            # Exact, case-insensitive match
            ids = partner_obj.search(
                cr, SUPERUSER_ID,
                [('email', '=ilike', email_address),
                 ('user_ids', '!=', False)],
                limit=1, context=context
            )

            if not ids:
                # If no match with addr-spec, attempt substring match within name-addr pair
                ids = partner_obj.search(
                    cr, SUPERUSER_ID,
                    [('email', '=ilike', email_brackets),
                     ('user_ids', '!=', False)],
                    limit=1, context=context
                )

            if not ids:
                _logger.warn("%s not found. Creating", email)
                partner_id = partner_obj.create(cr, uid, {'name': email_address, 'email': email})
                res.append(partner_id)

        return res

    def message_parse(self, cr, uid, message, save_original=False, context=None):
        res = super(mail_thread, self).message_parse(cr, uid, message, save_original, context=context)

        _logger.debug(context)
        _logger.debug(res)

        return res
    
    def message_new(self, cr, uid, msg_dict, custom_values=None, context=None):
        _logger.debug("self: %s" % self)
        _logger.debug("msg: %s" % msg_dict)
        _logger.debug("cust: %s" % custom_values)
        _logger.debug("ctx: %s" % context)

        return super(mail_thread, self).message_new(self, cr, uid, msg_dict, custom_values, context)
    
    def message_process(self, cr, uid, model, message, custom_values=None,
                        save_original=False, strip_attachments=False,
                        thread_id=None, context=None):

        _logger.debug("model: %s" % model)
        _logger.debug("msg: %s" % message)
        _logger.debug("cust: %s" % custom_values)
        _logger.debug("ctx: %s" % context)

        return super(mail_thread, self).message_process(cr, uid, model, message, custom_values, save_original, strip_attachments, thread_id, context)
