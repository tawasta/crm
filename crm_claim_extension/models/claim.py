from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID, tools
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)


class crm_claim(osv.Model):

    _inherit = 'crm.claim'
    _order = "write_date DESC"

    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}

        if vals.get('email_from'):
            vals['email_from_readonly'] = vals.get('email_from')

        # If partner doesn't exist, we'll need to create one
        if not vals.get('partner_id'):
            partner_vals = vals.copy()
            partner_vals['claim_autogenerated'] = True
            vals['partner_id'] = self._fetch_partner(
                cr, uid, partner_vals, context=context
            )
        res = super(crm_claim, self).create(cr, uid, vals, context)

        if self.browse(cr, uid, [res], context)[0]:
            fetchmail_server = self.pool.get('fetchmail.server').\
                browse(cr, uid, context.get('fetchmail_server_id'))

            if fetchmail_server:
                company_id = fetchmail_server.company_id.id
                reply_to = self._default_get_reply_to(cr, uid,
                                                      company_id=company_id)

                write_vals = {'company_id': company_id, 'reply_to': reply_to,
                              'user_id': False}

                super(crm_claim, self).write(cr, uid, [res], write_vals,
                                             context)

        # Remove the helpdesk email and its aliases from cc emails
        claim_instance = self.browse(cr, uid, res)
        if claim_instance.email_cc:
            email_list = claim_instance.email_cc.split(',')

            try:
                email_regex = re.compile("[<][^>]+[>]")
                email_raw = email_regex.findall(claim_instance.reply_to)[0]
                email_raw = re.sub(r'[<>]', "", email_raw)

                reply_to = email_raw

                exclude_list = self._get_exclude_list(
                    cr, uid, context, claim_instance.company_id.id
                ) + [reply_to]

                for exclude in exclude_list:
                    match = [s for s in email_list if exclude in s]

                    if match:
                        email_list.pop(email_list.index(match[0]))

                    match = False
                _logger.info("Email CC: %s", email_list)
                email_cc = ','.join(email_list)

                self.write(cr, uid, res, {'email_cc': email_cc})
            except Exception, e:
                _logger.error('Could not set email CC: %s', e)

        if vals.get('attachment_ids'):
            # Update attachment res_id so inline-added
            # attachments are matched correctly
            attachment_obj = self.pool.get('ir.attachment')
            try:
                attachments_list = vals.get('attachment_ids')[0][2]
                for attachment in attachments_list:
                    attachment_obj.write(cr, uid, attachment, {'res_id': res})
            except:
                attachments_list = []

            # Check if attachments are removed
            for attachment_id in attachment_obj.search(
                cr, SUPERUSER_ID, [('res_id', '=', res),
                                   ('res_model', '=', 'crm.claim')]
            ):
                if attachment_id not in attachments_list:
                    attachment_obj.unlink(cr, uid, res)

        self._claim_send_autoreply(cr, uid, res, context)

        return res

    def write(self, cr, uid, ids, values, context=None):
        # When a claim stage changes, save the date
        if values.get('email_from'):
            values['email_from_readonly'] = values.get('email_from')

        if values.get('stage_id'):
            stage_id = values.get('stage_id')

            if stage_id:
                values['stage_change_ids'] = [(0, _, {'stage': stage_id})]

            if stage_id == 2:
                # In progress
                values['date_start'] = datetime.now().replace(microsecond=0)
                if not self.browse(cr, uid, ids)[0].user_id:
                    values['user_id'] = uid
            if stage_id == 3:
                # Settled
                values['date_settled'] = datetime.now().replace(microsecond=0)
            if stage_id == 4:
                # Rejected
                values['date_rejected'] = datetime.now().replace(microsecond=0)
            if stage_id == 5:
                # Waiting
                values['date_waiting'] = datetime.now().replace(microsecond=0)

        if values.get('attachment_ids'):
            # Update attachment res_id so inline-added
            # attachments are matched correctly
            attachment_obj = self.pool.get('ir.attachment')
            try:
                attachments_list = values.get('attachment_ids')[0][2]
            except:
                attachments_list = []

            for attachment in attachments_list:
                if not attachment_obj.browse(cr, uid, attachment).res_id:
                    attachment_obj.write(
                        cr, SUPERUSER_ID, attachment,
                        {'res_id': self.browse(cr, uid, ids).id}
                    )

        if values.get('message_last_post'):
            stage_id = self.browse(cr, uid, ids).stage_id.id

            # Check if a closed ticket gets a new message.
            # If so, mark the ticket as new
            if stage_id in [3, 4]:
                values['stage_id'] = 1
                msg_body = _("Re-opening claim due to a new message.")
                self.message_post(cr, uid, ids, body=msg_body)
            elif stage_id in [6, 7]:
                values['stage_id'] = 5
                msg_body = _("Changing to assigned due to a new message..")
                self.message_post(cr, uid, ids, body=msg_body)

        if values.get('partner_id'):
            # Partner id is changed. Set the new partner as a follower
            self.message_unsubscribe(
                cr, uid, ids, [self.browse(cr, uid, ids).partner_id.id],
                context=context
            )
            self.message_subscribe(
                cr, uid, ids, [values.get('partner_id')], context=context
            )

        return super(crm_claim, self).write(cr, uid, ids, values, context=context)

    # Not implemented
    def action_rejected(self, cr, uid, ids, context=None):
        _logger.warn("Rejected")

        return super(crm_claim, self).action_rejected(cr, uid, context)

    # Not implemented
    def action_settled(self, cr, uid, ids, context=None):
        _logger.warn("Settled")

        return super(crm_claim, self).action_settled(cr, uid, context)

    # Not implemented
    def _onchange_stage_id(self, cr, uid, ids, stage_id, context):
        _logger.warn(stage_id)
        return True

    def _claim_send_autoreply(self, cr, uid, claim_id, context):
        # Checks if a partner is applicable for sending a mail
        claim = self.browse(cr, uid, claim_id)
        partner = claim.partner_id

        # All claims for the partner within the last 15 minutes
        timestamp_search = datetime.strftime(datetime.now() - relativedelta(minutes=15), '%Y-%m-%d %H:%M:%S')
        claims_count = self.search(cr, SUPERUSER_ID, [('partner_id', '=', partner.id),('stage_id', '=', 1), ('create_date', '>=', timestamp_search)], count=True)

        if claims_count > 3:
            _logger.warn("This partner has more than three new claims in last 15 minutes. Autoreply is disabled")
            msg_body = _("<strong>Autoreply was not sent.</strong>") + "<br/>"
            msg_body += _('This partner has more than three claims in the last 15 minutes.') + "<br/>" 
            msg_body += _('Sending autoreply is disabled for this partner to prevent an autoreply-loop.') + "<br/>" 
            msg_body += _('Please wait a while before creating new ticket, or mark some tickets as started.') + "<br/>" 
            self.message_post(cr, uid, [claim.id], body=msg_body)

            return False

        self._claim_created_mail(cr, uid, claim_id, context)
        return True

    def _claim_created_mail(self, cr, uid, claim_id, context, disabled=False):
        # Creates and sends a "claim created" mail to the partner
        claim = self.browse(cr, uid, claim_id)
        mail_message = self.pool.get('mail.message')
        values = {}

        subject = "#" + str(claim.claim_number) + ": " + claim.name
        email = claim.reply_to

        if not claim.description:
            claim.description = ''

        description = claim.description.replace('\n', '<br />').encode('ascii', 'ignore')

        # values['body'] = "<p style='font-weight: bold;'>" + subject + "</p>"
        values['body'] = "<p><span style='font-weight: bold;'>" + _("Received claim") + ":</span></p>"
        values['body'] += "<p><div dir='ltr' style='margin-left: 2em;'>" + str(description) + "</div></p>"

        values['record_name'] = subject
        values['subject'] = subject
        values['email_from'] = email
        values['reply_to'] = email

        values['res_id'] = claim.id
        values['model'] = claim.__class__.__name__
        values['type'] = 'email'
        values['subtype_id'] = 1

        if claim.attachment_ids:
            values['attachment_ids'] = [(6, 0, claim.attachment_ids.ids)]

        if claim.partner_id:
            self.message_subscribe(cr, uid, [claim.id], [claim.partner_id.id])

        context = {'default_model': 'crm.claim', 'default_res_id': claim_id}
        context['pre_header'] = "<strong>" + _("Your claim has been received.") + "</strong>"

        res = mail_message.create(cr, uid, values, context)

        return res

    def _default_get_value(self, cr, uid, value_name, context=None, company_id=None):
        return False

        if not company_id:
            company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id

        reply_ids=self.pool.get('crm_claim.reply').search(cr, SUPERUSER_ID,[('company_id', '=', company_id)])
        assert len(reply_ids) == 1, 'There should be only one settings instance for each company.'

        if reply_ids:
            reply_obj = self.pool.get('crm_claim.reply').browse(cr, SUPERUSER_ID,reply_ids)[0]
        else:
            _logger.warn('There were no settings for company %s', company_id)
            return False

        _logger.warn(reply_obj)
        _logger.warn(value_name)

        res = getattr(reply_obj, value_name, False)

        _logger.warn("Res: %", res)

        return res

    def _default_get_reply_to(self, cr, uid, context=None, company_id=None):
        if not company_id:
            company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id

        reply_ids = self.pool.get('crm_claim.reply').search(cr, uid, [('company_id', '=', company_id)])
        if reply_ids:
            reply_obj = self.pool.get('crm_claim.reply').browse(cr, uid, reply_ids)
            if reply_obj.reply_to:
                reply_to = reply_obj.reply_to
                return reply_to

        return False

    def _get_exclude_list(self, cr, uid, context=None, company_id=None):
        mail_ids = self._default_get_reply_alias_ids(cr, uid, context, company_id)

        res = []

        for mail_id in mail_ids:
            res.append(mail_id.name)

        return res

    def _default_get_reply_alias_ids(self, cr, uid, context=None, company_id=None):
        # return self._default_get_value(cr, uid, 'reply_alias_ids', context, company_id)
        if not company_id:
            company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id

        reply_object = self.pool.get('crm_claim.reply')

        reply_settings_id = reply_object.search(cr, uid, [('company_id', '=', company_id)])[0]

        if reply_settings_id:
            result = reply_object.browse(cr,SUPERUSER_ID,reply_settings_id).reply_alias_ids

            return result

        return False

    def _default_get_reply_header(self, cr, uid, context=None, company_id=None,):
        if not company_id:
            company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id

        reply_object = self.pool.get('crm_claim.reply')

        reply_settings_id = reply_object.search(cr, uid, [('company_id', '=', company_id)])

        if reply_settings_id:
            result = reply_object.browse(cr, uid, reply_settings_id[0]).header

            return result

        return False

    def _default_get_reply_footer(self, cr, uid, context=None, company_id=None,):
        if not company_id:
            company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id

        reply_object = self.pool.get('crm_claim.reply')
        reply_settings_id = reply_object.search(cr,uid,[('company_id', '=', company_id)])

        if reply_settings_id:
            result = reply_object.browse(cr, uid, reply_settings_id[0]).footer

            return result

        return False

    def _get_company(self, cr, uid, context=None):
        current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        res = current_user.company_id.id

        return res

    _defaults = {
        'sla': "1",
        'stage_id': 1,
        'reply_to': _default_get_reply_to,
        'company_id': _get_company
    }

    _sql_constraints = [
        ('claim_number', 'unique(claim_number)', _('This claim number is already in use.'))
    ]
