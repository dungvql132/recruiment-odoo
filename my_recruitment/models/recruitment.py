from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ExpectApplicant(models.Model):
    _name = "expect.applicant"
    _description = "Expect Applicant"

    name = fields.Char('Name')
    skill_type_id = fields.Many2one(comodel_name='hr.skill.type',string='Skill Type')
    skill_id = fields.Many2one(comodel_name='hr.skill',string='Skill')
    expect_quantity = fields.Integer(string='Expect Quantity')
    ob_quantity = fields.Integer(string='OB Quantity')
    remain_quantity = fields.Integer(string='Remain Quantity')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request',string='Recruitment Request')

    @api.depends('expect_quantity','ob_quantity')
    def compute_remain_quantity(self):
        for rec in self:
            rec.remain_quantity = rec.expect_quantity - rec.ob_quantity

class RecruimentRequest(models.Model):
    _name = "recruitment.request.applicant"
    _description = "Recruitment Request Applicant"
    _rec_name = 'applicant_id'

    applicant_id = fields.Many2one(comodel_name='hr.applicant',string='Applicant')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request',string='Recruitment Request')
    stage_id = fields.Many2one(comodel_name='hr.recruitment.stage', string='Stage')
    note = fields.Char(string='Note')
    accept_date = fields.Datetime(string='Accept Date')
    on_board_date = fields.Date(string='On Board Date')
    reject_date = fields.Datetime(string='Reject Date')
    interview_answer_id = fields.Many2one(comodel_name='interview.answer', string='Interview Answer')
    offer_id = fields.Many2one(comodel_name='offer.request', string='Offer')

    state = fields.Char(string='State',compute='compute_stage_id', store=True)

    def action_on_board(self):
        return {
            'name': _("Set On Board"),
            'view_mode': 'form',
            'view_id': self.env.ref('my_recruitment.wizard_set_onboard_from').id,
            'view_type': 'form',
            'res_model': 'wizard.set.onboad.rr',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_rr_applicant_id': self.id,
            }
        }

    @api.depends('stage_id')
    def compute_stage_id(self):
        for rec in self:
            rec.state = rec.stage_id.name

    def action_to_reviewing(self):
        self.stage_id = self.env.ref('my_recruitment.stage_reviewing').id

    def action_accept_ol(self):
        self.stage_id = self.env.ref('my_recruitment.stage_accept_ol').id

    def action_reject_ol(self):
        self.stage_id = self.env.ref('my_recruitment.stage_reject_ol').id

    @api.constrains('stage_id')
    def contrains_stage_id(self):
        for rec in self:
            rec.applicant_id.stage_id = rec.stage_id.id

    def create_interview_answer(self):
        #         	my_recruitment.interview_answer_form
        return {
            'name': _("Create New Interview Answer"),
            'view_mode': 'form',
            'view_id': self.env.ref('my_recruitment.create_interview_answer_form').id,
            'view_type': 'form',
            'res_model': 'interview.answer',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_rr_applicant_id': self.id,
            }
        }

    def view_interview_answer(self):
        if not self.interview_answer_id:
            raise ValueError("This RR Applicant don't have interview answer")
        return {
            'name': _("Create New Interview Answer"),
            'view_mode': 'form',
            'view_id': self.env.ref('my_recruitment.view_interview_answer_form').id,
            'view_type': 'form',
            'res_model': 'interview.answer',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'res_id': self.interview_answer_id.id,
        }
    def create_offer(self):
        return {
            'name': _("Create New Offer"),
            'view_mode': 'form',
            'view_id': self.env.ref('my_recruitment.offer_request_form').id,
            'view_type': 'form',
            'res_model': 'offer.request',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {
                'default_type': 'created',
                'default_rr_applicant_id': self.id,
            }
        }

    def view_offer(self):
        return {
            'name': _("View Offer"),
            'view_mode': 'form',
            'view_id': self.env.ref('my_recruitment.view_offer_request_form').id,
            'view_type': 'form',
            'res_model': 'offer.request',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': '[]',
            'context': {
            },
            'res_id': self.offer_id.id,
        }

class RecruimentRequest(models.Model):
    _name = "recruitment.request"
    _description = "Recruitment Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'reference'

    def get_default_reference(self):
        return self.env['ir.sequence'].next_by_code('recruitment.request') or "New"

    name = fields.Char('Name')
    reference = fields.Char('Reference', default= lambda self: _('New'))
    state = fields.Selection(selection=[('draft','Draft'),('submitted','Submitted'),
                                        ('opening','Opening'),('pending','Pending'),
                                        ('close','Close'),('reject','Reject')], string='State', default='draft',tracking=True)
    expect_quantity = fields.Integer(string='Expect Quantity', compute='compute_expect_quantity', store=True)
    remain_quantity = fields.Integer(string='Remain Quantity', compute='compute_remain_quantity', store=True)
    ob_quantity = fields.Integer(string='OB Quantity', compute='compute_ob_quantity', store=True)
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
    recruiter_ids = fields.Many2many(comodel_name='hr.employee',
                                     relation='rr_request_recruiter_rel',
                                     string='Recruiters')
    recruiter_user_ids = fields.Many2many(comodel_name='res.users',
                                          relation='rr_request_recruiter_user_rel',
                                          string='Recruiters User')

    @api.constrains('recruiter_ids')
    def compute_recruiter_user_ids(self):
        for rec in self:
            print("data: ", rec)
            print("data 1: ", rec.recruiter_ids)
            print(rec.recruiter_ids.filtered(lambda x: x.user_id).mapped('user_id.id'))
            value_set = [(6,0,rec.recruiter_ids.filtered(lambda x:x.user_id).mapped('user_id.id'))]
            print(value_set)
            rec.recruiter_user_ids = value_set

    @api.constrains('rr_applicant_ids','rr_applicant_ids.stage_id')
    def contrains_rr_applicant_ids(self):
        for rec in self:
            ob_rr_ids = rec.rr_applicant_ids.filtered(lambda x:
                                              x.stage_id.id == self.env.ref('my_recruitment.stage_on_board').id)
            print('rec.expect_applicant_ids', rec.expect_applicant_ids)
            print('rec.rr_applicant_ids', ob_rr_ids)

            for data in rec.expect_applicant_ids:
                count_ob = 0
                for ob_rr in ob_rr_ids:
                    if data.skill_id.id == ob_rr.offer_id.skill_id.id:
                        count_ob += 1
                data.ob_quantity = count_ob

    @api.model
    def create(self, vals_list):
        reference = vals_list.get('reference', _('New'))
        if reference and reference == _('New'):
            vals_list['reference'] = self.get_default_reference()
        return super(RecruimentRequest, self).create(vals_list)

    @api.depends('expect_applicant_ids','expect_applicant_ids.expect_quantity')
    def compute_expect_quantity(self):
        for rec in self:
            rec.expect_quantity = sum(rec.expect_applicant_ids.mapped('expect_quantity'))

    @api.depends('expect_applicant_ids', 'expect_applicant_ids.remain_quantity')
    def compute_remain_quantity(self):
        for rec in self:
            rec.remain_quantity = sum(rec.expect_applicant_ids.mapped('remain_quantity'))

    @api.depends('expect_applicant_ids', 'expect_applicant_ids.ob_quantity')
    def compute_ob_quantity(self):
        for rec in self:
            rec.remain_quantity = sum(rec.expect_applicant_ids.mapped('ob_quantity'))

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
        if self.state != 'opening':
            raise ValidationError(_('RR is not opening'))
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
                'default_recruitment_request_id':self.id,
            }
        }