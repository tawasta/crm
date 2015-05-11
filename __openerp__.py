# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015- Oy Tawasta Technologies Ltd. (http://www.tawasta.fi)
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
    'author': 'Oy Tawasta Technologies Ltd.',
    'website': 'http://www.tawasta.fi',
    'depends': ['crm', 'sale_business_id', 'crm_customer_account_number_gen'],
    'description': '''
* Simplifies partner types to 'contact', 'delivery' and 'invoice'
* Adds notebook pages for each partner type
* Simpilfies adding partners by type directly from according notebook pages
* Changes default partner views from kanban to row
* Adds full name hierarchy to display name
''',
    'data': [
        'view/res_partner_form.xml',
        'view/res_partner_form_contact.xml',
        'view/res_partner_form_einvoice.xml',
        #'view/res_partner_tree.xml',
        'view/res_partner_menu.xml',
    ],
}
