# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:
from openerp.addons.mail.mail_message import decode

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
    def message_route(self, message, message_dict, model=None, thread_id=None, custom_values=None):

        res = super(MailThread, self).message_route(message, message_dict, model, thread_id, custom_values)

        # Try matching by the claim number
        try:
            # A try-block if res is empty for some reason
            if res[0][0] == 'crm.claim' and not res[0][1]:

                # Could not match the claim with header information.
                # Trying to match by subject
                claim_number_re = re.compile("[#][0-9]{5,6}[: ]", re.UNICODE)
                number_re = re.compile("[0-9]+", re.UNICODE)

                message_subject = decode_header(message, 'Subject')
                match = claim_number_re.search(message_subject)

                claim_number = match and match.group(0)
                # Strip all but numbers
                claim_number = number_re.search(claim_number).group(0)

                claim_id = self.env['crm.claim'].sudo().search(
                   [('claim_number', '=', claim_number)]
                )

                # Rewrite the res tuple
                lst = list(res[0])
                lst[1] = claim_id[0]
                res[0] = tuple(lst)
                _logger.info('Matched a message "%s" to claim "#%s" using message subject', message_subject, claim_number)

        except Exception, e:
            # TODO: FIX "Error while matching a claim: expected string or buffer"

            _logger.warn('Error while matching a claim: %s', e)

        return res