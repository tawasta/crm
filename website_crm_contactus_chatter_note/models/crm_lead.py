# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo import tools  # html_escape

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model_create_multi
    def create(self, vals_list):
        leads = super().create(vals_list)

        # Yritetään tunnistaa "Contact Us" -peräiset liidit
        website_medium = self.env.ref('utm.utm_medium_website', raise_if_not_found=False)
        website_medium_id = website_medium.id if website_medium else False

        # Käydään syntyneet liidit läpi (tuettu myös massaluontiin)
        for lead, vals in zip(leads, vals_list):
            try:
                # Tarkistus sekä arvoista että lopullisesta kentästä (varmistaa toimivuuden myös
                # jos medium_id puuttuu valsista mutta täyttyy oletuksella/onchangella).
                is_from_website = (
                    (vals.get('medium_id') and vals.get('medium_id') == website_medium_id)
                    or (lead.medium_id and lead.medium_id.id == website_medium_id)
                )

                if not is_from_website:
                    continue

                # Aihe ja sisältö Contact Us -lomakkeelta:
                # Odoon vakiossa "name" toimii aiheena ja "description" sisältönä.
                subject = (vals.get('name') or lead.name or _("Yhteydenotto")).strip()
                content = (vals.get('description') or lead.description or "").strip()

                # Kirjoitetaan siisti HTML-chatteriin
                body = "<p><strong>Aihe:</strong> {}</p><p>{}</p>".format(
                    tools.html_escape(subject),
                    tools.html_escape(content).replace("\n", "<br/>")
                )

                # --- UUSI: varmista, että vastuuhenkilö "Watch" / seuraaja on päällä ---
                pid = lead.user_id.partner_id.id if lead.user_id and lead.user_id.partner_id else False
                if pid:
                    # lisää seuraajaksi jos ei jo seuraa
                    lead.message_subscribe(partner_ids=[pid])

                # Korvattu: message_post -> message_notify
                lead.message_notify(
                    body=body,
                    subject=False,
                    partner_ids=[pid] if pid else [],
                    email_layout_xmlid='mail.mail_notification_light',
                    notify_by_email=False,
                )
            except Exception:
                # Ei kaadeta liidin luontia, vaikka postaus epäonnistuisi.
                continue

        return leads
