# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
RATING_STATUS = [
    ('0', 'Chưa đánh giá'),
    ('1', 'Rất kém'),
    ('2', 'Kém'),
    ('3', 'Bình thường'),
    ('4', 'Yêu thích'),
    ('5', 'Rất được yêu thích')
]

CONTRACT_STATUS = [
    ('0', 'Đang soạn'),
    ('1', 'Đang trình ký'),
    ('2', 'Đã nhận bản cứng')
]

PO_STATUS = [
    ('draft', 'Bản thảo'),
    ('sent', 'Bản thảo được gửi'),
    ('to approve', 'Bản thảo chờ duyệt'),
    ('purchase', 'Đơn hàng'),
    ('done', 'Hoàn thành'),
    ('cancel', 'Hủy bỏ')
]

# Phần này xổ xuống 11 trường: EXW, FCA, FOB, FAS, CFR, CIF, CPT, CIP, DAF, DES, DEQ, DDU, DDP

ECO_TERM = [
    ('EXW', 'EXW'),
    ('FCA', 'FCA'),
    ('FOB', 'FOB'),
    ('FAS', 'FAS'),
    ('CFR', 'CFR'),
    ('CIF', 'CIF'),
    ('CPT', 'CPT'),
    ('CIP', 'CIP'),
    ('DAF', 'DAF'),
    ('DES', 'DES'),
    ('DEQ', 'DEQ'),
    ('DDU', 'DDU'),
    ('DDP', 'DDP')
]
