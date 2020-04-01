

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import base64
import requests
from odoo.addons.base.models.res_partner import Partner


class ResUsers(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('import_file'):
            self._check_import_consistency(vals_list)
        for vals in vals_list:
            if vals.get('website'):
                vals['website'] = self._clean_website(vals['website'])
            if vals.get('parent_id'):
                vals['company_name'] = False
        partners = super(Partner, self).create(vals_list)

        if self.env.context.get('_partners_skip_fields_sync'):
            return partners

        for partner, vals in zip(partners, vals_list):
            partner._fields_sync(vals)
            partner._handle_first_contact_creation()
        return partners