# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re
import sys
import pytz
import datetime
import logging

_logger = logging.getLogger(__name__)

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import SUPERUSER_ID, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class MailMail(models.Model):

    # 1. Private attributes
    _inherit = 'mail.mail'

    reload(sys)
    sys.setdefaultencoding('utf8')

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods
    @api.model
    def create(self, values):
        model = False

        if 'mail_message_id' in values:
            mail_message = self.env['mail.message'].browse([values['mail_message_id']])
            model = mail_message.model
            res_id = mail_message.res_id

        # Only send custom messages for claim model message instances
        if model and model == 'crm.claim' and res_id:
            # Always create a notification
            if 'notification' not in values and values.get('mail_message_id'):
                values['notification'] = True

            claim_model = self.env['crm.claim']
            claim_instance = claim_model.sudo().browse([res_id])

            if not 'author_id' in values and 'email_from' in values:
                author = self.env['mail.message'].get_author_by_email(values['email_from'])
                if author:
                    values['author_id'] = author.id

            # Incoming message. Skip all this
            if 'author_id' in values:
                return super(MailMail, self).create(values)

            # Get message header from reply_to settings
            header = claim_model._default_get_reply_header(company_id=claim_instance.company_id.id)

            # Get message footer from reply_to settings
            footer = claim_model._default_get_reply_footer(company_id=claim_instance.company_id.id)

            # This is the first message to the claim. Add a notification before the header
            if len(claim_instance.message_ids) <= 3:
                if not header:
                    header = ''

                header = "<strong>" + _("Your claim has been received.") + "</strong>" + "<br/>" + header

            # Get message recipients from claim
            values['reply_to'] = claim_instance._get_reply_to()
            values['email_from'] = claim_instance.reply_to
            values['email_cc'] = claim_instance.email_cc

            # Message subject
            values['record_name'] = _('Claim') + " #" + str(claim_instance.claim_number) + ": " + str(claim_instance.name)
            values['subject'] = values['record_name']

            # A "static" header that's fetched from company-specific settings
            static_header = "<p><small>" + str(header) + "</small></p><hr style='margin: 1em 0 1em 0;'/>"
            static_header += '<p>#' + str(claim_instance.claim_number) + ": " + str(claim_instance.name) + "</p>"
            static_header += '<p>'

            # The body_html is in html-format. We'll replace the heading <p>-tag with our own header
            values['body_html'] = re.sub(r'(^<p>)', static_header, values['body_html'])

            # Start the footer
            values['body_html'] += "<p><small>"
            values['body_html'] += "--<br/>"

            if 'mail_message_id' in values:
                # Get the message instance
                MailMessage = self.env['mail.message']
                message_instance = MailMessage.sudo().browse([values.get('mail_message_id')])

                # Add message description to the bottom
                description = '<div dir="ltr" style="color: grey;">'
                description += '<div style="padding-left: 1em;">'
                description += claim_instance.description
                description += '</div>'
                description += '</div>'

                # Don't sign the message with sender name,
                # if the message was sent by admin (e.g. automatic messages)
                if message_instance.create_uid.id != SUPERUSER_ID:
                    values['body_html'] += str(message_instance.create_uid.partner_id.name)
                    values['body_html'] += "<br/>"
                values['body_html'] += str(footer)
                values['body_html'] += "</small></p>"

                # Include message description on the bottom of the message,
                # under a horizontal line
                values['body_html'] += "<hr style='margin: 1em 0 1em 0;' />"
                values['body_html'] += description
                values['body_html'] += "<br/>"

            elif res_id:
                values['body_html'] += str(footer)
                values['body_html'] += "</small></p>"

            if not res_id:
                values['recipient_ids'] = []

        return super(MailMail, self).create(values)

    # 7. Action methods

    # 8. Business methods
