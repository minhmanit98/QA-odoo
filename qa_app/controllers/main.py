# -*- coding: utf-8 -*-
import json

import base64
import json
import math
import re
import requests
from addons.portal.controllers import web
from werkzeug import urls

from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo.http import content_disposition, Controller, request, route
from odoo.tools import consteq
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.website.controllers.main import Website

class UTC2Forum(Controller):

    def _prepare_portal_layout_values(self):
        # get customer sales rep
        sales_user = False
        partner = request.env.user.partner_id
        if partner.user_id and not partner.user_id._is_public():
            sales_user = partner.user_id

        return {
            'sales_user': sales_user,
            'page_name': 'home',
            'archive_groups': [],
        }

    @route(['/my/account/password'], type='http', auth='user', website=True)
    def password(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.check_change_password(post)
            try:
                request.env['res.users'].change_password(post['old_pwd'], post['new_password'])
            except UserError as e:
                msg = e.name
                error["old_pwd"] = 'error'
                error_message.append(msg)
            except AccessDenied as e:
                msg = e.args[0]
                if msg == AccessDenied().args[0]:
                    msg = _('The old password you provided is incorrect, your password was not changed.')
                error["old_pwd"] = 'error'
                error_message.append(msg)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if redirect:
                return request.redirect(redirect)
            return request.redirect('/web/session/logout?redirect=/')
        #     Thêm dialog thông bảo đổi mật khẩu thành công
        response = request.render("qa_app.utc2_password", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def check_change_password(self, data):
        error = dict()
        error_message = []
        CHANGE_PASSSWORD_FIELDS = ["old_pwd", "new_password", "confirm_pwd"]
        # Validation
        for field_name in CHANGE_PASSSWORD_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('confirm_pwd') != data.get('new_password'):
            error["confirm_pwd"] = 'error'
            error_message.append(_('The confirmation password is incorrect ! Please enter a confirm password.'))

        return error, error_message


class Website(Home):

    @http.route(website=True, auth="public", sitemap=False)
    def web_login(self, redirect=None, *args, **kw):
        response = super(Website, self).web_login(redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                redirect = '/forum'
            return http.redirect_with_hash(redirect)
        return response


class AuthSignupHome(Home):

    def get_avatar_default(self, email):
        response = requests.get('https://api.adorable.io/avatars/' + email).content
        return base64.b64encode(response)

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
        values['image_1920'] = self.get_avatar_default(qcontext.get('login'))
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

