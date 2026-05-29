##############################################################################
#
#    Author: Futural Oy
#    Copyright 2025 Futural Oy (https://futural.fi)
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
    "name": "CRM Lead Map View",
    "summary": "Add map view for CRM leads",
    "version": "17.0.1.0.0",
    "category": "CRM",
    "website": "https://github.com/tawasta/crm",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["crm", "partner_map_view"],
    "data": ["views/map_view.xml"],
    "assets": {
        "web.assets_backend": [
            "crm_lead_map_view/static/src/js/crm_lead_map_arch_parser.esm.js",
            "crm_lead_map_view/static/src/js/crm_lead_map_controller.esm.js",
            "crm_lead_map_view/static/src/js/crm_lead_map_model.esm.js",
            "crm_lead_map_view/static/src/js/crm_lead_map_renderer.esm.js",
            "crm_lead_map_view/static/src/js/crm_lead_map_view.esm.js",
            "crm_lead_map_view/static/src/views/*.xml",
        ],
    },
    "demo": [],
}
