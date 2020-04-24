# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, exceptions
from odoo.tools.translate import html_translate


class KarmaRank(models.Model):
    _inherit = 'gamification.karma.rank'

    image_rank = fields.Binary('Image Rank')


