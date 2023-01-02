from odoo import api, fields, models, _


class ApplicantRequest(models.Model):
    _name = 'applicant.request'
    _description = 'Applicant Request'

    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    state_id = fields.Many2one(comodel_name='hr.recruitment.stage', string='Stage')
    note = fields.Char(string='Note')
    accept_date = fields.Datetime(string='Accept Date')
    reject_date = fields.Datetime(string='Reject Date')


class InterviewMeeting(models.Model):
    _name = 'interview.meeting'
    _description = 'Interview Meeting'

    interview_date = fields.Datetime(string='Interview Date')
    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    note = fields.Char(string='Note')
    interviewer_ids = fields.Many2many(comodel_name='hr.employee', relation='interviewer_employee_rel',
                                       string='Interviewer')

class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    applicant_request_ids = fields.One2many(comodel_name='applicant.request',
                                            inverse_name='applicant_id',
                                            string='Applicant Request')

    interview_meeting_ids = fields.One2many(comodel_name='interview.meeting',
                                            inverse_name='applicant_id',
                                            string='Interview Meeting')

    recruiter_id = fields.Many2one(comodel_name='hr.employee',string='Recruiter')