.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================
Distributor/Sales Partner for leads
===================================

* Enables linking Leads/Opportunities to a Distributor/Sales Partner, in addition to the standard Salesperson
* Note: Distributor/Sales Partners are intended to be external persons outside of the company, and they are not
  expected to have user accounts in Odoo.

  * An example use case is that Leads from foreign countries come in 
    through the Odoo Website, and then the company's internal Salesperson marks them to be handled by 
    that specific country's external Distributor/Sales Partner
  

Configuration
=============
* In Contacts, check the new "Is Sales Partner?" field for all relevant partners. These partners
  become selectable in Sales Partner fields of Leads/Opportunities.
* (optional) In Contacts, for Customers, set the "Sales Partner" selection field value, to be able to filter
  customer lists based on the Distributor/Sales Partner they are linked to

Usage
=====
* In Lead/Opportunity form view, use the new dropdown menu to select a Sales Partner
* In Partner form view, use the new "Sales Partner Leads" action button to reach
  a pipeline view showing that Distributor's/Sales Partner's Leads/Opportunities.


Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------
* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
