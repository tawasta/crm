# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
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
    'summary': 'Improved lead to sale functionality',
    'category': 'CRM',
    'version': '8.0.0.4.2',
    'author': 'Oy Tawasta Technologies Ltd.',
    'website': 'http://www.tawasta.fi',
    'depends': [
        'crm_simplification',
        'sale_crm',
        'sale_order_description',
        'sale_simplification',
    ],
    'data': [
        'views/crm_lead_form.xml',
        'views/crm_lead_kanban.xml',
        'views/crm_lead_tree.xml',
        'views/sale_order_form.xml',
    ],
}
