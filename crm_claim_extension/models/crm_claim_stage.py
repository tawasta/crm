# -*- coding: utf-8 -*-
from openerp import api, fields, models


class CrmClaimStage(models.Model):
    _inherit = 'crm.claim.stage'

    # TODO: waiting, closed, etc. should be selection or One2many
    # Same stage should be allowed to be waiting AND closed

    # The point of this is to mark which claim stages should be reverted
    # back to the "new reply stage" when new message arrives
    # (waiting for customer, completed, cancelled, etc.
    waiting = fields.Boolean(
        string='Waiting',
        help='Claims in this stage are waiting for customer or third party',
    )
    closed = fields.Boolean(
        string='Closed',
        help='Claims in this stage are closed, e.g. completed or cancelled',
    )

    # This is the stage to which tickets in "closed" stage should be moved
    # TODO: this should obviously be constrained to a single stage
    new_reply_stage = fields.Boolean(
        string='New reply stage',
        help='Claim will be returned to this stage on new message',
    )
