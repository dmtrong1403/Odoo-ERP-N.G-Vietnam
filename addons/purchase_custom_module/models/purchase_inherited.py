# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models
from . import custom_variables as cv


class custom_purchase_order(models.Model):
    _inherit = 'purchase.order'

    contract_status = fields.Selection(cv.LIST_STATUS, string='Tình trạng hợp đồng')
    tag_ids = fields.Many2many(comodel_name="purchase.request.tag", string="Tag name")
    state = fields.Selection([
        ('draft', 'Bản thảo'),
        ('sent', 'Bản thảo được gửi'),
        ('to approve', 'Bản thảo chờ duyệt'),
        ('purchase', 'Đơn hàng'),
        ('done', 'Hoàn thành'),
        ('cancel', 'Hủy bỏ')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    purchase_contract_line_ids = fields.One2many(comodel_name="purchase.contract.line",
                                                 inverse_name="purchase_order_id")
    purchase_request_id = fields.Many2one(comodel_name="purchase.request", string="Yêu cầu mua hàng", domain="[('state', '=', 'received')]")

    @api.onchange("purchase_request_id")
    def get_purchase_request_line(self):
        if self.purchase_request_id:
            result = []
            for line in self.purchase_request_id.purchase_request_line_ids:
                result.append(
                    {'product_id': line.product_id, 'product_uom': line.product_uom, 'product_qty': line.product_qty,
                     'price_unit': 0, 'attribute_value_ids': line.attribute_value_ids, 'date_planned': line.deadline,
                     'name': line.product_id.display_name})
            self.tag_ids = self.purchase_request_id.tag_ids
            self.order_line = result

class custom_purchase_orderline(models.Model):
    _inherit = 'purchase.order.line'

    def get_prod_attr(self):
        return self.product_id.attribute_value_ids

    def _get_line_numbers(self):
        line_num = 1
        if self.ids:
            first_line_rec = self.browse(self.ids[0])

            for line_rec in first_line_rec.order_id.order_line:
                line_rec.line_no = line_num
                line_num += 1

    rating_by_po = fields.Selection(cv.LIST_RATING, string='Đánh giá')
    discount = fields.Float(
        string='Chiết khấu (%)', digits=dp.get_precision('Discount'),
    )
    manufacturer = fields.Many2one(comodel_name="res.partner", string="Hãng sản xuất",
                                   related="product_id.manufacturer")
    product_country = fields.Many2one('res.country', string='Xuất xứ', ondelete='restrict',
                                      related="product_id.product_country")
    attribute_value_ids = fields.Many2many('product.attribute.value', string='Thông số kỹ thuật')
    line_no = fields.Integer(compute='_get_line_numbers', string='STT', readonly=False, default=False)

    @api.onchange("product_id")
    def change_prod_attr(self):
        if self.product_id:
            self.attribute_value_ids = self.get_prod_attr()

    @api.depends('discount')
    def _compute_amount(self):
        for line in self:
            price_unit = False
            # This is always executed for allowing other modules to use this
            # with different conditions than discount != 0
            price = line._get_discounted_price_unit()
            if price != line.price_unit:
                # Only change value if it's different
                price_unit = line.price_unit
                line.price_unit = price
            super(custom_purchase_orderline, line)._compute_amount()
            if price_unit:
                line.price_unit = price_unit

        _sql_constraints = [
            ('discount_limit', 'CHECK (discount <= 100.0)',
             'Discount must be lower than 100%.'),
        ]

    def _get_discounted_price_unit(self):
        """Inheritable method for getting the unit price after applying
        discount(s).

        :rtype: float
        :return: Unit price after discount(s).
        """
        self.ensure_one()
        if self.discount:
            return self.price_unit * (1 - self.discount / 100)
        return self.price_unit

    @api.multi
    def _get_stock_move_price_unit(self):
        """Get correct price with discount replacing current price_unit
        value before calling super and restoring it later for assuring
        maximum inheritability.
        """
        price_unit = False
        price = self._get_discounted_price_unit()
        if price != self.price_unit:
            # Only change value if it's different
            price_unit = self.price_unit
            self.price_unit = price
        price = super(custom_purchase_orderline, self)._get_stock_move_price_unit()
        if price_unit:
            self.price_unit = price_unit
        return price
