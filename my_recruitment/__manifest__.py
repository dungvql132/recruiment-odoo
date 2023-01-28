# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'My Recruitment',
    'version' : '1.1',
    'summary': 'My Recruitment',
    'sequence': -100,
    'description': """
My Recruitment
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/page/billing',
    'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['base','hr_recruitment','hr_skills','my_company'],
    'data': [
        'security/recruitment_groups.xml',
        'security/ir.model.access.csv',
        'security/recruitment_record_rule.xml',
        'views/hr_applicant_view.xml',
        'views/recruitment_view.xml',
        'views/skills_view.xml',
        'views/interview_answer_view.xml',
        'views/offer_view.xml',
        'wizard/create_rr_applicant_view.xml',
        'wizard/create_rr_meeting_view.xml',
        'wizard/change_state_view.xml',
        'data/config_data_stage.xml',
        'data/data.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
