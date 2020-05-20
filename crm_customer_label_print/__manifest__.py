##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2016 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    'name': 'Customer address labels',
    'summary': 'Customer address labels print 3x8 without margins',
    'version': '8.0.0.2.4',
    'category': 'CRM',
    'website': 'https://github.com/Tawasta/crm',
    'author': 'Oy Tawasta Technologies Ltd.',
    'license': 'AGPL-3',
    'application': False,
    'installable': False,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'crm',
        'report',
    ],
    'data': [
        'report/paperformat_european_a4_nomargin.xml',
        'report/res_partner.xml',
        'report/res_partner_address_labels.xml',
    ],
    'demo': [
    ],
}
