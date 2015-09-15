from openerp.osv import osv, fields
from openerp.tools.translate import _


class ClaimStageChange(osv.Model):

    _name = 'crm.claim.stage.change'
    _rec_name = 'stage'

    _order = 'create_date DESC'

    _columns = {
        'stage': fields.many2one('crm.claim.stage', _('New stage')),
        'claim_id': fields.many2one('crm.claim', _('Claim id')),
    }
