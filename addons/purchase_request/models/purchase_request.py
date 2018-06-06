# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class purchase_request_tag(models.Model):
    _name = "purchase.request.tag"
    _rec_name = "name"

    name = fields.Char("Tag name")


class purchase_request(models.Model):
    _name = "purchase.request"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = "name"

    def get_current_user(self):
        return self.env.user.id

    def get_current_company(self):
        return self.env.user.company_id.id

    def get_current_department(self):
        resource = self.env['resource.resource'].search([('user_id', '=', self.env.user.id)])
        employee = self.env['hr.employee'].search([('resource_id', '=', resource.id)])
        return employee.department_id.id

    name = fields.Char(string="Nhãn yêu cầu", index=True, copy=False, default='Mới')
    user_id = fields.Many2one("res.users", "Người đề xuất", default=lambda self: self.get_current_user())
    department_id = fields.Many2one("hr.department", "Phòng ban", default=lambda self: self.get_current_department())
    company_id = fields.Many2one("res.company", "Trang trại / Công ty", default=lambda self: self.get_current_company())
    project_ids = fields.Many2many(comodel_name="project.project", string="Dự án", required=True)
    tag_ids = fields.Many2many(comodel_name="purchase.request.tag", string="Tag name")
    propose = fields.Char("Mục đích")
    note = fields.Text()
    purchase_request_line_ids = fields.One2many(comodel_name="purchase.request.line", \
                                                inverse_name="purchase_request_id", \
                                                string="Chi tiết sản phẩm", required=True)
    state = fields.Selection([
        ("draft", "Bản thảo"),
        ("confirmed", "Đã gửi"),
        ("approved", "Đã duyệt"),
        ("received", "Đã nhận yêu cầu"),
        ("done", "Hoàn thành")
    ], "Trạng thái xét duyệt", default="draft", track_visibility='onchange')

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)',
         'Nhãn yêu cầu mua hàng này đã tồn tại.')
    ]

    @api.multi
    def action_draft(self):
        self.state = "draft"

    @api.multi
    def action_confirm(self):
        self.state = "confirmed"

    @api.multi
    def action_approve(self):
        self.state = "approved"

    @api.multi
    def action_receive(self):
        self.state = "received"

    @api.multi
    def action_done(self):
        is_finished = True
        for line in self.purchase_request_line_ids:
            if not line.is_finished:
                raise exceptions.except_orm(
                    'Chưa hoàn thành các yêu cầu mua hàng: cần cập nhật trạng thái hoàn thành cho từng yêu cầu.')
                is_finished = False
                break
        if is_finished:
            self.state = "done"

    @api.multi
    def unlink(self):
        for request in self:
            if request.state != "draft":
                raise exceptions.except_orm('Chỉ được phép xóa bản thảo.')
            else:
                for line in self.purchase_request_line_ids:
                    line.unlink()
                return models.Model.unlink(self)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Mới') == 'Mới':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request')
        return super(purchase_request, self).create(vals)
