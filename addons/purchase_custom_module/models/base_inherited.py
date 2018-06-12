# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

from . import custom_variables as cv


class custom_crm(models.Model):
    _inherit = 'res.partner'

    crm_rating = fields.Selection(cv.RATING_STATUS, string='Đánh giá', track_visibility='always')
