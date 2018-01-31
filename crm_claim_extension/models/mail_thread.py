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
        if res and res[0][0] == 'crm.claim':  # and not res[0][1]:
            # Could not match the claim with header information.
            # Trying to match by subject

            claim_number_re = re.compile("[#][0-9]{5,6}[: ]", re.UNICODE)
            number_re = re.compile("[0-9]+", re.UNICODE)

            message_subject = decode_header(message, 'Subject')
            match = claim_number_re.search(message_subject)
            claim_number = match and match.group(0)

            # No claim number
            if not claim_number:
                _logger.info('Could not find claim number from "%s"' % message_subject)
                return res

            # Strip everything but numbers
            claim_number = number_re.findall(claim_number)[0]
            claim_id = self.env['crm.claim'].sudo().search([
                ('claim_number', '=', claim_number)
                ],
                limit=1
            )

            # Can't recognize the claim number
            if not claim_id:
                _logger.info('Could not find a claim matching number "%s"' % claim_number)
                return res

            # Rewrite the res tuple
            lst = list(res[0])
            lst[1] = claim_id.id
            res[0] = tuple(lst)

            # Update CC:s
            current_cc_list = re.findall(r'[\w\.-]+@[\w\.-]+', claim_id.email_cc) if claim_id.email_cc else list()

            try:
                new_cc_list = re.findall(r'[\w\.-]+@[\w\.-]+', message_dict['cc']) if 'cc' in message_dict else list()
            except TypeError:
                _logger.warning("Could not find cc from message")
                new_cc_list = list()

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

        return res

    @api.model
    def _find_partner_from_emails(self, id, emails, model=None, check_followers=True):
        res = super(MailThread, self)._find_partner_from_emails(
            id=id,
            emails=emails,
            model=model,
            check_followers=check_followers,
        )

        CrmClaim = self.env['crm.claim']

        for email in emails:

            email_address = tools.email_split(email)[0]

            _logger.info("Using '%s' for partner matching", email_address)

            # Skip empty emails
            if not email_address:
                continue

            vals = dict()
            vals['email_from'] = email_address

            partner_id = CrmClaim._fetch_partner(vals)
            res.append(partner_id)

        return res
