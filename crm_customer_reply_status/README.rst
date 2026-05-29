.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=========================
CRM Customer Reply Status
=========================
This module helps sales teams identify CRM leads that have received a new
customer reply.

The module marks a CRM lead as requiring attention when an incoming customer
email is posted on an existing lead. It also stores the latest customer reply
timestamp, shows the status in CRM views, and can optionally move the lead to a
configured CRM stage.

Features
========

* Mark CRM leads when a customer replies by email.
* Store the latest customer reply date on the lead.
* Show a ``Customer Replied`` badge in the CRM kanban view.
* Add a ``Customer Replied`` search filter.
* Allow configuring a CRM stage as the customer replied stage.
* Optionally notify sales team members by email.
* Reset the customer replied flag when a salesperson sends a chatter message to
  the customer.
* Ignore internal notes and system notifications.
* Ignore incoming emails that create a new lead, because they are new enquiries
  and not replies to existing leads.

Configuration
=============

Customer replied stage
----------------------

Go to CRM stages and enable ``Customer Replied Stage`` on the stage where leads
should be moved when an existing customer replies by email.

Only one stage should normally be configured for this purpose per relevant CRM
pipeline.

Notifications
-------------

Notifications are disabled by default.

To notify all members of a sales team when a customer replies:

#. Open the sales team.
#. Enable ``Notify Customer Replies``.

When this option is enabled on the sales team, it overrides member-specific
notification settings.

To notify only selected members:

#. Keep ``Notify Customer Replies`` disabled on the sales team.
#. Open the relevant sales team member records.
#. Enable ``Notify Customer Replies`` only for the members who should be
   notified.

Usage
=====

Incoming customer reply
-----------------------

When an incoming email is posted on an existing CRM lead:

* ``Customer Replied`` is set to true.
* ``Customer Reply Date`` is updated.
* The lead is moved to the CRM stage marked as ``Customer Replied Stage``, if
  such a stage is configured.
* A badge is shown in the CRM kanban view.
* The lead appears in the ``Customer Replied`` filter.
* Configured sales team members receive an email notification.
* A note is added to the chatter showing who was notified.

New incoming lead
-----------------

When an incoming email creates a new CRM lead, the module does not mark it as a
customer reply.

This is intentional: a new inbound email is treated as a new enquiry, not as a
reply to an existing lead.

Salesperson reply
-----------------

When a salesperson sends a chatter message to the customer, the module resets
``Customer Replied`` to false.

This means the lead no longer requires attention from the salesperson and is
again waiting for the customer's next reply.

Internal comments
-----------------

Internal notes and system notifications do not change the customer replied
status.

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
