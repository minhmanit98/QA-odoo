# -*- coding: utf-8 -*-
import json

import base64
import requests
import werkzeug.exceptions
import werkzeug.urls
import werkzeug.wrappers
from odoo.addons.website_profile.controllers.main import WebsiteProfile

from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo.http import content_disposition, Controller, request, route


class UTC2Predict(Controller):

    def _prepare_user_values(self, **kwargs):
        values = super(UTC2Predict, self)._prepare_user_values(**kwargs)
        if kwargs.get('predict'):
            values['predict'] = kwargs.get('predict')
        return values

    @http.route(['/sinhvien/create'], type='http', auth="user", csrf=False, methods=['POST'], website=True)
    def create_predict(self, **post):
        user = request.env.user
        msv_predict = post.get('msv_predict')
        if msv_predict:
            if request.env['utc2.qld.students'].search_count([('name', '=', msv_predict)]) > 0:
                predict_scores = request.env['utc2.qld.predict'].create({
                    'student_id': request.env['utc2.qld.students'].search([('name', '=', msv_predict)], limit=1).id
                })
            else:
                return request.render('http_routing.http_error', {
                    'status_code': _('Bad Request'),
                    'status_message': _('Mã sinh viên không có trên hệ thống') or _(
                        'Mã sinh viên này không được hỗ trợ')
                })
        else:
            return request.render('http_routing.http_error', {
                'status_code': _('Bad Request'),
                'status_message': _('Mời nhập mã sinh viên') or _(
                    'Mã sinh viên không được để trống')
            })
        return werkzeug.utils.redirect(
            "/sinhvien/%s" % (predict_scores.id))


    @http.route(['/sinhvien'], type='http', auth="public", website=True)
    def my_predict(self):
        user = request.env.user
        predict_scores = request.env['utc2.qld.predict'].search([('create_uid', '=', user.id)])
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

    @http.route(['/sinhvien/<model("utc2.qld.predict"):predict>'], type='http', auth="public", website=True)
    def qld_predict(self, predict, **kwargs):
        # if not predict.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        user = request.env.user
        subject_search = kwargs.get('subject_search')
        subject_search_id = request.env['utc2.qld.subjects'].search(
            [('name_display', '=', subject_search)])
        predict_subject_ids = request.env['utc2.qld.predict.subjects']
        values = {}
        values.update({
            'predict': predict,
            'predict_scores_ids': predict.predict_scores_ids,
            'predict_subject_ids': predict_subject_ids,
            'subject_search_id': subject_search_id,
        })
        return request.render("qld_app.website_predict_score", values)

    @http.route(['/sinhvien/<model("utc2.qld.predict"):predict>/delete'],
                type='http', auth="user", methods=['POST'], website=True)
    def delete_predict(self, predict, **post):
        # if not predict.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        predict.unlink()
        return werkzeug.utils.redirect(
            "/sinhvien")

    @http.route(['/sinhvien/<model("utc2.qld.predict"):predict>/<model("utc2.qld.predict.scores"):score>/delete'], type='http', auth="user", methods=['POST'], website=True)
    def delete_predict_scores(self, predict, score, **post):
        # if not predict.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        score.unlink()
        return werkzeug.utils.redirect(
            "/sinhvien/%s" % (predict.id))

    @http.route(['/sinhvien/<model("utc2.qld.predict"):predict>/update'],
                type='http', auth="user", methods=['POST'], website=True)
    def update_predict(self, predict, **post):
        # if not predict.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        predict.action_get_scores()
        return werkzeug.utils.redirect(
            "/sinhvien/%s" % (predict.id))

    @http.route(['/sinhvien/<model("utc2.qld.predict"):predict>/<model("utc2.qld.predict.scores"):score>/add_subject'],
                type='http', auth="user", methods=['POST'], website=True)
    def add_subject_predict(self, predict, score, **post):
        # if not predict.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        predict_subject_ids = post.get('predict_subject_ids')
        score.predict_subject_id = request.env['utc2.qld.predict.subjects'].search([('id', '=', predict_subject_ids)]).id
        # score.write({'predict_subject_id': request.env['utc2.qld.predict.subjects'].browse(predict_subject_ids).id})
        return werkzeug.utils.redirect(
            "/sinhvien/%s" % (predict.id))

    @http.route(['/sinhvien/<model("utc2.qld.predict"):predict>/add_scores'],
                type='http', auth="user", methods=['POST'], website=True)
    def add_subject_scores(self, predict, **post):
        # if not predict.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        subject_search = post.get('subject_search')
        predict_subject_id = request.env['utc2.qld.subjects'].search(
            [('name_display', '=', subject_search)]).id
        # score.write({'predict_subject_id': request.env['utc2.qld.predict.subjects'].browse(predict_subject_ids).id})
        return werkzeug.utils.redirect(
            "/sinhvien/%s" % (predict.id))

    @http.route(['/sinhvien/<model("utc2.qld.predict"):predict>/save'],
                type='http', auth="user", methods=['POST'], website=True)
    def save_score_4custorm(self, predict, **post):
        # if not predict.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        scores = request.env['utc2.qld.predict.scores']
        for field in post:
            score_id = post[field].split('/')[0]
            score_custom = post[field].split('/')[1]
            scores.search([('id', '=', score_id)]).scores_4custom = float(score_custom)
        scores.predict_id._compute_scores_4cus()
        # score.write({'predict_subject_id': request.env['utc2.qld.predict.subjects'].browse(predict_subject_ids).id})
        return werkzeug.utils.redirect(
            "/sinhvien/%s" % (predict.id))
