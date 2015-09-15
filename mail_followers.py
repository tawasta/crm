from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class mail_followers(osv.Model):
    _inherit = 'mail.followers'
