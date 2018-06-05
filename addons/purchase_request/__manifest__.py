# -*- coding: utf-8 -*-
{
    'name': "purchase_request",
    'summary': "Module yêu cầu mua sắm",
    'description': """
        Module được phát triển bởi Livezone development team
    """,
    'author': "Livezone development team",
    # 'website': "http://www.quangvinh86.domain",
    'category': 'Custom module',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'project'],
    # always loaded
    'data': [
        'security/purchase_security.xml',
        'security/ir.model.access.csv',
        'views/purchase_request.xml',
        'views/purchase_request_line.xml',
        'views/workflow.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
