from odoo import api, fields, models, _


class InterviewMeeting(models.Model):
    _name = 'interview.meeting'
    _description = 'Interview Meeting'

    interview_date = fields.Datetime(string='Interview Date')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    note = fields.Char(string='Note')
    interviewer_ids = fields.Many2many(comodel_name='hr.employee', relation='interviewer_employee_rel',
                                       string='Interviewer')

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    rr_applicant_ids = fields.One2many(comodel_name='recruitment.request.applicant',
                                       inverse_name='applicant_id',
                                       string='RR Applicant')

    interview_meeting_ids = fields.One2many(comodel_name='interview.meeting',
                                            inverse_name='applicant_id',
                                            string='Interview Meeting')

    recruiter_id = fields.Many2one(comodel_name='hr.employee',string='Recruiter')