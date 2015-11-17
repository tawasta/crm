# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Jarmo Kortetjärvi
#    Copyright 2015 Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

{
    'name': 'CRM Simplification',
    'version': '8.0.0.4.20',
    'category': 'CRM',
    'website': 'http://www.tawasta.fi',
    'author': 'Oy Tawasta Technologies Ltd.',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'crm',
        'crm_address_simplification',
        'crm_customer_account_number_gen',
        'sale_business_id',
        'sale_business_id_extension',
        'sale_crm',
    ],
    'data': [
        'views/res_partner_form.xml',
        'views/res_partner_form_contact.xml',

        'views/crm_lead_form.xml',
        'views/crm_lead_menu.xml',
        'views/crm_lead_search.xml',

        'views/crm_opportunity_form.xml',
        'views/crm_make_sale_form.xml',

        'views/crm_lead_convert_to_opportunity_form.xml',
    ],
}
