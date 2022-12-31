# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Pivot CusTom',
    'version' : '1.1',
    'summary': 'Pivot CusTom',
    'sequence': 0,
    'description': """Pivot CusTom""",
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/page/billing',
    'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/dung.xml',
    ],
    'demo': [
    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
