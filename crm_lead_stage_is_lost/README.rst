.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
CRM: 'Is Lost Stage?' Field for Stages
======================================

* Adds a 'Is Lost Stage?' field to CRM stages and provides the following functionality:

  * Limits only one stage to have the 'Is Lost Stage?' enabled at a time
  * When Mark as Lost is clicked, move the opportunity to the configured lost stage
  * When an opportunity's stage changes to the configured lost stage, either via the button
    or by dragging in pipeline, calculate its Days to Close (date created --> to current date),
    and archive it so it gets the "Lost" ribbon
  

Configuration
=============
* Go to CRM -> Configuration -> Stages, select the stage you use as the lost stage,
  and check the new Is Lost Stage? checkbox

Usage
=====
* In pipeline view, either click the Mark as Lost button or drag the opportunity
  to the configured lost stage.


Known issues / Roadmap
======================
* Consider supporting multiple lost stages (e.g. different ones per sales team)

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
