# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo import tools  # kept for potential future use; not used directly here
import logging
from markupsafe import Markup, escape

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Backend-only extension for crm.lead create():
        - Detects leads originating from the website (utm.utm_medium_website).
        - Builds a translatable subject line including the sender's name and lead title.
        - Posts a single light-layout chatter entry (mail.mail_notification_light).
        - Renders the body safely using Markup/escape (line breaks -> <br/>).
        - Keeps logging minimal (INFO on success/failure).

        Notes:
        - The same subject_line is shown in the chatter body after the "Subject:" label,
        as requested.
        """
        leads = super().create(vals_list)

        website_medium = self.env.ref('utm.utm_medium_website', raise_if_not_found=False)
        website_medium_id = website_medium.id if website_medium else False

        for lead, vals in zip(leads, vals_list):
            try:
                # Process only website-originated leads
                v_mid = vals.get('medium_id')
                l_mid = lead.medium_id.id if lead.medium_id else None
                if not ((v_mid and v_mid == website_medium_id) or (l_mid and l_mid == website_medium_id)):
                    continue

                # Use values directly from the created record
                lead_title = (lead.name or "").strip()
                content = (lead.description or "").strip()
                sender_name = (lead.contact_name or "").strip()

                # Translatable subject line used both as email/chatter subject AND in the body
                subject_line = _("Subject: %(title)s — Sender: %(name)s", title=lead_title, name=sender_name)

                # Safe HTML body (preserve line breaks)
                content_html = Markup("<br/>").join(escape(content).split("\n"))
                body = Markup("<p><strong>{label}</strong> {subject_line}</p><p>{content}</p>").format(
                    label=escape(_("Subject:")),
                    subject_line=escape(subject_line),
                    content=content_html,
                )

                # Notify the record's responsible partner and keep a chatter entry
                pid = lead.user_id.partner_id.id if lead.user_id and lead.user_id.partner_id else False
                if not pid:
                    continue

                msg = lead.message_post(
                    body=body,
                    subject=subject_line,
                    partner_ids=[pid],
                    subtype_xmlid='mail.mt_note',
                    email_layout_xmlid='mail.mail_notification_light',
                )
                _logger.info("CONTACT-US: lead_id=%s chatter_msg_id=%s", lead.id, getattr(msg, "id", None))

            except Exception as e:
                _logger.info("CONTACT-US: lead_id=%s failed: %s", lead.id if lead else None, e)
                continue

        return leads
