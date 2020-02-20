import json

from odoo import http
from odoo.http import request


class QA (http.Controller):

    @http.route('/library/books', auth='user')
    def list(self, **kwargs):
        QA = http.request.env['library.book']
        qas = QA.search([])
        return http.request.render(
            'library_app.book_list_template',
            {'qa': QA})


    # def example(self, Var):
    #     values = {}
    #
    #     data = request.env['ProjectName.TableName'].sudo().search([("id", "=", int(Var))])
    #
    #     if data:
    #         values['success'] = True
    #         values['return'] = "Something"
    #     else:
    #         values['success'] = False
    #         values['error_code'] = 1
    #         values['error_data'] = 'No data found!'
    #
    #     return json.dumps(values)
