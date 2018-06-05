#  -*-  coding:  utf-8  -*-
from odoo import models, fields

class myconf(models.Model):
    _name='myconferences.myconf'
    _description='a model for a conference'
    confname=fields.Char('ConfName' , Required=True)
    indexed=fields.Boolean('Indexed ?', Required=True)
    startdate=fields.Date('Start Date', Required=True)
    enddate=fields.Date('End Date', Required=True)
    fee=fields.Float('Registration Fee', Required=True)
