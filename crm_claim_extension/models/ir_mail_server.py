# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class IrMailServer(models.Model):

    # 1. Private attributes
    _inherit = 'ir.mail_server'

    # 2. Fields declaration

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None,
        smtp_port=None, smtp_user=None, smtp_password=None,
        smtp_encryption=None, smtp_debug=False):
        # Send a BCC message to an address every time a mail is sent.
        # This is for debugging purposes

        # Get TO-recipients as a list
        current_to_list = list(set(re.findall(r'[\w\.-]+@[\w\.-]+', message['To'])))
        new_to_list = list()
        user_to_list = list()

        users_model = self.env['res.users']
        for email_addess in current_to_list:
            # ilike is a bit risky, but we are using it to match
            # "Some Guy <some.guy@mail.com>" with "some.guy@gmail.com"
            if len(current_to_list) == 1 and users_model.search([('partner_id.email', 'ilike', email_addess)]):
                # TODO: a noreply address
                noreply_address = 'noreply' + re.search("@[\w.]+", message['Reply-to']).group()
                noreply_string = "Reply-To: %s\n" % noreply_address

                del message['Cc']
                del message['Reply-To']
                message['Reply-To'] = noreply_string

        # Set a BCC recipient
        del message['Bcc']
        message['Bcc'] = "odoo@tawasta.fi"

        return super(IrMailServer, self).send_email(
            message=message,
            mail_server_id=mail_server_id,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password,
            smtp_encryption=smtp_encryption,
            smtp_debug=smtp_debug
        )