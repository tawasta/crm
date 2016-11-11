# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class CrmClaim(models.Model):
    
    # 1. Private attributes
    _inherit = 'crm.claim'

    # 2. Fields declaration
    swkb_installations = fields.Many2many(
        'software_knowledge_base.installation',
        'swkb_installation_claim_relation',
        string='Installations',
        domain=lambda self: self.compute_swkb_installations_domain(),
        default=lambda self: self._get_default_swkb_installations(),
    )

    # 3. Default methods
    def _get_default_swkb_installations(self):
        # If partner is a support person for only one installation, use that
        context = self._context

        if self.partner_id:
            partner_id = self.partner_id.id
        elif 'params' in context and 'id' in context['params']:
            claim = self.browse([context['params']['id']])
            partner_id = claim.partner_id.id
        else:
            return list()

        installation = self.swkb_installations.search([('technical_contact_ids', '=', partner_id)])

        if len(installation) == 1:
            return installation.ids

    # 4. Compute and search fields, in the same order that fields declaration
    @api.depends('partner_id')
    def compute_swkb_installations_domain(self):
        # Search installations in which the person is a contact person, or the installation belongs to the company
        context = self._context
        partners = list()

        if self.partner_id:
            partner = self.partner_id.id
            partners.append(partner)
        elif 'params' in context and 'id' in context['params']:
            claim = self.browse([context['params']['id']])

            partner = claim.partner_id.id
            partners.append(partner)

            if claim.partner_id.parent_id:
                partners.append(claim.partner_id.parent_id.id)
        else:
            return list()

        domain = ['|', ('partner_ids', 'in', partners), ('technical_contact_ids', '=', partner)]
        print domain

        return domain

    # 5. Constraints and onchanges

    # TODO: update installations on partner change
    # @api.onchange('partner_id')
    # def onchange_partner_id_update_swkb_installations(self):
    #     if not self.swkb_installations:
    #         installations = self._get_default_swkb_installations()
    #         self.swkb_installations = installations
    #         return {'value': {'swkb_installations': installations}}

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
