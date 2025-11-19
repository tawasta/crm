from odoo import fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    company_registry = fields.Char()
    organization_year_established = fields.Integer("Year Established")
    organization_director_name = fields.Char("Director's Name")
    invoice_email = fields.Char("Invoicing E-mail")
    edicode = fields.Char()

    einvoice_operator_id = fields.Many2one(
        comodel_name="res.partner.operator.einvoice",
        string="eInvoice Operator",
        help="Provider for eInvoice documents",
    )
