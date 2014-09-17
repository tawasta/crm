from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

class mail_message(osv.Model):
    """ Update of mail_message class, to restrict mail access. """
    _inherit = 'mail.message'

    def create(self, cr, uid, values, context=None):
        if context is None:
            context = {}
        model = context.get('default_model')
        if model and model=='crm.claim':
            res_id =  context.get('default_res_id')
            claim = self.pool[model].browse(cr,uid,res_id)
            if 'reply_to' not in values:
                values['reply_to'] = claim.reply_to if claim.reply_to else False

        newid = super(mail_message, self).create(cr, uid, values, context)
        _logger.warning("Created mail %s", newid)
    
        return newid