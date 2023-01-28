from odoo import api, fields, models, _

class WizardCreateRRAplicant(models.TransientModel):
    _name = "wizard.create.rr.meeting"
    _description = "Create RR Meeting"

    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    rr_applicant_id = fields.Many2one(comodel_name='recruitment.request.applicant', string='RR Applicant')
    interviewer_ids = fields.Many2many(comodel_name='hr.employee', relation='interviewer_employee_wizard_rel',
                                       string='Interviewer', required=True)
    interview_date = fields.Datetime(string='Interview Date', required=True)

    @api.onchange('recruitment_request_id')
    def change_recruitment_request_id(self):
        reviewing_draft_id = self.env.ref('my_recruitment.stage_reviewing').id
        if self.recruitment_request_id:
            all_accept_rr_applicant = self.recruitment_request_id.rr_applicant_ids.filtered(
                lambda x: x.stage_id.id == reviewing_draft_id
            )
            return {
                'domain': {
                    'rr_applicant_id': [
                        ('id', 'in', all_accept_rr_applicant.ids),
                        ('id', 'not in', self.recruitment_request_id.interview_meeting_ids.mapped('rr_applicant_id.id'))
                    ]}
            }

    @api.onchange('rr_applicant_id')
    def change_rr_applicant_id(self):
        self.applicant_id = self.rr_applicant_id.applicant_id.id
        self.recruitment_request_id = self.rr_applicant_id.recruitment_request_id.id

    def create_new_rr_meeting(self):
        print('tao moi nhe')
        self.env['interview.meeting'].sudo().create({
            'rr_applicant_id': self.rr_applicant_id.id,
            'recruitment_request_id': self.rr_applicant_id.recruitment_request_id.id,
            'applicant_id': self.rr_applicant_id.applicant_id.id,
            'interviewer_ids': [(6,0,self.interviewer_ids.ids)],
            'interview_date': self.interview_date,
        })