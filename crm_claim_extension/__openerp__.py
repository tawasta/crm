# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
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
    'name': 'CRM Claims extension',
    'summary': 'Improved claims with helpdesk-like functionality',
    'category': 'Sales',
    'version': '8.0.0.9.5',
    'author': 'Oy Tawasta Technologies Ltd.',
    'website': 'http://www.tawasta.fi',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'crm_claim',
        'fetchmail',
    ],
    'data': [
        'data/claim_number_init.xml',
        'data/crm_claim_data.xml',

        'security/claim_security.xml',
        'security/ir.model.access.csv',

        'views/claim_css.xml',

        'views/claim_form_view.xml',
        #'views/claim_tree_view.xml',
        'views/crm_claim_stage_form.xml',

        'views/claim_menu.xml',
        'views/claim_reply_view.xml',
        'views/claim_search_view.xml',
        'views/fetchmail_server_form_view.xml',
        'views/res_partner_form_view.xml',
    ],
}
