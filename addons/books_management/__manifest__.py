# -*- coding: utf-8 -*-
{
    'name': "books_management",
    'summary': "chương trình demo quản lý sách",
    'description': """
        Chương trình quản lý sách được tạo bởi ...
    """,
    'author': "Vinh.NguyenQuang",
    'website': "http://www.quangvinh86.domain",
    'category': 'Demo',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'views/books.xml',
        'views/authors.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
