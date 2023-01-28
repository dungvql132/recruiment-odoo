from odoo import api, fields, models, _

class OfferRequest(models.Model):
    _name = 'offer.request'
    _description = 'Offer Request'

    offer_parent_id = fields.Many2one(comodel_name='offer.request', string="Offer Parent")
    name = fields.Char(string='Name')
    note = fields.Char(string='Note')
    min_salary = fields.Integer(string='Min Salary')
    max_salary = fields.Integer(string='Max Salary')
    skill_id = fields.Many2one(comodel_name='hr.skill', string='Skill')
    skill_level_id = fields.Many2one(comodel_name='hr.skill.level',string='Skill Level')
    type = fields.Selection(selection=[('base','Base'),('created','Created')], string='Type', required=True, default='base')
    rr_applicant_id = fields.Many2one(comodel_name='recruitment.request.applicant', string='RR Applicant')

    @api.onchange('offer_parent_id')
    def change_offer_parent_id(self):
        self.name = self.offer_parent_id.name
        self.note = self.offer_parent_id.note
        self.min_salary = self.offer_parent_id.min_salary
        self.max_salary = self.offer_parent_id.max_salary
        self.skill_id = self.offer_parent_id.skill_id.id
        self.skill_level_id = self.offer_parent_id.skill_level_id.id

    @api.constrains('rr_applicant_id')
    def add_offer_to_rr_applicant(self):
        for rec in self:
            if rec.rr_applicant_id:
                rec.rr_applicant_id.sudo().write({
                    'offer_id': rec.id
                })