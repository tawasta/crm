.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
CRM Lead: Configurable Field Mapping to Partner
===============================================

* Copies configured lead fields to a new partner created from the lead,
  e.g. with "New Quotation" > "Create a new customer". Existing partners
  are never changed.
* Each mapping targets the parent company, the contact person itself, 
  both, or an invoice address. Invoice address mappings create an invoice address
  under the person. This can be used when an organization is paying a membership
  and you want to store it under the contact person in the hierarchy.

Configuration
=============
* Configure the mapping via CRM > Configuration > Customer Creation > Lead to Partner Fields.
* Mapped fields must be of the same type. Empty lead values are not
  copied, and a mapped value overrides the value set by core.
* To manage Company IDs for the invoice addresses, you can install
  ``l10n_fi_company_registry_invoice_addresses_are_companies``. Its
  "Suggest Company Invoice Address" setting also preselects that address
  on quotations.

Usage
=====
* Create new customers from lead after having configured the mappings.

Known issues / Roadmap
======================
\-

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
