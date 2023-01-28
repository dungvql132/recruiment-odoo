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

class SetOnBoardRRApplicant(models.TransientModel):
    _name = "wizard.set.onboad.rr"
    _description = "Set On Board RR Applicant"

    rr_applicant_id = fields.Many2one(comodel_name='recruitment.request.applicant',
                                       string='RR Applicant')
    on_board_date = fields.Date(string='On Board Date',required=True)

    def set_onboard(self):
        self.rr_applicant_id.on_board_date = self.on_board_date
        self.rr_applicant_id.stage_id = self.env.ref('my_recruitment.stage_on_board').id