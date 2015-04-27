# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015- Vizucom Oy (http://www.vizucom.com)
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
    'name': 'Partner Address Customizations',
    'category': 'CRM',
    'version': '0.1',
    'author': 'Vizucom Oy',
    'website': 'http://www.vizucom.com',    
    'depends': ['crm', 'sale_business_id', 'crm_customer_account_number_gen'],
    'description': '''
* Simplifies res_partner address types
* Simplifies adding addresses
* Breaks res_partner addresses to multiple notebook pages
* Changes res_partner address views from kanban to row
''',
    'data': [
        'view/res_partner_form.xml',
        'view/res_partner_form_contact.xml',
        'view/res_partner_form_einvoice.xml',
        'view/res_partner_tree.xml',
        'view/res_partner_menu.xml',
    ],
}
