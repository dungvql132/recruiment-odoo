from odoo import api, fields, models, _

class InterviewAnswer(models.Model):
    _name = 'interview.answer'
    _description = 'Interview Answer'

    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    stage_id = fields.Many2one(comodel_name='hr.recruitment.stage', string='Stage')
    note = fields.Char(string='Note')
    accept_date = fields.Datetime(string='Accept Date')
    reject_date = fields.Datetime(string='Reject Date')