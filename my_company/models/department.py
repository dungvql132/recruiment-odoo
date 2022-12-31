from odoo import api, fields, models, _

class Dung(models.Model):
    _name = "hr.department.part"
    _description = "Hr Department Part"
    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'You can not have two users with the same name !')
    ]

    name = fields.Char('Name')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')

