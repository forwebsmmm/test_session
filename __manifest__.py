# -*- coding: utf-8 -*-
{
    'name': "Test",

    'summary': """
        Test module""",

    'description': """
        Test for partners
    """,

    'author': "Andrey",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'contacts'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/test_views.xml',
        'views/test_partner_views.xml',
        'views/test_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
