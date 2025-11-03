.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================
CRM: 'High Priority Activities' Flag for Leads
==============================================

* Enables flagging leads' activities with a simple "High Priority"
  boolean

Configuration
=============
* None needed

Usage
=====
* Create a new activity for a lead, and check the 
  High Priority Box

Known issues / Roadmap
======================
* Meeting activities do not currently support the flag
* 'social' repo contains a similar module 
  'mail_activity_high_priority_flag' that affects all
  models that inherit from the mail.activity.mixin (not just leads). It
  is currently flagged as uninstallable as it had some issues
  initializing the data on large installations.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
