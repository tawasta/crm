from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    company_registry = fields.Char()
    organization_year_established = fields.Integer("Year Established")
    organization_director_name = fields.Char("Director's Name")
    payer_name = fields.Char(
        help="Organization that pays the membership, if not paid by the applicant",
    )
    invoice_email = fields.Char("Invoicing E-mail")
    edicode = fields.Char()

    einvoice_operator_id = fields.Many2one(
        comodel_name="res.partner.operator.einvoice",
        string="eInvoice Operator",
        help="Provider for eInvoice documents",
    )

    # Names and selection keys match OCA partner_contact_birthdate and
    # partner_contact_gender, so the values map 1:1 to res.partner
    birthdate_date = fields.Date("Birthdate")
    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female"), ("other", "Other")],
    )
