from odoo import api, fields, models, _

class ExpectApplicant(models.Model):
    _name = "expect.applicant"
    _description = "Expect Applicant"

    name = fields.Char('Name')
    skill_type_id = fields.Many2one(comodel_name='hr.skill.type',string='Skill Type')
    skill_id = fields.Many2one(comodel_name='hr.skill',string='Skill')
    expect_quantity = fields.Integer(string='Expect Quantity')
    remain_quantity = fields.Integer(string='Remain Quantity')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request',string='Recruitment Request')

class RecruimentRequest(models.Model):
    _name = "recruitment.request.applicant"
    _description = "Recruitment Request Applicant"

    applicant_id = fields.Many2one(comodel_name='hr.applicant',string='Applicant')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request',string='Recruitment Request')
    stage_id = fields.Many2one(comodel_name='hr.recruitment.stage', string='Stage')
    note = fields.Char(string='Note')
    accept_date = fields.Datetime(string='Accept Date')
    reject_date = fields.Datetime(string='Reject Date')
class RecruimentRequest(models.Model):
    _name = "recruitment.request"
    _description = "Recruitment Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name')
    state = fields.Selection(selection=[('draft','Draft'),('submitted','Submitted'),
                                        ('opening','Opening'),('pending','Pending'),
                                        ('close','Close'),('reject','Reject')], string='State', default='draft',tracking=True)
    expect_quantity = fields.Integer(string='Expect Quantity', compute='compute_expect_quantity', store=True)
    remain_quantity = fields.Integer(string='Remain Quantity', compute='compute_remain_quantity', store=True)
    ob_quantity = fields.Integer(string='Remain Quantity')
    expect_applicant_ids = fields.One2many(comodel_name='expect.applicant',
                                           inverse_name='recruitment_request_id',
                                           string='Expect Applicant')
    opening_date = fields.Datetime(string='Opening Date')
    deadline_date = fields.Date(string='DeadLine Date')

    rr_applicant_ids = fields.One2many(comodel_name='recruitment.request.applicant',
                                       inverse_name='recruitment_request_id',
                                       string='RR Applicant')

    interview_meeting_ids = fields.One2many(comodel_name='interview.meeting',
                                            inverse_name='recruitment_request_id',
                                            string='Interview Meeting')
    reason_change_state = fields.Char('Reason Change State',tracking=True)
    approved_date = fields.Date('Approve Date', tracking=True)

    @api.depends('expect_applicant_ids','expect_applicant_ids.expect_quantity')
    def compute_expect_quantity(self):
        for rec in self:
            rec.expect_quantity = sum(rec.expect_applicant_ids.mapped('expect_quantity'))

    @api.depends('expect_applicant_ids', 'expect_applicant_ids.remain_quantity')
    def compute_remain_quantity(self):
        for rec in self:
            rec.remain_quantity = sum(rec.expect_applicant_ids.mapped('remain_quantity'))

    def action_submit(self):
        if self.state == 'draft':
            self.state = 'submitted'

    def action_approve(self):
        if self.state == 'submitted':
            self.state = 'opening'

    def action_reject(self):
        if self.state == 'submitted':
            self.state = 'reject'

    def popup_add_new_rr_applicant(self):
        return {
            'name': _("Add new rr applicant"),
            'view_mode': 'form',
            'view_id': self.env.ref('my_recruitment.wizard_create_rr_applicant_view').id,
            'view_type': 'form',
            'res_model': 'wizard.create.rr.applicant',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_type':'rr',
                'default_recruitment_request_id':self.id,
            }
        }

    def popup_change_state_rr(self):
        return {
            'name': _("Change State"),
            'view_mode': 'form',
            'view_id': self.env.ref('my_recruitment.wizard_change_state_rr_from').id,
            'view_type': 'form',
            'res_model': 'wizard.change.state.rr',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_recruitment_request_id':self.id,
            }
        }

    def popup_add_new_rr_meeting(self):
        return {
            'name': _("Add new rr metting"),
            'view_mode': 'form',
            'view_id': self.env.ref('my_recruitment.wizard_create_rr_meeting_view').id,
            'view_type': 'form',
            'res_model': 'wizard.create.rr.meeting',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_type':'rr',
                'default_recruitment_request_id':self.id,
            }
        }