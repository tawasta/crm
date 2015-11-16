# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Jarmo Kortetjärvi
#    Copyright 2015 Oy Tawasta OS Technologies Ltd.
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Lead to Sale',
    'category': 'CRM',
    'version': '8.0.0.3.0',
    'author': 'Oy Tawasta Technologies Ltd.',
    'website': 'http://www.tawasta.fi',
    'depends': [
        'sale_crm',
        'sale_order_description',
    ],
    'description': '''
Lead to Sale
--------------------------

Adds a relation between lead and sale

''',
    'data': [
        'views/crm_lead_form.xml',
        'views/sale_order_form.xml',
    ],
}
