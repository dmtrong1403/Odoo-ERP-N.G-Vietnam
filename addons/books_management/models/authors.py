# -*- coding: utf-8 -*-
from odoo import models, fields

class Author(models.Model):
    _name = "books_management.author"
    _rec_name = "author_name"
    _auto = True
    # _table = "authors"
    _decription ="My ebook"
    _order = "author_name"
    _translate = False;
    author_name = fields.Char("Author name")
    date_of_birth = fields.Date("Date of birth")
    books = fields.One2many(comodel_name="books_management.mybook",
                            inverse_name="author",
                            string="Main editor")
    _sql_constraints = [
     ('name_uniq', 'UNIQUE(author_name)',
     'You can not enter two author with the same name ')
    ]

