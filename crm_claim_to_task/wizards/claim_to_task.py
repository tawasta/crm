# -*- coding: utf-8 -*-

# 1. Standard library imports:
import re

# 2. Known third party imports:
from bs4 import BeautifulSoup

# 3. Odoo imports (openerp):
from openerp import api, fields, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class ClaimToTask(models.TransientModel):
    
    # 1. Private attributes
    _name = 'claim.to.task'

    # 2. Fields declaration
    partner = fields.Many2one('res.partner', 'Partner')
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    user = fields.Many2one('res.users', 'User')
    project = fields.Many2one('project.project', 'Project', required=True)

    # 3. Default methods
    @api.model
    def default_get(self, fields):
        res = super(ClaimToTask, self).default_get(fields)

        active_id = self._context['active_id']

        claim = self.env['crm.claim'].browse([active_id])

        # Replace possible br-elements with line breaks
        description = re.sub('<br\s*[\/]?>', '\n', claim.description or '')

        res['user'] = self._uid
        res['name'] = claim.name
        # Strip possible html elements
        res['description'] = BeautifulSoup(description, 'lxml').text
        res['partner'] = claim.partner_id.id

        return res

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def create_task(self):
        self.ensure_one()
        context = self._context

        values = {
            'project_id': self.project.id,
            'partner_id': self.partner.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user.id or False,
        }

        task = self.env['project.task'].create(values)

        if 'active_id' in context:
            active_id = context['active_id']
            self.env['crm.claim'].browse([active_id]).write({'task': task.id})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.task',
            'target': 'current',
            'res_id': task.id,
            'type': 'ir.actions.act_window',
        }

    # 8. Business methods
