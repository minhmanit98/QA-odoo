# -*- coding: utf-8 -*-
import json

import base64
import requests
from addons.website_forum.controllers.main import WebsiteForum

from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_profile.controllers.main import WebsiteProfile
from odoo.addons.website_forum.controllers.main import WebsiteForum
from odoo.addons.website.models.ir_http import sitemap_qs2dom
import werkzeug.exceptions
import werkzeug.urls
import werkzeug.wrappers
from odoo.addons.http_routing.models.ir_http import slug

from .text_classification_utc2 import settings
import pickle as pickle
from .text_classification_utc2.preProcessData import FeatureExtraction, NLP

from .qa_ml.qa_ml import QA_ML


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

    # @http.route('/', type='http', auth="public", website=True)
    # def index(self, **kw):
    #     redirect = '/home'
    #     return http.redirect_with_hash(redirect)


class AuthSignupHome(Home):

    def get_avatar_default(self, email):
        response = requests.get('https://api.adorable.io/avatars/' + email).content
        return base64.b64encode(response)

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password')}
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


class WebsiteForum(WebsiteProfile):

    def sitemap_forum(env, rule, qs):
        Forum = env['forum.forum']
        dom = sitemap_qs2dom(qs, '/forum', Forum._rec_name)
        dom += env['website'].get_current_website().website_domain()
        for f in Forum.search(dom):
            loc = '/forum/%s' % slug(f)
            if not qs or qs.lower() in loc:
                yield {'loc': loc}

    # Post
    # --------------------------------------------------
    @http.route(['/forum/<model("forum.forum"):forum>/ask'], type='http', auth="user", website=True)
    def forum_post(self, forum, **post):
        user = request.env.user
        if not user.email or not tools.single_email_re.match(user.email):
            return werkzeug.utils.redirect(
                "/forum/%s/user/%s/edit?email_required=1" % (slug(forum), request.session.uid))
        values = self._prepare_user_values(forum=forum, searches={}, header={'ask_hide': True}, new_question=True)
        return request.render("website_forum.new_question", values)

    @http.route(['/forum/<model("forum.forum"):forum>/new',
                 '/forum/<model("forum.forum"):forum>/<model("forum.post"):post_parent>/reply'],
                type='http', auth="user", methods=['POST'], website=True)
    def post_create(self, forum, post_parent=None, **post):
        if post.get('content', '') == '<p><br></p>':
            return request.render('http_routing.http_error', {
                'status_code': _('Bad Request'),
                'status_message': post_parent and _('Reply should not be empty.') or _('Question should not be empty.')
            })

        content = post.get('content', False).lower()
        classifier = pickle.load(open(settings.LINEARSVC_TFIDF_MODEL, 'rb'))

        # tf-idf
        vectorizer = pickle.load(open(settings.VECTOR_EMBEDDING, 'rb'))
        data_features = []
        data_features.append(' '.join(NLP(text=content).get_words_feature()))
        features = vectorizer.transform(data_features)

        post_tag_ids = forum._tag_to_write_vals(post.get('post_tags', ''))
        tag_classifier_id = forum._get_tag_id_tag_name(classifier.predict(features)[0])
        if tag_classifier_id:
            post_tag_ids[0][2].append(tag_classifier_id)

        response_primary, response_message, line_id_primary = QA_ML(content)
        qa_ml_id = request.env['forum.post'].search([('content', '=', response_message)]).id

        if request.env.user.forum_waiting_posts_count:
            return werkzeug.utils.redirect("/forum/%s/ask" % slug(forum))

        # if post.get('is_published') and post.get('is_private') == False:
        #     post_incognito = False
        # else:
        #     post_incognito = True
        if not post_parent:
            new_question = request.env['forum.post'].create({
                'forum_id': forum.id,
                'name': post.get('post_name') or (post_parent and 'Re: %s' % (post_parent.name or '')) or '',
                'is_incognito': post.get('post_incognito') or False,
                'content': content,
                'qa_ml_answer': response_primary,
                'qa_ml_score': str(round(line_id_primary * 100, 2)),
                'qa_ml_id': qa_ml_id,
                'parent_id': post_parent and post_parent.id or False,
                'tag_ids': post_tag_ids
            })

            if qa_ml_id:
                new_question.with_env(request.env(user=request.env.ref('base.user_root').id)).message_post_with_view(
                    'qa_app.utc2_comment_qa_ml',
                    message_type='comment',
                    partner_ids=[(6, 0, [3])],
                    subtype_id=request.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment'),
                    subject=new_question.name)

        # qa_ml_answer = request.env['forum.post'].with_env(request.env(user=request.env.ref('base.user_root').id)).create({
        #     'forum_id': forum.id,
        #     'content': response_primary,
        #     'parent_id': new_question.id
        # })

        return werkzeug.utils.redirect(
            "/forum/%s/question/%s" % (slug(forum), post_parent and slug(post_parent) or new_question.id))

    @http.route(['/home'], type='http', auth="public", website=True, sitemap=sitemap_forum)
    def index(self, forum=None, tag=None, page=1, filters='all', my=None, sorting=None, search='', **post):
        # if not forum.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        forum = request.env['forum.forum'].search([('id', '=', 1)])
        Post = request.env['forum.post']
        domain = [('forum_id', '=', forum.id), ('parent_id', '=', False), ('state', '=', 'active')]
        if search:
            domain += ['|', ('name', 'ilike', search), ('content', 'ilike', search)]
        if tag:
            domain += [('tag_ids', 'in', tag.id)]
        if filters == 'unanswered':
            domain += [('child_ids', '=', False)]
        elif filters == 'solved':
            domain += [('has_validated_answer', '=', True)]
        elif filters == 'unsolved':
            domain += [('has_validated_answer', '=', False)]

        user = request.env.user

        if my == 'mine':
            domain += [('create_uid', '=', user.id)]
        elif my == 'followed':
            domain += [('message_partner_ids', '=', user.partner_id.id)]
        elif my == 'tagged':
            domain += [('tag_ids.message_partner_ids', '=', user.partner_id.id)]
        elif my == 'favourites':
            domain += [('favourite_ids', '=', user.id)]

        if sorting:
            # check that sorting is valid
            # retro-compatibily for V8 and google links
            try:
                Post._generate_order_by(sorting, None)
            except ValueError:
                sorting = False

        if not sorting:
            sorting = forum.default_order

        question_count = Post.search_count(domain)

        if tag:
            url = "/forum/%s/tag/%s/questions" % (slug(forum), slug(tag))
        else:
            url = "/forum/%s" % slug(forum)

        url_args = {
            'sorting': sorting
        }
        if search:
            url_args['search'] = search
        if filters:
            url_args['filters'] = filters
        pager = request.website.pager(url=url, total=question_count, page=page,
                                      step=5, scope=5,
                                      url_args=url_args)

        question_ids = Post.search(domain, limit=5, offset=pager['offset'], order=sorting)

        values = self._prepare_user_values(forum=forum, searches=post, header={'ask_hide': not forum.active})
        values.update({
            'main_object': tag or forum,
            'edit_in_backend': not tag,
            'question_ids': question_ids,
            'question_count': question_count,
            'pager': pager,
            'tag': tag,
            'filters': filters,
            'my': my,
            'sorting': sorting,
            'search': search,
        })
        return request.render("qa_app.home_forum_index", values)