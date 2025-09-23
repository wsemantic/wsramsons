# -*- coding: utf-8 -*-
{
    'name': "wsramsons",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Semantic Web Software SL",
    'website': "https://wsemantic.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'account', 'crm'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/product.xml',
        'views/partner.xml',
        'views/invoice.xml',
        'views/due_list.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "license": "AGPL-3",
}
