# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class custom_product_product(models.Model):
    _inherit = "product.product"

    product_warranty = fields.Integer(string="Bảo Hành(tháng)", track_visibility="onchange")
    manufacturer = fields.Many2one(comodel_name="res.partner", string="Hãng sản xuất", track_visibility="onchange")
    product_country = fields.Many2one(comodel_name="res.country", string="Xuất xứ", ondelete="restrict",
                                      track_visibility="onchange")
    po_tag = fields.Many2one(comodel_name="purchase.order", string="Purchase Order Tag", track_visibility="onchange")
    custom_pricelist_ids = fields.One2many(comodel_name="purchase.custom.pricelist", inverse_name="product_id",
                                           string="Bảng giá nhà cung cấp")

    @api.onchange("attribute_value_ids")
    def apply_change_to_product_pricelist(self):
        for product in self.custom_pricelist_ids:
            product.attribute_value_ids = self.attribute_value_ids


class custom_product_attribute_value(models.Model):
    _inherit = "product.attribute.value"

    @api.multi
    def name_get(self):
        if not self._context.get('show_attribute', True):  # TDE FIXME: not used
            return super(custom_product_attribute_value, self).name_get()
        return sorted([(value.id, "%s: %s" % (value.attribute_id.name, value.name)) for value in self])
