# -*- coding: utf-8 -*-
import json

import base64
import requests
import werkzeug.exceptions
import werkzeug.urls
import werkzeug.wrappers
from addons.website_profile.controllers.main import WebsiteProfile

from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo.http import content_disposition, Controller, request, route


class UTC2Predict(Controller):

    def _prepare_user_values(self, **kwargs):
        values = super(UTC2Predict, self)._prepare_user_values(**kwargs)
        if kwargs.get('predict'):
            values['predict'] = kwargs.get('predict')
        return values

    @http.route(['/sinhvien'], type='http', auth="public", website=True)
    def my_predict(self):
        user = request.env.user
        predict_scores = request.env['utc2.qld.predict'].search([])

        values = {}
        values.update({
            'predict_scores': predict_scores,
        })
        return request.render("qld_app.web_list_predict_score", values)


    @http.route(['/sinhvien/<model("utc2.qld.predict"):predict>'], type='http', auth="public", website=True)
    def qld_predict(self, predict, **kwargs):
        # if not predict.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        user = request.env.user
        predict_subject_ids = request.env['utc2.qld.predict.subjects']
        values = {}
        values.update({
            'predict': predict,
            'predict_scores_ids': predict.predict_scores_ids,
            'predict_subject_ids': predict_subject_ids,
        })
        return request.render("qld_app.website_predict_score", values)
