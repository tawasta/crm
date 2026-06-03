import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class Lead(models.Model):
    _inherit = "crm.lead"

    customer_replied = fields.Boolean(
        readonly=True,
        copy=False,
        index=True,
    )

    customer_reply_date = fields.Datetime(
        readonly=True,
        copy=False,
        index=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        # Messages posted while creating a lead from an incoming email are part
        # of the initial enquiry. They must not be treated as a customer reply
        # to an existing lead.
        leads = super(
            Lead,
            self.with_context(skip_customer_reply_tracking=True),
        ).create(vals_list)

        return leads

    def message_post(self, *args, **kwargs):
        """Track customer replies and salesperson responses on CRM leads.

        The CRM chatter creates different ``mail.message`` records depending on
        the source of the message:

        * Incoming customer email:
          ``message_type == "email"``

        * Outgoing message sent from the chatter:
          ``message_type == "comment"`` with email recipients

        * Internal notes, notifications and system messages:
          ``message_type == "comment"`` / ``"notification"``

        The ``customer_replied`` flag is meant to be actionable:

        * ``True`` means the customer has replied and the lead needs attention.
        * ``False`` means the salesperson has answered and the lead is waiting
          for the customer again.
        """

        message = super().message_post(*args, **kwargs)

        if self.env.context.get("skip_customer_reply_tracking"):
            return message

        if (
            message.message_type == "comment"
            and message.partner_ids.filtered("email")
            and message.subtype_id == self.env.ref("mail.mt_comment")
        ):
            self.sudo().write(
                {
                    "customer_replied": False,
                }
            )

            return message

        if message.message_type != "email":
            return message

        previous_message_count = self.env["mail.message"].search_count(
            [
                ("model", "=", self._name),
                ("res_id", "in", self.ids),
                ("id", "!=", message.id),
            ]
        )

        if not previous_message_count:
            return message

        stage = self._stage_find(
            domain=[("customer_replied", "=", True)],
            limit=1,
        )

        vals = {
            "customer_replied": True,
            "customer_reply_date": (message.date or fields.Datetime.now()),
        }

        if stage:
            vals["stage_id"] = stage.id

        self.sudo().write(vals)

        for lead in self:
            if not lead.team_id:
                continue

            if lead.team_id.customer_reply_notify:
                members = lead.team_id.crm_team_member_ids
            else:
                members = lead.team_id.crm_team_member_ids.filtered(
                    "customer_reply_notify"
                )

            partners = members.mapped("user_id.partner_id").filtered("active")

            if not partners:
                continue

            lead.message_post(
                body=_("Customer reply email notification sent to: %s")
                % ", ".join(partners.mapped("display_name")),
                message_type="comment",
                subtype_xmlid="mail.mt_note",
            )

            lead.with_context(
                mail_notify_force_send=True,
            ).message_notify(
                partner_ids=partners.ids,
                subject=_("Customer has replied to CRM lead: %s") % lead.display_name,
                body=_("Customer has replied to this CRM lead."),
                email_layout_xmlid="mail.mail_notification_layout",
            )

        return message
