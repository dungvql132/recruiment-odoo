from odoo import api, fields, models, _

class WizardCreateRRAplicant(models.TransientModel):
    _name = "wizard.create.rr.meeting"
    _description = "Create RR Meeting"

    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    interviewer_ids = fields.Many2many(comodel_name='hr.employee', relation='interviewer_employee_wizard_rel',
                                       string='Interviewer', required=True)
    interview_date = fields.Datetime(string='Interview Date', required=True)
    type = fields.Selection(selection=[('rr','RR'),('applicant','Applicant')],string='Type')

    def create_new_rr_meeting(self):
        self.env['interview.meeting'].sudo().create({
            'recruitment_request_id': self.recruitment_request_id.id,
            'applicant_id': self.applicant_id.id,
            'interviewer_ids': [(6,0,self.interviewer_ids.ids)],
            'interview_date': self.interview_date,
        })