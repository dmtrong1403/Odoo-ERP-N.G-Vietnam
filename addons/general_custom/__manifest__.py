# -*- coding: utf-8 -*-
{
    'name': 'General Custom Module',
    'version': '1.0.0',
    'category': 'Other',
    'author': 'TnT Solution',
    'sequence': 10,
    'summary': '',
    'description': "",
    'depends': ['web'],
    'data': [
        'views/templates.xml',
    ],
    "images": ["static/description/banner.jpeg"],
    'license': 'LGPL-3',
    'qweb': [
        'static/src/xml/base.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
