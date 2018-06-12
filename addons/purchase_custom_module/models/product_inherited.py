# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class custom_product_product(models.Model):
    _inherit = "product.product"

    product_warranty = fields.Integer(string="Bảo Hành(tháng)", track_visibility="onchange")
    manufacturer = fields.Many2one(comodel_name="res.partner", string="Hãng sản xuất", track_visibility="onchange")
    product_country = fields.Many2one(comodel_name="res.country", string="Xuất xứ", ondelete="restrict",
                                      track_visibility="onchange")
    custom_pricelist_ids = fields.One2many(comodel_name="purchase.custom.pricelist", inverse_name="product_id",
                                           string="Bảng giá nhà cung cấp")

    @api.onchange("attribute_value_ids")
    def apply_change_to_product_pricelist(self):
        for product in self.custom_pricelist_ids:
            product.attribute_value_ids = self.attribute_value_ids
