from odoo import api, fields, models, _

class WizardCreateRRAplicant(models.TransientModel):
    _name = "wizard.create.rr.applicant"
    _description = "Create RR Applicant"

    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    type = fields.Selection(selection=[('rr','RR'),('applicant','Applicant')],string='Type')

    @api.onchange('recruitment_request_id','type')
    def change_recruitment_request_id(self):
        state_draft_id = self.env.ref('my_recruitment.stage_draft').id
        reviewing_draft_id = self.env.ref('my_recruitment.stage_reviewing').id
        all_applicant_accept = self.env['hr.applicant'].search([('stage_id','in',[state_draft_id,reviewing_draft_id])])
        if self.type == 'rr' and self.recruitment_request_id:
            return {
                'domain':{
                    'applicant_id':[
                        ('id','in',all_applicant_accept.ids),
                        ('id','not in',self.recruitment_request_id.rr_applicant_ids.mapped('applicant_id.id'))
                    ]}
            }


    @api.onchange('applicant_id','type')
    def change_applicant_id(self):
        print('yyyyyyyyyyyyyyyyyyyyyyyyyy')

    def create_new_rr_applicant(self):
        print("ahihi")
        if self.recruitment_request_id and self.applicant_id:
            self.env['recruitment.request.applicant'].sudo().create({
                'recruitment_request_id': self.recruitment_request_id.id,
                'applicant_id': self.applicant_id.id,
                'stage_id': self.env.ref('my_recruitment.stage_draft').id
            })