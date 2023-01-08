from odoo import api, fields, models, _

class InterviewAnswer(models.Model):
    _name = 'offer.request'
    _description = 'Offer Request'

    name = fields.Char(string='Name')
    note = fields.Char(string='Note')
    min_salary = fields.Integer(string='Min Salary')
    max_salary = fields.Integer(string='Max Salary')
    skill_id = fields.Many2one(comodel_name='hr.skill', string='Skill')
    skill_level_id = fields.Many2one(comodel_name='hr.skill.level',string='Skill Level')