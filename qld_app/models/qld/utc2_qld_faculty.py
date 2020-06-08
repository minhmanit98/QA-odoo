# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QLDClass (models.Model):
    _name = 'utc2.qls.faculty'
    _description = 'KHoa'

    name = fields.Char('NHóm môn', required=True)
    subjects = fields.Float(string='Môn học')