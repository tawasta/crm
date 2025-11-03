import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class MailActivity(models.Model):
    _inherit = "mail.activity"

    high_priority = fields.Boolean()
