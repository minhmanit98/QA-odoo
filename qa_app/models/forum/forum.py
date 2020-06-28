# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError, AccessError

class Tags(models.Model):
    _inherit = "forum.tag"
    parent_id = fields.Many2one('forum.tag', string='Parent Tag', ondelete='restrict')
    parent_path = fields.Char(index=True)
    # Optional, but good to have
    child_ids = fields.One2many('forum.tag', 'parent_id', string='Subtag')
    highlighted_id = fields.Reference([('forum.post', 'Post')], 'Tags Highlight')
    document_page_ids = fields.One2many('document.page', 'tag_id', 'Câu trả lời tùy chỉnh')


class Post(models.Model):
    _inherit = "forum.post"

    @api.model
    @api.depends('is_incognito')
    def _compute_user_incognito(self):
        for record in self:
            if record.is_incognito:
                record.user_incognito = self.env.ref('qa_app.user_private')
            else:
                record.user_incognito = False

    @api.model
    @api.depends('tag_ids')
    def _compute_tag_main(self):
        for record in self:
            record.tag_main = record.tag_ids and record.tag_ids[0] or False

    is_incognito = fields.Boolean('Private post', default=False, readonly=True)
    user_incognito = fields.Many2one('res.users', string='User Incognito', compute=_compute_user_incognito)
    tag_main = fields.Many2one('forum.tag', string='Tag main', compute=_compute_tag_main, store=True)
    qa_ml_answer = fields.Char('QA ML Answer', default=False, readonly=True)
    qa_ml_score = fields.Char('QA Score', default=False, readonly=True)
    qa_ml_id = fields.Many2one('forum.post', string='QA ML id', default=False)

    def post_notification(self):
        for post in self:
            tag_partners = post.tag_ids.sudo().mapped('message_partner_ids')

            if post.state == 'active' and post.parent_id:
                post.parent_id.message_post_with_view(
                    'website_forum.forum_post_template_new_answer',
                    subject=_('Re: %s') % post.parent_id.name,
                    partner_ids=[(4, p.id) for p in tag_partners],
                    subtype_id=self.env['ir.model.data'].xmlid_to_res_id('website_forum.mt_answer_new'))
            elif post.state == 'active' and not post.parent_id and post.is_incognito:
                post.message_post_with_view(
                    'website_forum.forum_post_template_new_question',
                    subject=post.name,
                    partner_ids=[(4, p.id) for p in tag_partners],
                    subtype_id=self.env['ir.model.data'].xmlid_to_res_id('website_forum.mt_question_new'))
            elif post.state == 'pending' and not post.parent_id and post.is_incognito:
                # TDE FIXME: in master, you should probably use a subtype;
                # however here we remove subtype but set partner_ids
                partners = post.sudo().message_partner_ids | tag_partners
                partners = partners.filtered(lambda partner: partner.user_ids and any(user.karma >= post.forum_id.karma_moderate for user in partner.user_ids))

                post.message_post_with_view(
                    'website_forum.forum_post_template_validation',
                    subject=post.name,
                    partner_ids=partners.ids,
                    subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'))
        return True


class Forum(models.Model):
    _inherit = 'forum.forum'

    def _get_tag_id_tag_name(self, tag_name):
        Tag = self.env['forum.tag']
        tag_id = Tag.search([('name', '=', tag_name)], limit=1).id
        return tag_id
