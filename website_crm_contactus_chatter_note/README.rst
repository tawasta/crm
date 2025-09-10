.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

==================================
website_crm_contactus_chatter_note
==================================

When a lead is created from the website Contact Us form, this module posts a
single **light-layout** chatter message to the lead, addressed to the assigned
salesperson. The subject is **translatable** and includes both the **lead title**
and the **sender’s name**. The message body is rendered safely with preserved
line breaks.

Configuration
=============
- Ensure the standard Contact Us flow is enabled (module ``website_crm``).
- Set **Website → Configuration → Contact Form** defaults so leads get an **assigned salesperson** (``user_id``).
- Make sure **UTM** is available (dependency ``utm``) so website-originated leads carry ``utm_medium = website``.
- (Optional) Add translations for the strings **“Subject:”** and **“Sender:”** via *Settings → Translations*.


Usage
=====
- A visitor submits the **Contact Us** form on the website.
- A lead is created and this module posts one chatter message:
  - **Subject:** ``Subject: <lead title> — Sender: <name>`` (translatable)
  - **Body:** repeats the subject and includes the message content with line breaks preserved.
- The message is addressed to the assigned salesperson and uses the **light** email layout.


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
        :alt: Futural Oy
        :target: https://futural.fi/

This module is maintained by Futural Oy
