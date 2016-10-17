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
        model = self._context.get('default_model')
        if not model:
            model = self._context.get('default_res_model')

        if model and model == 'crm.claim':
            # Only send custom messages for claim model message instances

            # Always create a notification
            if 'notification' not in values and values.get('mail_message_id'):
                values['notification'] = True

            res_id = self._context.get('default_res_id')

            claim_model = self.env['crm.claim']
            claim_instance = claim_model.sudo().browse([res_id])

            # Get message header from reply_to settings
            header = claim_model._default_get_reply_header(company_id=claim_instance.company_id.id)

            # Get message footer from reply_to settings
            footer = claim_model._default_get_reply_footer(company_id=claim_instance.company_id.id)

            # If we have a message to show before header,
            # it can be set in context.
            # E.g. "Your claim has been received" before header
            if self._context.get('pre_header'):
                if not header:
                    header = ''
                header = self._context.get('pre_header') + "<br/>" + header

            # Get message recipients from claim
            values['reply_to'] = claim_instance.reply_to
            values['email_from'] = claim_instance.reply_to
            values['email_cc'] = claim_instance.email_cc

            # Message subject
            values['record_name'] = "#" + str(claim_instance.claim_number) + ": " + str(claim_instance.name)
            values['subject'] = values['record_name']

            # A "static" header that's fetched from company-spesific settings
            static_header = "<p><small>" + str(header) + "</small></p><hr style='margin: 1em 0 1em 0;'/>"
            static_header += '<p>#' + str(claim_instance.claim_number) + ": " + str(claim_instance.name) + "</p>"
            static_header += '<p>'

            # The body_html is in html-format. We'll replace the heading <p>-tag with our own header
            values['body_html'] = re.sub(r'(^<p>)', static_header, values['body_html'])

            # Start the footer
            values['body_html'] += "<p><small>"
            values['body_html'] += "--<br/>"

            if 'mail_message_id' in values:
                # Add message history to claim replies

                # Get the message instance
                message_model = self.env['mail.message']
                message_instance = message_model.sudo().browse([values.get('mail_message_id')])

                # Get message history from parent and grandparent (lower levels shouldn't exists on claims)
                mail_parent_id = message_instance.parent_id.id
                mail_grandparent_id = message_instance.parent_id.parent_id.id if \
                    message_instance.parent_id.parent_id.id \
                    else mail_parent_id

                message_child_ids = message_model.sudo().search(
                    ['|',
                     ('parent_id', '=', mail_parent_id),
                     ('parent_id', '=', mail_grandparent_id),
                     ('subtype_id', '=', 1),
                     ('id', '!=', message_instance.id),
                     ('parent_id', '!=', False)
                     ]
                )

                # Write a html-formatted messages history from previous message thread messages
                messages_history = '<div dir="ltr" style="color: grey;">'

                # Get users timezone
                tz = pytz.timezone(self.env['res.users'].browse([self._uid]).partner_id.tz) or pytz.utc

                # Indentation level
                level = 1

                for child_message in message_child_ids:
                    # Format child messages with incementing indentation
                    # TODO: Should we use '>' for indentation instead of CSS?
                    message_date = pytz.utc.localize(
                        datetime.datetime.strptime(child_message.date, '%Y-%m-%d %H:%M:%S')
                    ).astimezone(tz)

                    level += 1
                    messages_history += "<div style='padding-left: %sem;'>" % level
                    messages_history += "<p>" + message_date.strftime('%d.%m.%Y %H:%M:%S') + ", " +\
                                        child_message.email_from + " :</p>"
                    messages_history += child_message.body
                    messages_history += "</div>"

                messages_history += '</div>'

                # Don't sign the message with sender name, if the message was sent by admin (e.g. automatic messages)
                if message_instance.create_uid.id != 1:
                    values['body_html'] += str(message_instance.create_uid.partner_id.name)
                    values['body_html'] += "<br/>"
                values['body_html'] += str(footer)
                values['body_html'] += "</small></p>"

                # Include messages history on the bottom of the message,
                # under a horizontal line
                values['body_html'] += "<hr style='margin: 1em 0 1em 0;' />"
                values['body_html'] += messages_history
                values['body_html'] += "<br/>"

            elif res_id:
                values['body_html'] += str(footer)
                values['body_html'] += "</small></p>"

        return super(MailMail, self).create(values)

    # 7. Action methods

    # 8. Business methods
    # @api.multi
    # def send(self, auto_commit=False, raise_exception=False):
    #     for record in self:
    #         super(MailMail, self).send(auto_commit=auto_commit, raise_exception=raise_exception)
