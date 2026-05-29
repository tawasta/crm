import logging

from odoo import _, fields, models

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

    def message_post(self, *args, **kwargs):
        """Track customer replies and salesperson responses on CRM leads.

        The CRM chatter creates different `mail.message` records depending on
        what happened:

        * Incoming email from the customer:
          `message_type == "email"`

        * Outgoing message sent from the chatter to recipients:
          `message_type == "comment"` with email recipients

        * Internal notes and system notifications:
          `message_type == "comment"` / `"notification"` without being a
          customer reply event

        The goal is to keep `customer_replied` as an actionable flag:

        * True  = the customer has replied and the lead needs attention.
        * False = the salesperson has answered, so we are waiting for the
          customer again.
        """
        message = super().message_post(*args, **kwargs)

        # A chatter message sent to partners with email addresses means the
        # salesperson has replied to the customer. Reset the actionable flag.
        #
        # Internal notes must not reset the flag. They normally do not have
        # external email recipients in `message.partner_ids`.
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

        # Only incoming email messages represent customer replies. Other
        # chatter entries, notes and notifications are ignored.
        if message.message_type != "email":
            return message

        # When an incoming email creates a brand-new lead, it is a new enquiry,
        # not a reply to an existing CRM lead. In that case we leave the flag
        # untouched.
        previous_message_count = self.env["mail.message"].search_count(
            [
                ("model", "=", self._name),
                ("res_id", "in", self.ids),
                ("id", "!=", message.id),
            ]
        )

        if not previous_message_count:
            return message

        # A CRM stage can be marked as the target stage for customer replies.
        # If no such stage is configured, the lead is still marked as replied;
        # only the automatic stage move is skipped.
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

            # Team-level setting overrides member-level settings:
            # if enabled on the team, notify all team members.
            if lead.team_id.customer_reply_notify:
                members = lead.team_id.crm_team_member_ids
            else:
                members = lead.team_id.crm_team_member_ids.filtered(
                    "customer_reply_notify"
                )

            partners = members.mapped("user_id.partner_id").filtered("active")

            if not partners:
                continue

            # Leave an audit trail in the chatter so users can see who was
            # notified about the customer reply.
            lead.message_post(
                body=_("Customer reply email notification sent to: %s")
                % ", ".join(partners.mapped("display_name")),
                message_type="comment",
                subtype_xmlid="mail.mt_note",
            )

            # Send an explicit email notification. This avoids relying only on
            # Discuss inbox notifications, which users may miss.
            lead.with_context(
                mail_notify_force_send=True,
            ).message_notify(
                partner_ids=partners.ids,
                subject=_("Customer has replied to CRM lead: %s") % lead.display_name,
                body=_("Customer has replied to this CRM lead."),
                email_layout_xmlid="mail.mail_notification_layout",
            )

        return message
