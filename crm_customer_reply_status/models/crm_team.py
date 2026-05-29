from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    customer_reply_notify = fields.Boolean(
        string="Notify Customer Replies",
        help=(
            "If enabled, all members of this sales team are notified when "
            "a customer replies to a CRM lead. This overrides member-specific "
            "notification settings."
        ),
    )


class CrmTeamMember(models.Model):
    _inherit = "crm.team.member"

    customer_reply_notify = fields.Boolean(
        string="Notify Customer Replies",
        help=(
            "Notify this member when a customer replies to a CRM lead. "
            "Ignored if customer reply notification is enabled on the sales team."
        ),
    )
