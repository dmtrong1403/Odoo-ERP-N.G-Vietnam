# -*- coding: utf-8 -*-
{
    'name': "Purchase Request",
    'summary': "Yêu cầu mua sắm",
    'description': """
        Module phát triển bởi Tony Đỗ và chuyên gia Nguyễn Thanh Thảo. 
        Mục đích: phát triển menu yêu cầu mua hàng cho đối tượng người dùng các phòng ban và phòng purchasing.
    """,
    'website': 'https://github.com/dmtrong1403',
    'author': "Tony Đỗ và chuyên gia Nguyễn Thanh Thảo",
    'category': 'Custom modules',
    'depends': ['base', 'hr', 'project'],
    'data': [
        'security/purchase_security.xml',
        'security/ir.model.access.csv',
        'views/purchase_request.xml',
        'views/purchase_request_line.xml',
        'views/workflow.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
