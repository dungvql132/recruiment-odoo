from odoo import api, fields, models, _

class ExpectApplicant(models.Model):
    _name = "expect.applicant"
    _description = "Expect Applicant"

    name = fields.Char('Name')
    skill_id = fields.Many2one(comodel_name='hr.skill',string='Skill')
    expect_quantity = fields.Integer(string='Expect Quantity')
    remain_quantity = fields.Integer(string='Remain Quantity')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request',string='Recruitment Request')

class RecruimentRequest(models.Model):
    _name = "recruitment.request.applicant"
    _description = "Recruitment Request Applicant"

    applicant_id = fields.Many2one(comodel_name='hr.applicant',string='Applicant')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request',string='Recruitment Request')
class RecruimentRequest(models.Model):
    _name = "recruitment.request"
    _description = "Recruitment Request"

    name = fields.Char('Name')
    state = fields.Selection(selection=[('draft','Draft'),('submitted','Submitted'),
                                        ('opening','Opening'),('pending','Pending'),
                                        ('close','Close')], string='State', default='draft')
    expect_quantity = fields.Integer(string='Expect Quantity')
    remain_quantity = fields.Integer(string='Remain Quantity')
    expect_applicant_ids = fields.One2many(comodel_name='expect.applicant',
                                           inverse_name='recruitment_request_id',
                                           string='Expect Applicant')
    opening_date = fields.Datetime(string='Opening Date')
    deadline_date = fields.Date(string='DeadLine Date')

    rr_applicant_ids = fields.One2many(comodel_name='recruitment.request.applicant',
                                       inverse_name='recruitment_request_id',
                                       string='RR Applicant')

