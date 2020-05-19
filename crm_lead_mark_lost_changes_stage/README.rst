.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================================
CRM Lead - Use an appropriate stage with Mark Lost-button
=========================================================

Override Mark Lost-button to search stage that has 0.00 Probability as an
attribute. Lead's contemporary stage changes to searched stage.

Configuration
=============
Configure a stage accordingly to use this module successfully.

Usage
=====
Select a lead and click on Mark Lost-button.
There has to be a stage with these attributes:

- Folded in Pipeline: True
- Change Probability Automatically: True
- Probability: 0.00

If some of the values in this list is missing, this module will show and error
message.

Known issues / Roadmap
======================
To be safe, only have one existing stage that has values listed above. That way
the search domain will select one stage at maximum.

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@tawasta.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
