# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:
from openerp.addons.mail.mail_message import decode
from openerp import tools

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
_logger = logging.getLogger(__name__)


def decode_header(message, header, separator=' '):
    return separator.join(map(decode, filter(None, message.get_all(header, []))))


class MailThread(models.Model):
    
    # 1. Private attributes
    _inherit = 'mail.thread'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    @api.model
    def message_process(self, model, message, custom_values=None, save_original=False, strip_attachments=False,
                        thread_id=None):

        res = super(MailThread, self).message_process(
            model=model,
            message=message,
            custom_values=custom_values,
            save_original=save_original,
            strip_attachments=strip_attachments,
            thread_id=thread_id
        )

        return res

    # TODO: clean up this mess
    @api.model
    def message_route(self, message, message_dict, model=None, thread_id=None, custom_values=None):

        res = super(MailThread, self).message_route(message, message_dict, model, thread_id, custom_values)

        # Try matching by the claim number
        try:
            _logger.info(res)
            # A try-block if res is empty for some reason
            if res[0][0] == 'crm.claim' and not res[0][1]:
                # Could not match the claim with header information.
                # Trying to match by subject
                claim_number_re = re.compile("[#][0-9]{5,6}[: ]", re.UNICODE)
                number_re = re.compile("[0-9]+", re.UNICODE)

                message_subject = decode_header(message, 'Subject')

                match = claim_number_re.search(message_subject)

                claim_number = match and match.group(0)

                # Strip everything but numbers
                claim_number = number_re.search(claim_number).group(0)

                claim_id = self.env['crm.claim'].sudo().search(
                   [('claim_number', '=', claim_number)], limit=1
                )
                if claim_id:
                    # Rewrite the res tuple
                    lst = list(res[0])
                    lst[1] = claim_id.id
                    res[0] = tuple(lst)

                    # Update CC:s
                    current_cc_list = re.findall(r'[\w\.-]+@[\w\.-]+', claim_id.email_cc)
                    new_cc_list = re.findall(r'[\w\.-]+@[\w\.-]+', message_dict['cc']) if 'cc' in message_dict else False

                    # Compare current CC:s to new CC:s
                    new_cc_recipients = set(new_cc_list) - set(current_cc_list)

                    if new_cc_recipients:
                        new_cc_recipients_str = ", ".join(new_cc_list)
                        _logger.info('Adding %s to CC recipients', new_cc_recipients_str)

                        msg = "Adding '%s' to CC-recipients" % new_cc_recipients_str
                        claim_id.message_post(body=msg)

                        # Update CC recipients
                        claim_id.email_cc = ', '.join(set(current_cc_list + new_cc_list))

                    _logger.info('Matched a message "%s" to claim "#%s" using message subject', message_subject, claim_number)

        except Exception, e:
            # TODO: FIX "Error while matching a claim: expected string or buffer"

            _logger.warn('Error while matching a claim: %s', e)

        return res

    @api.model
    def _find_partner_from_emails(self, id, emails, model=None, check_followers=True):
        res = super(MailThread, self)._find_partner_from_emails(
            id=id,
            emails=emails,
            model=model,
            check_followers=check_followers,
        )

        for email in emails:
            partner_object = self.env['res.partner']
            email_address = tools.email_split(email)[0]

            # Escape special SQL characters in email_address to avoid invalid matches
            email_address = (email_address.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_'))
            email_brackets = "<%s>" % email_address

            _logger.info("Using '%s' for partner matching", email_address)

            # Skip empty emails
            if not email_address:
                continue

            # Exact, case-insensitive match
            ids = partner_object.sudo().search(
                [('email', 'ilike', email_address)],
                limit=1
            )

            if not ids:
                # If no match with addr-spec, attempt substring match within name-addr pair
                ids = partner_object.search(
                    [('email', 'ilike', email_brackets)],
                    limit=1
                )

            if not ids:
                _logger.warn("%s not found. Creating", email_address)
                partner_id = partner_object.create({'name': email_address, 'email': email})
                res.append(partner_id.id)

        return res

    # def message_parse(self, cr, uid, message, save_original=False, context=None):
    #     res = super(MailThread, self).message_parse(cr, uid, message, save_original, context=context)
    #
    #     _logger.debug(res)
    #
    #     return res
    #
    #
    # def message_new(self, cr, uid, msg_dict, custom_values=None, context=None):
    #     _logger.debug("self: %s" % self)
    #     _logger.debug("msg: %s" % msg_dict)
    #     _logger.debug("cust: %s" % custom_values)
    #
    #     return super(MailThread, self).message_new(self, cr, uid, msg_dict, custom_values, context)
    #
    #
    # def message_process(self, cr, uid, model, message, custom_values=None,
    #                     save_original=False, strip_attachments=False,
    #                     thread_id=None, context=None):
    #     _logger.debug("model: %s" % model)
    #     _logger.debug("msg: %s" % message)
    #     _logger.debug("cust: %s" % custom_values)
    #     _logger.debug("ctx: %s" % context)
    #
    #     return super(MailThread, self).message_process(cr, uid, model, message, custom_values, save_original,
    #                                                     strip_attachments, thread_id, context)
