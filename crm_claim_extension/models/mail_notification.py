from openerp.osv import osv, fields

import logging
_logger = logging.getLogger(__name__)


class mail_notification(osv.Model):
    _inherit = 'mail.notification'

    def get_partners_to_email(self, cr, uid, ids, message, context=None):
        notify_pids = super(mail_notification, self).get_partners_to_email(cr, uid, ids, message, context)

        ''' Send helpdesk messages even if partner has notifications disabled '''
        if message.model == "crm.claim":
            for notification in self.browse(cr, uid, ids, context=context):
                partner = notification.partner_id

                if partner.notify_email == 'none':
                    notify_pids.append(partner.id)

        return notify_pids
