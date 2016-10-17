# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

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
            # TODO: Get rid of this hack.
            # For some reason the author_id is False
            # if a new partner was created
            if not vals.get('author_id'):
                # TODO: This doesn't seem to do anything?
                email_from = vals.get('email_from')
                email_regex = re.compile("[<][^>]+[>]")

                try:
                    email = email_regex.findall(email_from)[0]
                    email = re.sub(r'[<>]', "", email)
                except IndexError, e:
                    logger.warn(e)

                vals['author_id'] = self.get_author_by_email(vals)

            # Add claim number to the first post
            if 'subject' in vals and vals['subject'] and not re.match('[#][0-9]+', vals['subject']):
                vals['subject'] = "#" + self.env[model].browse([vals['res_id']]).claim_number + ": " + vals['subject']

        return super(MailMessage, self).create(vals)

    # 7. Action methods

    # 8. Business methods
    @api.model
    def get_author_by_email(self, vals):
        # Try to get an author (i.e. partner) by email address
        email_from = vals.get('email_from')
        email_regex = re.compile("[<][^>]+[>]")

        try:
            email = email_regex.findall(email_from)[0]
            email = re.sub(r'[<>]', "", email)
        except IndexError, e:
            logger.warn(e)
            email = False

        author = self.env['res.partner'].search(
            [('email', '=', email)]
        )

        res = author[0] if author else False

        return res


