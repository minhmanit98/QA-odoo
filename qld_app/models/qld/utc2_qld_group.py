# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QLDGroup (models.Model):
    _name = 'utc2.qls.group'
    _description = 'Nhóm môn'

    name = fields.Char('NHóm môn', required=True)
    subjects = fields.Float(string='Môn học')








