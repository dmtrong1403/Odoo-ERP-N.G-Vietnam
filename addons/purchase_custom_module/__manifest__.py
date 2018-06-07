# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'purchase_custom_module',
    'version': '1.0',
    'description': """
	Custom module developed by LZ dev Team
    """,
    'depends': ['base', 'purchase', 'product', 'purchase_request'],
    'data': [
        'security/purchase_security.xml',
        'security/ir.model.access.csv',
        'views/base_inherited_view.xml',
        'views/product_inherited_view.xml',
        'views/purchase_inherited_view.xml',
        'views/hide_items.xml',
        'views/purchase_custom_pricelist.xml',
        'views/purchase_request_inherited_view.xml',
        'report/purchase_report_template.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': True,
    'auto_install': False,
}
