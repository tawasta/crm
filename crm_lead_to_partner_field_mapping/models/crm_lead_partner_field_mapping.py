from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

# These build the partner hierarchy, so the code sets them
STRUCTURE_PARTNER_FIELDS = ["parent_id", "is_company", "type"]
# Core names the company and the contact person, but an invoice address
# gets its name only from a mapping
NAMED_PARTNER_PROTECTED_FIELDS = STRUCTURE_PARTNER_FIELDS + ["name"]
UNSUPPORTED_FIELD_TYPES = ["one2many", "properties", "reference", "many2one_reference"]


class CrmLeadPartnerFieldMapping(models.Model):
    _name = "crm.lead.partner.field.mapping"
    _description = "Lead to Partner Field Mapping"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    lead_field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Lead Field",
        required=True,
        ondelete="cascade",
        domain=[
            ("model", "=", "crm.lead"),
            ("ttype", "not in", UNSUPPORTED_FIELD_TYPES),
        ],
    )
    partner_field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Partner Field",
        required=True,
        ondelete="cascade",
        domain=f"""[
            ("model", "=", "res.partner"),
            ("store", "=", True),
            ("readonly", "=", False),
            ("ttype", "not in", {UNSUPPORTED_FIELD_TYPES}),
            (
                "name",
                "not in",
                {STRUCTURE_PARTNER_FIELDS}
                if apply_to == "invoice"
                else {NAMED_PARTNER_PROTECTED_FIELDS},
            ),
        ]""",
    )
    apply_to = fields.Selection(
        selection=[
            ("both", "Company and Contact Person"),
            ("company", "Company"),
            ("contact", "Contact Person"),
            ("invoice", "Invoice Address"),
        ],
        required=True,
        default="both",
        help="Which partner created from the lead gets the value: "
        "the company, the contact person or both, or an invoice address "
        "created under the customer.",
    )

    @api.depends(
        "lead_field_id.field_description",
        "partner_field_id.field_description",
        "apply_to",
    )
    def _compute_display_name(self):
        apply_to_labels = dict(
            self._fields["apply_to"]._description_selection(self.env)
        )
        for mapping in self:
            mapping.display_name = (
                f"{mapping.lead_field_id.field_description} → "
                f"{mapping.partner_field_id.field_description} "
                f"({apply_to_labels.get(mapping.apply_to)})"
            )

    @api.model_create_multi
    def create(self, vals_list):
        self.env.registry.clear_cache()
        return super().create(vals_list)

    def write(self, vals):
        self.env.registry.clear_cache()
        return super().write(vals)

    def unlink(self):
        self.env.registry.clear_cache()
        return super().unlink()

    @api.model
    @tools.ormcache()
    def _get_active_mappings(self):
        """Return (lead field, partner field, apply to) name tuples"""
        # sudo: the cached result is shared by all users, and it only holds
        # field names configured by a sales manager
        mappings = self.sudo().search([])
        return tuple(
            (m.lead_field_id.name, m.partner_field_id.name, m.apply_to)
            for m in mappings
        )

    @api.constrains("lead_field_id", "partner_field_id", "apply_to")
    def _check_field_compatibility(self):
        # The field domains only guide the UI, so validate on the server too
        for mapping in self:
            error = mapping._get_field_incompatibility()
            if error:
                raise ValidationError(error)

    def _get_field_incompatibility(self):
        """Return an error message if the lead value can't be written to the
        partner field, otherwise False"""
        self.ensure_one()
        lead_field = self.lead_field_id
        partner_field = self.partner_field_id
        if lead_field.model != "crm.lead" or partner_field.model != "res.partner":
            return _("Map a lead field to a partner field.")
        if {lead_field.ttype, partner_field.ttype} & set(UNSUPPORTED_FIELD_TYPES):
            return _("Fields of this type can't be mapped.")
        # create() doesn't check field groups, so a restricted partner field
        # would be writable through the lead by any salesperson
        if self._is_restricted_field(lead_field) or self._is_restricted_field(
            partner_field
        ):
            return _("Fields restricted to user groups can't be mapped.")
        if (
            not partner_field.store
            or partner_field.readonly
            or partner_field.name in self._get_protected_partner_fields()
        ):
            return _(
                "The partner field %(field)s can't be written.",
                field=partner_field.field_description,
            )
        if (lead_field.ttype, lead_field.relation) != (
            partner_field.ttype,
            partner_field.relation,
        ):
            return _(
                "The fields %(lead_field)s and %(partner_field)s have "
                "different types.",
                lead_field=lead_field.field_description,
                partner_field=partner_field.field_description,
            )
        if lead_field.ttype == "selection":
            return self._get_selection_incompatibility()
        return False

    def _get_protected_partner_fields(self):
        self.ensure_one()
        if self.apply_to == "invoice":
            return STRUCTURE_PARTNER_FIELDS
        return NAMED_PARTNER_PROTECTED_FIELDS

    def _is_restricted_field(self, ir_field):
        # ir.model.fields doesn't store the groups, so read them from the
        # registry
        field = self.env[ir_field.model]._fields.get(ir_field.name)
        return not field or bool(field.groups)

    def _get_selection_incompatibility(self):
        # Read the values from the registry, because ir.model.fields doesn't
        # store dynamic selections
        lead_values = (
            self.env["crm.lead"]._fields[self.lead_field_id.name].get_values(self.env)
        )
        partner_values = (
            self.env["res.partner"]
            ._fields[self.partner_field_id.name]
            .get_values(self.env)
        )
        missing_values = set(lead_values) - set(partner_values)
        if not missing_values:
            return False
        return _(
            "The partner field %(field)s doesn't have the values: %(values)s",
            field=self.partner_field_id.field_description,
            values=", ".join(sorted(missing_values)),
        )
