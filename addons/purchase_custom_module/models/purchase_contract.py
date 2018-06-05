# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class purchase_contract_line(models.Model):
    _name = "purchase.contract.line"
    _rec_name = "id"

    purchase_order_id = fields.Many2one(comodel_name="purchase.order")
    contract_phase = fields.Integer(string="Đợt", required=True)
    payment_date = fields.Date(string="Hạn thanh toán", required=True)
    payment_amount = fields.Float(string="Số tiền", required=True)
    note = fields.Char(string="Ghi chú")
