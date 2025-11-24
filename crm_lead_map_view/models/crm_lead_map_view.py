from odoo import fields, models


class View(models.Model):
    """
    Extends the base "ir.ui.view" model to include a new type of view
    called "CRM Lead Map".
    """

    _inherit = "ir.ui.view"
    type = fields.Selection(selection_add=[("CRMLeadMapView", "CRM Lead Map")])


class IrActionsActWindowView(models.Model):
    """
    Extends the base "ir.actions.act_window.view" model to include
    a new view mode called "CRM Lead Map".
    """

    _inherit = "ir.actions.act_window.view"
    view_mode = fields.Selection(
        selection_add=[("CRMLeadMapView", "CRM Lead Map")],
        ondelete={"CRMLeadMapView": "cascade"},
    )
