# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions

class Book(models.Model):
    _name = "books_management.mybook"
    _rec_name = "book_name"
    book_name = fields.Char(string="Book name", help="Please type book name",)
    book_description = fields.Text("Description")
    book_type = fields.Selection(string="book type",
                                 selection=[
                                     ("comic", "Comic"),
                                     ("manga", "Manga"),
                                     ("manhwa", "Manhwa"),
                                      ])
    book_publish_date = fields.Date("Publish date")
    count = fields.Integer("NumberOf")
    book_update_date = fields.Date("Update date")
    demo_content = fields.Html("Demo content")
    status = fields.Boolean("Status")
    money = fields.Float("Money")
    price = fields.Float("Sell price", compute="_sell_calculate")
    image = fields.Binary(string="image")
    author = fields.Many2one(comodel_name="books_management.author",
                             string="Author")
    editors = fields.Many2many(comodel_name="books_management.author",
                             string="Editors")
    
    @api.multi
    @api.constrains("book_name")
    def _check_book_name(self):
        if(" " not in self.book_name):
            raise exceptions.ValidationError("book name must "\
                                             "be contain a blank")

    @api.onchange("book_name", "count", "money", "status", "author")
    def _auto_fill_name(self):
        self.book_description = self.book_name
        self.bind_data()
    
    def bind_data(self):
        book_description = ""
        if self.book_name:
            book_description += "Book_name: {}\n".format(self.book_name)
        if self.author:
            book_description += "Author: {}\n".format(self.author["author_name"])
        if self.count:
            book_description += "Count: {}\n".format(self.count)
        if self.money:
            book_description += "Money: {}\n".format(self.money)
        if book_description:
            book_description += "Status: {}\n".format(self.status)
        self.book_description = book_description
    
    @api.depends("count", "money")
    def _sell_calculate(self):
            if self.count > 3:
                self.price = self.money
            elif self.count > 0:
                self.price = self.money * 120/100
