# -*- coding: utf-8 -*-
from openerp import api, fields, models


class CrmClaimStage(models.Model):
    _inherit = 'crm.claim.stage'

    # TODO: rename "closed". The point of this is to mark which claim stages should be reverted back to the
    # "new reply stage" when new message arrives (waiting for customer, completed, cancelled, etc.
    closed = fields.Boolean(
        string='Inactive stage',
        help='This stage is not in support persons "todo", list. E.g. completed or waiting for customer',
    )

    # This is the stage to which tickets in "closed" stage should be moved
    # TODO: this should obviously be constrained to a single stage
    new_reply_stage = fields.Boolean(
        string='New reply stage',
        help='Claim will be returned to this stage on new message',
    )
