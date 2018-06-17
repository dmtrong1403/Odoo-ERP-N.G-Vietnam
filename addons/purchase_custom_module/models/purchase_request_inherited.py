# -*- coding: utf-8 -*-

# from odoo import models, fields
#
#
# class purchase_request_line_custom(models.Model):
#     _inherit = "purchase.request.line"
#
#     product_warranty = fields.Integer(string="Bảo Hành(tháng)", related="product_id.product_warranty")
#     manufacturer = fields.Many2one(comodel_name="res.partner", string="Hãng sản xuất",
#                                    related="product_id.manufacturer")
#     product_country = fields.Many2one(comodel_name="res.country", string="Xuất xứ", ondelete="restrict",
#                                       related="product_id.product_country")
