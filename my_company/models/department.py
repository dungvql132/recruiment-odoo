from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrDepartmentPart(models.Model):
    _name = "hr.department.part"
    _description = "Hr Department Part"

    name = fields.Char('Name')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')

    @api.constrains('name','company_id')
    def check_duplicate(self):
        for rec in self:
            data = self.env['hr.department.part'].search([('name','=',rec.name),
                                                          ('company_id','=',rec.company_id.id),
                                                          ('id','!=',rec.id)])
            if data:
                raise ValidationError(_(f'hr department part duplicate: name-{rec.name},company-{rec.company_id.name}'))

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    hr_department_part_id = fields.Many2one(comodel_name='hr.department.part', string="Department Part")