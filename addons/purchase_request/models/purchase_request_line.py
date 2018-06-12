# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class purchase_request_line(models.Model):
    _name = "purchase.request.line"
    _rec_name = "purchase_request_name"

    def _get_line_numbers(self):
        line_num = 1
        if self.ids:
            first_line_rec = self.browse(self.ids[0])

            for line_rec in first_line_rec.purchase_request_id.purchase_request_line_ids:
                line_rec.line_no = line_num
                line_num += 1

    product_id = fields.Many2one("product.product", "Tên vật tư", required=True)
    purchase_request_id = fields.Many2one("purchase.request", "Mã yêu cầu")
    purchase_request_name = fields.Char(string="Tên yêu cầu", store=False, related="purchase_request_id.name")
    product_uom = fields.Many2one("product.uom", "Đơn vị tính", related="product_id.uom_id", required=True)
    product_qty = fields.Float("Số lượng", required=True, default=1)
    attribute_value_ids = fields.Many2many('product.attribute.value',
                                           string="Yêu cầu kỹ thuật")
    deadline = fields.Date("Hạn chót", required=True, default=datetime.today())
    vendor_name = fields.Char("Nhà cung cấp")
    note = fields.Char("Ghi chú")
    project_id = fields.Many2many(comodel_name="project.project", string="Dự án")
    state = fields.Selection("Tình trạng duyệt", related="purchase_request_id.state")
    line_no = fields.Integer(compute='_get_line_numbers', string='STT', readonly=False, default=False)
    is_finished = fields.Boolean(string="Hoàn thành", default=False)

    _sql_constraints = [
        ("check_product_qty", "CHECK (product_qty > 0)", "Số lượng sản phẩm không hợp lệ. Xin vui lòng kiểm tra lại")]

    @api.onchange("product_id")
    def get_product_attr_vals(self):
        if self.product_id:
            self.attribute_value_ids = self.product_id.attribute_value_ids

    @api.model
    def create(self, values):
        line = super(purchase_request_line, self).create(values)
        if line.purchase_request_id.state != 'draft':
            msg = _("Bổ sung yêu cầu %s ") % (line.product_id.display_name,)
            line.purchase_request_id.message_post(body=msg)
        return line

    @api.multi
    def write(self, values):
        requests = False
        if 'product_qty' in values or 'product_id' in values:
            changed_lines = self.filtered(lambda x: x.purchase_request_id.state != 'draft')
            if changed_lines:
                requests = changed_lines.mapped('purchase_request_id')
                for request in requests:
                    request_lines = changed_lines.filtered(lambda x: x.purchase_request_id == request)
                    msg = "<ul>"
                    for line in request_lines:
                        if 'product_id' in values:
                            values_product_id = self.env['product.product'].browse(values['product_id'])
                            msg += "<li> %s -> %s" % (line.product_id.display_name, values_product_id.display_name)
                        else:
                            msg += "<li> %s" % (line.product_id.display_name,)
                        if 'product_qty' in values:
                            msg += "<br/>" + _("Số lượng yêu cầu") + ": %s -> %s <br/>" % (
                                line.product_qty, float(values['product_qty']),)
                    msg += "</ul>"
                    request.message_post(body=msg)
        result = super(purchase_request_line, self).write(values)
        return result

    @api.multi
    def unlink(self):
        for line in self:
            if line.purchase_request_id.state != 'draft':
                raise UserError('Không thể xóa yêu cầu đã gửi.')
            else:
                msg = _("Hủy bỏ yêu cầu %s ") % (line.product_id.display_name,)
                line.purchase_request_id.message_post(body=msg)
        return super(purchase_request_line, self).unlink()
