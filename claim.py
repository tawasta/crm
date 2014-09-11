from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

class claim(osv.Model):      

    _inherit = 'crm.claim'
    
    ''' When the module is installed, fetch all claims without a number and assign them one '''
    def _init_claim_numbers(self, cr, uid, ids=None, context=None):

        search_filter = [('claim_number','=',False)]
        
        matches = self.search(cr, SUPERUSER_ID, args=search_filter,order='id')
        
        settings_model = self.pool.get('crm_claim.settings')
        
        claim_number = settings_model.browse(cr, SUPERUSER_ID, [1], context)[0].next_number
        for match in self.browse(cr, SUPERUSER_ID, matches, context):
            self.write(cr, SUPERUSER_ID, [match.id], {'claim_number': claim_number }, context)
            claim_number += 1

        ''' Update the highest number in the settings '''
        settings_model.write(cr, SUPERUSER_ID, [1], {'next_number': claim_number }, context)
        
        return True
    
    ''' When a claim is created, assign it a new claim number '''
    def create(self, cr, uid, vals, context=None):
        
        if not context:
            context = {}
        
        res = super(claim, self).create(cr, uid, vals, context)
        
        if self.browse(cr, uid, [res], context)[0]:
            write_vals = {'claim_number': self._get_claim_number(cr) }
            super(claim, self).write(cr, uid, [res], write_vals, context)
    
        return res
        
    def _get_claim_number(self, cr):
            settings_model  = self.pool.get('crm_claim.settings')   
            crm_model  = self.pool.get('crm_customer_account_number_gen.settings')
            
            crm_number = crm_model.browse(cr, SUPERUSER_ID, [1])[0].next_number
            _logger.warning( crm_number )
            
            claim_number = settings_model.browse(cr, SUPERUSER_ID, [1])[0].next_number
            _logger.warning( claim_number ) 
            
            ''' Bump number in settings by one '''
            settings_model.write(cr, SUPERUSER_ID, [1], {'next_number': claim_number+1 })
            
            return claim_number        
                
    _columns = {
        'claim_number': fields.char('#'),
    }
    
    _sql_constraints = [
        ('claim_number', 'unique(claim_number)', _('This claim number is already in use.'))
    ]
    