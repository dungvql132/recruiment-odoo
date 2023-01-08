from odoo import api, fields, models, _

class WizardCreateRRAplicant(models.TransientModel):
    _name = "wizard.create.rr.applicant"
    _description = "Create RR Applicant"

    applicant_id = fields.Many2one(comodel_name='hr.applicant', string='Applicant')
    recruitment_request_id = fields.Many2one(comodel_name='recruitment.request', string='Recruitment Request')
    type = fields.Selection(selection=[('rr','RR'),('applicant','Applicant')],string='Type')

    def create_new_rr_applicant(self):
        for rec in self:
            if rec.recruitment_request_id and rec.applicant_id:
                self.env['recruitment.request.applicant'].sudo().create({
                    'recruitment_request_id': rec.recruitment_request_id.id,
                    'applicant_id': rec.applicant_id.id
                })