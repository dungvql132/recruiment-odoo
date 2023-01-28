from odoo import api, fields, models, _

class InterviewAnswer(models.Model):
    _name = 'interview.answer'
    _description = 'Interview Answer'

    def get_domain_stage_id(self):
        interviewed_id = self.env.ref('my_recruitment.stage_interviewed').id
        accept_ol_id = self.env.ref('my_recruitment.stage_accept_ol').id
        reject_ol_id = self.env.ref('my_recruitment.stage_reject_ol').id
        on_board_id = self.env.ref('my_recruitment.stage_on_board').id

        return [('id','in',[interviewed_id,accept_ol_id,reject_ol_id,on_board_id])]

    def get_default_stage_id(self):
        interviewed_id = self.env.ref('my_recruitment.stage_interviewed').id

        return interviewed_id

    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    rr_applicant_id = fields.Many2one(comodel_name='recruitment.request.applicant', string='RR Applicant')
    stage_id = fields.Many2one(comodel_name='hr.recruitment.stage', string='Stage',
                               domain=lambda self: self.get_domain_stage_id(),
                               default=lambda self: self.get_default_stage_id())
    note = fields.Char(string='Note')
    accept_date = fields.Datetime(string='Accept Date')
    reject_date = fields.Datetime(string='Reject Date')
    skill_id = fields.Many2one(comodel_name='hr.skill',string='Skill')

    @api.onchange('rr_applicant_id')
    def change_rr_applicant_id(self):
        self.applicant_id = self.rr_applicant_id.applicant_id.id
        self.recruitment_request_id = self.rr_applicant_id.recruitment_request_id.id

    @api.constrains('rr_applicant_id')
    def add_interview_answer_to_rr_app(self):
        for rec in self:
            if rec.rr_applicant_id:
                rec.rr_applicant_id.sudo().write({
                    'interview_answer_id':rec.id,
                    'stage_id': self.env.ref('my_recruitment.stage_interviewed').id
                })
            else:
                rec.rr_applicant_id.sudo().write({
                    'stage_id': self.env.ref('my_recruitment.stage_inprocessing').id
                })