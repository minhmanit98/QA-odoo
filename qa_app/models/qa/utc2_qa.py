from odoo import fields, models, api


class QA (models.Model):
    _name = 'utc2.qa'
    _description = 'Question and Answer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Question', required=True)
    date_published = fields.Date()
    status = fields.Many2one('res.partner', string='Status')
    active = fields.Boolean('Active?', default=True)
    answer = fields.Char('Answer', required=True)
    category = fields.Many2one('utc2.qa.category', string='Category')


    


