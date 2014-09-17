# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2014- Vizucom Oy (http://www.vizucom.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'MMG Claim customizations',
    'category': 'Sales',
    'version': '0.2',
    'author': 'Vizucom Oy',
    'website': 'http://www.vizucom.com',
    'depends': ['crm_claim'],

    'description': """
Claims extension
=========================================
* Generates account numbers for all existing claims
* Starts from 10001 by default, can be customized in data XML file
* Keeps track of assigned numbers internally, and gives a new one each time a new claim is created
""",
    'data': [
        'view/claim_menu.xml',
        'view/claim_form_view.xml',
        'view/claim_tree_view.xml',
        'view/claim_reply_view.xml',
        'data/claim_number_init.xml',
    ],
}
