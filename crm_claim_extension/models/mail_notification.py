# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models
from openerp import tools, _

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:
import logging
logger = logging.getLogger(__name__)


class MailNotification(models.Model):

    # 1. Private attributes
    _inherit = 'mail.notification'

    # 2. Fields declaration
    new_reply_stage = fields.Boolean("New reply stage", help="Claim will be returned to this stage on new message")

    # 3. Default methods
    @api.multi
    def get_partners_to_email(self,  message):
        notify_pids = super(MailNotification, self).get_partners_to_email(message=message)

        # Send helpdesk messages even if partner has notifications disable
        if message.model == "crm.claim":
            for notification in self:
                partner = notification.partner_id

                if partner.notify_email == 'none':
                    notify_pids.append(partner.id)

        return notify_pids

    @api.model
    def get_signature_footer(self, user_id, res_model=None, res_id=None, user_signature=True):
        # Removes the signature footer

        # This is not currently used at all
        res = super(MailNotification, self).get_signature_footer(
            user_id=user_id,
            res_model=res_model,
            res_id=res_id,
            user_signature=user_signature
        )

        return ''

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods


