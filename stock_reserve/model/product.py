# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2013 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    reservation_count = fields.Float(
        compute='_reservation_count',
        string='# Sales')

    @api.one
    def _reservation_count(self):
        self.reservation_count = sum(variant.reservation_count
                                     for variant in self.product_variant_ids)
        return self.reservation_count

    @api.multi
    def action_view_reservations(self):
        assert len(self._ids) == 1, "Expected 1 ID, got %r" % self._ids
        ref = 'stock_reserve.action_stock_reservation_tree'
        product_ids = self._get_products()
        prod_bj = self.pool.get('product.product')
        rent_service_ids = prod_bj.search(self._cr, self._uid, [('id', 'in', product_ids), ('rented_product_id', '!=', False)])
        if rent_service_ids:
            product_ids = [x for x in product_ids if x not in rent_service_ids]
            rented_prod_ids = [prod_bj.browse(self._cr, self._uid, x).rented_product_id.id for x in rent_service_ids]
            [product_ids.append(x) for x in rented_prod_ids if x not in product_ids]
        action_dict = self._get_act_window_dict(ref)
        action_dict['domain'] = [('product_id', 'in', product_ids)]
        action_dict['context'] = {
            'search_default_draft': 1,
            'search_default_reserved': 1
            }
        return action_dict


class ProductProduct(models.Model):
    _inherit = 'product.product'

    reservation_count = fields.Float(
        compute='_reservation_count',
        string='# Sales')

    @api.one
    def _reservation_count(self):
        domain = [('product_id', '=', self.id),
                  ('state', 'in', ['draft', 'assigned'])]
        rented_product = self.rented_product_id.id
        if rented_product:
            domain = [('product_id', '=', rented_product),
                  ('state', 'in', ['draft', 'assigned'])]
        reservations = self.env['stock.reservation'].search(domain)
        self.reservation_count = sum(reserv.product_qty
                                     for reserv in reservations)
        return self.reservation_count

    @api.multi
    def action_view_reservations(self):
        assert len(self._ids) == 1, "Expected 1 ID, got %r" % self._ids
        ref = 'stock_reserve.action_stock_reservation_tree'
        product_id = self._ids[0]
        rented_product = self.rented_product_id.id
        if rented_product:
            product_id = rented_product
        action_dict = self.product_tmpl_id._get_act_window_dict(ref)
        action_dict['domain'] = [('product_id', '=', product_id)]
        action_dict['context'] = {
            'search_default_draft': 1,
            'search_default_reserved': 1
            }
        return action_dict
