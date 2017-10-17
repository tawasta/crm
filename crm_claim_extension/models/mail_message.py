# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
logger = logging.getLogger(__name__)


class MailMessage(models.Model):

    # 1. Private attributes
    _inherit = 'mail.message'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def create(self, vals):
        model = vals.get('model')

        if model and model == 'crm.claim':

            if 'email_from' in vals:
                author = self.env[model]._fetch_partner(vals)
                if author:
                    vals['author_id'] = author
                else:
                    vals['author_id'] = False

            real_author = False

            if 'subject' in vals and vals['subject'] and not re.match('.*[#][0-9]{5,6}.*', vals['subject']):
                claim = self.env[model].browse([vals['res_id']])

                # Add claim number to the first post
                vals['subject'] = _('Claim') + " #" + claim.claim_number + ": " + vals['subject']

                # Add "claim received"-message
                real_author = vals.get('author_id')

                if not real_author:
                    real_author = claim.partner_id.id

                vals = claim.get_claim_received_vals(vals)

                if claim.attachment_ids:
                    vals['attachment_ids'] = [(6, 0, claim.attachment_ids.ids)]

                if claim.partner_id:
                    claim.message_subscribe([claim.partner_id.id])

        res = super(MailMessage, self).create(vals)

        if model and model == 'crm.claim' and real_author:
            # Change the "claim received" sender.
            # We can't do this before posting or the sender won't receive the mail,
            # as the sender and recipient would be the same
            res.author_id = real_author

        return res

    # 7. Action methods

    # 8. Business methods
    @api.model
    def get_author_by_email(self, email_from):
        # Try to get an author (i.e. partner) by email address
        email_regex = re.compile("[\w\.-]+@[\w\.-]+")

        try:
            email_match = email_regex.findall(email_from)
            if email_match:
                email_from = email_match[0]
                email_from = re.sub(r'[<>]', "", email_from)
        except IndexError, e:
            logger.warn(e)

        author = False
        if email_from:
            author = self.env['res.partner'].search(
                [('email', '=ilike', email_from)],
                limit=1,
            )

        res = author if author else False

        return res


