from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    def _claim_count(self, cr, uid, ids, field_name, arg, context=None):
        Claim = self.pool['crm.claim']
        
        for partner in self.browse(cr, uid, ids, context=context):  
            # Get child company partners
            child_ids = self.search(cr, uid,[('parent_id', '=', partner.id)], limit=None)
        
        return {
            partner_id: Claim.search_count(cr,uid, ['|', ('partner_id', '=', partner_id), ('partner_id', 'in', child_ids)], context=context)
            for partner_id in ids
        }

    _columns = {
        'claim_count': fields.function(_claim_count, string='# Claims', type='integer'),
    }