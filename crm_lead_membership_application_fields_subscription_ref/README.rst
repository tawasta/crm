.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================================================
CRM Lead: Membership Application Subscription Reference
========================================================

* Adds the field "Subscription Invoice Reference" to the lead's Billing Info,
  e.g. to be filled in from a membership application website form.
* A quotation created from the lead gets the reference as its
  "Customer Reference".
* When the order is confirmed, the new subscription gets the order's
  Customer Reference, which is then shown on
  the subscription's invoices. This applies to all orders, also those not
  created from a lead.

Configuration
=============
\-

Usage
=====
* Fill in Subscription Invoice Reference on the lead and create a quotation
  with a subscription product from it. Confirm the quotation.

Known issues / Roadmap
======================
* A reference set explicitly on the subscription is kept.
* If the order's lines are added to an existing subscription (e.g. with
  ``subscription_use_existing_subscription``), its reference is not changed.
* Consider if future version of ``subscription_customer_reference`` module 
  could already handle passing the reference from SO to subscription.
  

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
