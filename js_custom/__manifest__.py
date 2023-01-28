# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'JS CusTom',
    'version' : '1.1',
    'summary': 'JS CusTom',
    'sequence': 0,
    'description': """JS CusTom""",
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/asset.xml',
    ],
    'demo': [
    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
