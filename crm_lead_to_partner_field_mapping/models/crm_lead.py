from odoo import models


class Lead(models.Model):
    _inherit = "crm.lead"

    def _create_customer(self):
        customer = super()._create_customer()
        self._create_mapped_invoice_address(customer)
        return customer

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        values = super()._prepare_customer_values(partner_name, is_company, parent_id)
        partner_type = "company" if is_company else "contact"
        values.update(self._get_mapped_partner_values(partner_type))
        return values

    def _create_mapped_invoice_address(self, customer):
        """Create an invoice address under the customer, if the lead has
        values for the invoice address mappings"""
        values = self._get_mapped_partner_values("invoice")
        if not values:
            return self.env["res.partner"]
        values.update(parent_id=customer.id, type="invoice")
        return self.env["res.partner"].create(values)

    def _get_mapped_partner_values(self, partner_type):
        """Return the configured lead field values for a new partner

        :param partner_type: "company", "contact" or "invoice"
        """
        self.ensure_one()
        partner_fields = self.env["res.partner"]._fields
        mappings = self.env["crm.lead.partner.field.mapping"]._get_active_mappings()
        values = {}
        for lead_field_name, partner_field_name, apply_to in mappings:
            if not self._is_mapping_applied(apply_to, partner_type):
                continue
            # A field removed from the registry must not block partner creation
            lead_field = self._fields.get(lead_field_name)
            if not lead_field or partner_field_name not in partner_fields:
                continue
            value = self[lead_field_name]
            # Keep the value prepared by core instead of overwriting it with
            # an empty one
            if not value:
                continue
            values[partner_field_name] = lead_field.convert_to_write(value, self)
        return values

    def _is_mapping_applied(self, apply_to, partner_type):
        # "Both" covers the company and the contact person, not the invoice
        # address
        if apply_to == "both":
            return partner_type != "invoice"
        return apply_to == partner_type
