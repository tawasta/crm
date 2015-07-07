# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2015 - Oy Tawasta Technologies Ltd. (http://www.tawasta.fi)
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
    'name': 'CRM Claim Extension Reports',
    'category': 'CRM',
    'version': '0.1',
    'author': 'Oy Tawasta Technologies Ltd.',
    'website': 'http://www.tawasta.fi',
    'depends': ['crm_claim_extension'],
    'description': '''
CRM Claim Extension Reports
--------------------------

Overwrites the default claim reports, as they are just plain wrong with exteneded claims


Features
--------
* None Yet

''',
    'data': [
        'report/crm_claim_report.xml',
        'report/crm_claim_report_search.xml',
    ],
}
