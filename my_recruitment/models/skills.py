from odoo import api, fields, models, _

class HrSkill(models.Model):
    _inherit = 'hr.skill.level'
    _rec_name = 'name'

    skill_id = fields.Many2one(comodel_name='hr.skill',string='Skill')
class HrSkill(models.Model):
    _inherit = 'hr.skill'

    skill_level_ids = fields.One2many(comodel_name='hr.skill.level',inverse_name='skill_id')

