from odoo import api, fields, models, _

class Dung(models.Model):
    _name = "dung"
    _description = "Dung"

    name = fields.Char('Name')

