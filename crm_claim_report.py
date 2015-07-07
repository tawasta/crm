# -*- coding: utf-8 -*-
from openerp import models, api, fields
from openerp import tools

import logging
_logger = logging.getLogger(__name__)

AVAILABLE_PRIORITIES = [
   ('0', 'Low'),
   ('1', 'Normal'),
   ('2', 'High')
]

class CrmClaimReport(models.Model):
    
    _inherit = 'crm.claim.report'
    
    user_id = fields.Many2one('res.users', 'User', readonly=True)
    section_id = fields.Many2one('crm.case.section', 'Section', readonly=True)
    nbr_claims = fields.Integer('# of Claims', readonly=True)
    email = fields.Integer('# Emails', size=128, readonly=True)
    
    create_date = fields.Datetime('Create Date', readonly=True, select=True)
    claim_date = fields.Datetime('Claim Date', readonly=True)
    delay_close = fields.Float('Delay to close', digits=(16,2),readonly=True, group_operator="avg",help="Number of Days to close the case")
    date_closed = fields.Datetime('Close Date', readonly=True, select=True)
    date_deadline = fields.Date('Deadline', readonly=True, select=True)
    delay_expected = fields.Float('Overpassed Deadline',digits=(16,2),readonly=True, group_operator="avg")
    
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    stage_id = fields.Many2one ('crm.claim.stage', 'Stage', readonly=True)
    categ_id = fields.Many2one('crm.case.categ', 'Category',\
        domain="[('section_id','=',section_id),\
        ('object_id.model', '=', 'crm.claim')]", readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    
    priority = fields.Selection(AVAILABLE_PRIORITIES, 'Priority')
    sla = fields.Selection([('0', '-'),('1', 'Taso 1'), ('2', 'Taso 2'), ('3', 'Taso 3'), ('4', 'Taso 4')], 'Service level', readonly=True),

    
    type_action = fields.Selection([('correction','Corrective Action'),('prevention','Preventive Action')], 'Action Type')
    subject = fields.Char('Claim Subject', readonly=True)
    claim_number = fields.Char('Claim number', readonly=True)
    
    year_claim = fields.Integer('Claim year')
    month_claim = fields.Integer('Claim month')
    
    def _select(self):
        select_str = "SELECT "
        select_str += "min(c.id) as id"
        select_str += ",c.claim_number as claim_number"
        select_str += ",c.date as claim_date"
        select_str += ",c.date_closed as date_closed"
        select_str += ",c.date_deadline as date_deadline"
        select_str += ",c.user_id"
        select_str += ",c.stage_id"
        select_str += ",c.section_id"
        select_str += ",c.partner_id"
        select_str += ",c.company_id"
        select_str += ",c.categ_id"
        select_str += ",c.name as subject"
        select_str += ",count(*) as nbr_claims"
        select_str += ",c.sla as sla"
        select_str += ",c.priority as priority"
        select_str += ",c.type_action as type_action"
        select_str += ",c.create_date as create_date"
        select_str += ",avg(extract('epoch' from (c.date_closed-c.create_date)))/(3600*24) as delay_close, (SELECT count(id) FROM mail_message WHERE model='crm.claim' AND res_id=c.id) AS email,extract('epoch' from (c.date_deadline - c.date_closed))/(3600*24) as delay_expected"
        
        select_str += ",EXTRACT(YEAR FROM c.create_date) as year_claim"
        select_str += ",EXTRACT(MONTH FROM c.create_date) as month_claim"
        
        return select_str
    
    def _from(self):
        from_string = "crm_claim c"
        
        return from_string
    
    def _group_by(self):
        _group_by = "GROUP BY "
        _group_by += "c.date,"
        _group_by += "c.claim_number,"
        _group_by += "c.sla,"
        _group_by += "c.user_id,"
        _group_by += "c.section_id,"
        _group_by += "c.stage_id,"
        _group_by += "c.categ_id,"
        _group_by += "c.partner_id,"
        _group_by += "c.company_id,"
        _group_by += "c.create_date,"
        _group_by += "c.priority,"
        _group_by += "c.type_action,"
        _group_by += "c.date_deadline,"
        _group_by += "c.date_closed,"
        _group_by += "c.id"
        
        return _group_by
    
    def init(self, cr):
        # self._table = sale_report
        tools.drop_view_if_exists(cr, self._table)
        
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))