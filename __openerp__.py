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
    'name': 'CRM Token key management',
    'category': 'CRM',
    'version': '0.1',
    'author': 'Futurable Oy',
    'website': 'http://futurable.fi',
    'depends': ['crm'],
    'description': '''
* A simple token key management
''',
    'data': [
        'view/crm_tokenkey_menu.xml',
        'view/crm_tokenkey_form.xml',
        'view/crm_tokenkey_tree.xml',
    ],
}
