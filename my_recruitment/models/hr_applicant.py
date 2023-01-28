from odoo import api, fields, models, _


class InterviewMeeting(models.Model):
    _name = 'interview.meeting'
    _description = 'Interview Meeting'

    interview_date = fields.Datetime(string='Interview Date')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    rr_applicant_id = fields.Many2one(comodel_name='recruitment.request.applicant', string='RR Applicant')
    note = fields.Char(string='Note')
    interviewer_ids = fields.Many2many(comodel_name='hr.employee', relation='interviewer_employee_rel',
                                       string='Interviewer')
    state = fields.Selection(selection=[
        ('waiting','Waiting'),('cancel','Cancel'),('finish','Finish')
    ],default='waiting')

    def action_cancel_interview(self):
        self.state = 'cancel'

    def action_finish_interview(self):
        self.state = 'finish'
        self.rr_applicant_id.stage_id = self.env.ref('my_recruitment.stage_inprocessing').id
class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    rr_applicant_ids = fields.One2many(comodel_name='recruitment.request.applicant',
                                       inverse_name='applicant_id',
                                       string='RR Applicant')

    interview_meeting_ids = fields.One2many(comodel_name='interview.meeting',
                                            inverse_name='applicant_id',
                                            string='Interview Meeting')

    recruiter_id = fields.Many2one(comodel_name='hr.employee',string='Recruiter')

    @api.model
    def create(self, vals_list):
        if not vals_list.get('stage_id',None):
            vals_list.setdefault('stage_id',self.env.ref('my_recruitment.stage_draft').id)
            vals_list['stage_id'] = self.env.ref('my_recruitment.stage_draft').id
        return super(HrApplicant, self).create(vals_list)

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
                'default_type':'applicant',
                'default_applicant_id':self.id,
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
            }
        }