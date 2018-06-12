# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2017 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.addons.decimal_precision as dp

from odoo import api, fields, models, tools


class custom_purchase_report(models.Model):
    _inherit = "purchase.report"

    discount = fields.Float(
        string="Discount (%)", digits=dp.get_precision("Discount"),
        group_operator="avg",
    )
    product_warranty = fields.Integer(string="Bảo hành (tháng)", readonly=True)
    price_unit = fields.Float(string="Giá", readonly=True)
    rating_by_po = fields.Integer(string="Đánh giá (sao)", readonly=True)
    purchase_order_id = fields.Char(string="PO", readonly=True)
    product_origin = fields.Many2one(comodel_name="res.country", string="Xuất xứ", ondelete="restrict")

    def _join_product_supplierinfo(self):
        return """
            left join product_supplierinfo ps on (t.id = ps.product_tmpl_id)
        """

    def _select_product_origin(self):
        return """
            , ps.product_origin AS product_origin
        """

    def _select_purchase_discount(self):
        return """
            , l.discount AS discount
            """

    def _select_purchase_order_name(self):
        return """
            , s.name AS purchase_order_id
            """

    def _select_product_warranty(self):
        return """
            ,sum(t.product_warranty) as product_warranty
        """

    def _select_price_unit(self):
        return """
            ,sum(l.price_unit) as price_unit
        """

    def _select_rating_by_po(self):
        return """
            ,sum(cast(l.rating_by_po as integer)) as rating_by_po
        """

    def _group_by_purchase_discount(self):
        return ", l.discount"

    def _group_by_purchase_order_name(self):
        return ", s.name"

    def _group_by_product_origin(self):
        return ", ps.product_origin"

    def _get_discounted_price_unit_exp(self):
        """Inheritable method for getting the SQL expression used for
        calculating the unit price with discount(s).

        :rtype: str
        :return: SQL expression for discounted unit price.
        """
        return "(1 - l.discount / 100) * l.price_unit "

    @api.model_cr
    def init(self):
        """Inject parts in the query with this hack, fetching the query and
        recreating it. Query is returned all in upper case and with final ";".
        """
        super(custom_purchase_report, self).init()
        self._cr.execute("SELECT pg_get_viewdef(%s, true)", (self._table,))
        view_def = self._cr.fetchone()[0]
        if view_def[-1] == ";":  # Remove trailing semicolon
            view_def = view_def[:-1]

        view_def = view_def.replace(
            "GROUP BY",
            "{} GROUP BY".format(
                self._join_product_supplierinfo()
            ),
        )

        view_def = view_def.replace(
            "FROM purchase_order_line",
            "{} {} {} {} {} {} FROM purchase_order_line".format(
                self._select_purchase_discount(),
                self._select_product_warranty(),
                self._select_price_unit(),
                self._select_rating_by_po(),
                self._select_purchase_order_name(),
                self._select_product_origin()
            ),
        )

        view_def += self._group_by_purchase_discount()
        view_def += self._group_by_purchase_order_name()
        view_def += self._group_by_product_origin()
        # Replace the expression with space for avoiding to replace in the
        # group by part
        view_def = view_def.replace(
            "l.price_unit ", self._get_discounted_price_unit_exp(),
        )
        # Re-create view
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("create or replace view {} as ({})".format(
            self._table, view_def,
        ))
