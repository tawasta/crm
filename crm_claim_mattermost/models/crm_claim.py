# -*- coding: utf-8 -*-
import os
from subprocess import call

from openerp import api, fields, models
from openerp.exceptions import ValidationError
from openerp import _

class CrmClaim(models.Model):

    _inherit = 'crm.claim'

    @api.model
    def create(self, values):
        res = super(CrmClaim, self).create(values)

        res.mattermost_claim_created()

        return res

    @api.multi
    def write(self, values):
        res = super(CrmClaim, self).write(values)

        for record in self:
            if 'user_id' in values:
                record.mattermost_claim_author_changed()

            if 'stage_id' in values:
                record.mattermost_claim_stage_changed()

        return res

    def mattermost_claim_created(self):
        if self.name and self.partner_id:
            msg = 'A new claim **%(subject)s** from **%(partner)s**' \
                  % {'subject': self.name, 'partner': self.partner_id.display_name}

            return self.mattermost_send_message(_(msg))

    def mattermost_claim_author_changed(self):
        msg = '**%(user)s** assigned **%(name)s** to **%(author)s**' \
              % {'user': self.uid.name, 'name': self.name, 'author': self.user_id.name}

        return self.mattermost_send_message(_(msg))

    def mattermost_claim_stage_changed(self):
        msg = '**%(user)s** changed **%(name)s** stage to **%(stage)s**' \
              % {'user': self.uid.name, 'name': self.name, 'stage': self.stage_id.name}

        return self.mattermost_send_message(_(msg))

    def mattermost_send_message(self, message):
        company = self.company_id

        if not company.mattermost_active:
            # Mattermost claim integration is not set
            return False

        # Validate variables
        validation_error = self.validate_variables()
        if validation_error:
            raise ValidationError(validation_error)

        vars = {
            'login_id': company.mattermost_login_id,
            'password': company.mattermost_password,
            'team': company.mattermost_team,
            'channel': company.mattermost_channel,
            'url': company.mattermost_url,
            'port': company.mattermost_port,
            'basepath': company.mattermost_basepath,
            'scheme': company.mattermost_scheme,
            'verify': company.mattermost_verify,
            'message': message,
        }

        # This could be done smarter
        file_path = os.path.abspath(__file__)
        models_path = os.path.dirname(file_path)
        module_path = os.path.dirname(models_path)
        script_path = '%s/ext/mattermost_send.py' % module_path

        cmd = 'python3 %(script)s "%(vars)s"' % {'script': script_path, 'vars': vars}
        call(cmd, shell=True)

    def validate_variables(self):
        # TODO: actual validation for each variable and custom error messages
        company = self.company_id
        error_msg = False

        if not company.mattermost_login_id:
            error_msg = 'Invalid login id'
        elif not company.mattermost_password:
            error_msg = 'Missing password'
        elif not company.mattermost_team:
            error_msg = 'Invalid team'
        elif not company.mattermost_channel:
            error_msg = 'Invalid channel'
        elif not company.mattermost_url:
            error_msg = 'Invalid url'
        elif not company.mattermost_port:
            error_msg = 'Invalid port'
        elif not company.mattermost_basepath:
            error_msg = 'Invalid path'
        elif not company.mattermost_scheme:
            error_msg = 'Invalid scheme'

        return error_msg
