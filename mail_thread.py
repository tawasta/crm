from openerp.osv import osv
import logging
_logger = logging.getLogger(__name__)

class mail_thread(osv.Model):
    _inherit = 'mail.thread'

    def x_message_new(self, cr, uid, msg_dict, custom_values=None, context=None):
        _logger.warn("self: %s" % self)
        _logger.warn("msg: %s" % msg_dict)
        _logger.warn("cust: %s" % custom_values)
        _logger.warn("ctx: %s" % context)

        return super(mail_thread, self).message_new(self, cr, uid, msg_dict, custom_values, context)

    def x_message_process(self, cr, uid, model, message, custom_values=None,
                        save_original=False, strip_attachments=False,
                        thread_id=None, context=None):
        
        _logger.warn("model: %s" % model)
        _logger.warn("msg: %s" % message)
        _logger.warn("cust: %s" % custom_values)
        _logger.warn("ctx: %s" % context)
    
        return super(mail_thread, self).message_process(cr, uid, model, message, custom_values, save_original, strip_attachments, thread_id, context)