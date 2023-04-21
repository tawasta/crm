##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019- Oy Tawasta OS Technologies Ltd. (http://www.tawasta.fi)
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

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class CrmLead(models.Model):

    # 1. Private attributes
    _inherit = "crm.lead"

    # 2. Fields declaration
    activity_date_deadline_all = fields.Date(
        string="Activities Deadline",
        help="Activities deadline for all users",
        compute="_compute_activity_date_deadline_all",
        search="_search_activity_date_deadline_all",
        compute_sudo=False,
        readonly=True,
        store=False,
        groups="base.group_user",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends("activity_ids.date_deadline")
    @api.depends_context("uid")
    def _compute_activity_date_deadline_all(self):
        todo_activities = []
        if self.ids:
            todo_activities = self.env["mail.activity"].search(
                [("res_model", "=", self._name), ("res_id", "in", self.ids)],
                order="date_deadline ASC",
            )

        for record in self:
            record.activity_date_deadline_all = next(
                (
                    activity.date_deadline
                    for activity in todo_activities
                    if activity.res_id == record.id
                ),
                False,
            )

    def _search_activity_date_deadline_all(self, operator, operand):
        return [("activity_ids.date_deadline", operator, operand)]

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
