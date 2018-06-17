# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Custom Module',
    'summary': "Cập nhật module purchase",
    'version': '1.0',
    'description': """
        Module phát triển bởi Tony Đỗ và chuyên gia Nguyễn Thanh Thảo. 
        Mục đích: cập nhật quy trình phân hệ purchase phù hợp với yêu cầu doanh nghiệp.
    """,
    'website': 'https://github.com/dmtrong1403',
    'author': "Tony Đỗ và chuyên gia Nguyễn Thanh Thảo",
    'category': 'Custom modules',
    'depends': ['base', 'purchase', 'product', 'purchase_request'],
    'data': [
        'security/purchase_security.xml',
        'security/ir.model.access.csv',
        'views/base_inherited_view.xml',
        'views/product_inherited_view.xml',
        'views/purchase_inherited_view.xml',
        'views/hide_items.xml',
        'views/purchase_custom_pricelist.xml',
        'report/purchase_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
