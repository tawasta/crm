from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    is_distributor_partner = fields.Boolean(string="Is a Distributor Partner")

    distributor_partner_opportunity_count = fields.Integer(
        string="Distributor Partner Opportunity Count",
        compute="_compute_distributor_partner_opportunity_count",
    )

    distributor_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Distributor Partner",
        domain=[("is_distributor_partner", "=", True)],
        help="""The distributor partner responsible for this Customer""",
    )

    # Note that this does not fetch all the child partners and tally
    # the opportunity counts together
    def _compute_distributor_partner_opportunity_count(self):

        for partner in self:
            partner.distributor_partner_opportunity_count = self.env[
                "crm.lead"
            ].search_count([("distributor_partner_id", "=", partner.id)])

    # Launch the CRM pipeline view
    def action_view_distributor_partner_opportunities(self):
        self.ensure_one()
        action = self.env.ref("crm.crm_lead_action_pipeline").read()[0]

        # Modify the domain to show only distributor partner's opportunities
        action["domain"] = [
            ("type", "=", "opportunity"),
            ("distributor_partner_id", "=", self.id),
        ]

        # Modify the context to not use "search_default_assigned_to_me" filter
        action["context"] = {"default_type": "opportunity"}

        return action
