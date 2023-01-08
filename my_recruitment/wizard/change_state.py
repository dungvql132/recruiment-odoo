from odoo import api, fields, models, _

class ChangeStateRR(models.TransientModel):
    _name = "wizard.change.state.rr"
    _description = "Change State RR"

    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    state = fields.Selection(selection=[('opening', 'Opening'), ('pending', 'Pending'),
                                        ('close', 'Close')], string='State', default='opening',required=True)
    reason_change_state = fields.Char(string='Reason', required=True)

    def change_state(self):
        self.recruitment_request_id.sudo().write({
            'state': self.state,
            'reason_change_state': self.reason_change_state
        })