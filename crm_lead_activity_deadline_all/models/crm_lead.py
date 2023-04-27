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
from odoo.osv import expression

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

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Override to support ordering on activity_date_deadline_all"""
        if count or not order or "activity_date_deadline_all" not in order:
            return super().search(
                args, offset=offset, limit=limit, order=order, count=count
            )
        order_items = [
            order_item.strip().lower()
            for order_item in (order or self._order).split(",")
        ]

        # Perform a read_group on all activities to get a mapping lead_id / deadline
        # Remember date_deadline is required, we always have a value for it. Only
        # the earliest deadline per lead is kept.
        activity_asc = any(
            "activity_date_deadline_all asc" in item for item in order_items
        )
        all_lead_activities = self.env["mail.activity"].read_group(
            [("res_model", "=", self._name)],
            ["res_id", "date_deadline:min"],
            ["res_id"],
            orderby="date_deadline ASC",
        )
        all_lead_mapping = {
            item["res_id"]: item["date_deadline"] for item in all_lead_activities
        }
        all_lead_ids = list(all_lead_mapping.keys())
        all_lead_domain = expression.AND([[("id", "in", all_lead_ids)], args])
        all_lead_order = ", ".join(
            item for item in order_items if "activity_date_deadline_all" not in item
        )

        # Search leads linked to those activities and order them. See docstring
        # of this method for more details.
        search_res = super().search(
            all_lead_domain, offset=0, limit=None, order=all_lead_order, count=count
        )
        all_lead_ids_ordered = sorted(
            search_res.ids,
            key=lambda lead_id: all_lead_mapping[lead_id],
            reverse=not activity_asc,
        )
        # keep only requested window (offset + limit, or offset+)
        all_lead_ids_keep = (
            all_lead_ids_ordered[offset : (offset + limit)]
            if limit
            else all_lead_ids_ordered[offset:]
        )
        # keep list of already skipped lead ids to exclude them from future search
        all_lead_ids_skip = (
            all_lead_ids_ordered[: (offset + limit)] if limit else all_lead_ids_ordered
        )

        # do not go further if limit is achieved
        if limit and len(all_lead_ids_keep) >= limit:
            return self.browse(all_lead_ids_keep)

        # Fill with remaining leads. If a limit is given, simply remove count of
        # already fetched. Otherwise keep none. If an offset is set we have to
        # reduce it by already fetch results hereabove. Order is updated to exclude
        # activity_date_deadline_all when calling super() .
        lead_limit = (limit - len(all_lead_ids_keep)) if limit else None
        if offset:
            lead_offset = max((offset - len(search_res), 0))
        else:
            lead_offset = 0
        lead_order = ", ".join(
            item for item in order_items if "activity_date_deadline_all" not in item
        )

        other_lead_res = super().search(
            expression.AND([[("id", "not in", all_lead_ids_skip)], args]),
            offset=lead_offset,
            limit=lead_limit,
            order=lead_order,
            count=count,
        )
        return self.browse(all_lead_ids_keep) + other_lead_res

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
