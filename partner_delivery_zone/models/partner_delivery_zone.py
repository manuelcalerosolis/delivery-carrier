# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api


class PartnerDeliveryZone(models.Model):
    _name = 'partner.delivery.zone'
    _description = 'Partner delivery zone'

    name = fields.Char(
        string='Zone',
        required=True,
    )
    partner_zones_ids = fields.One2many(
        'delivery.zone.partner.line',
        'delivery_zone_id',
        string='Partner Zones Line',
        auto_join=True,
    )
    visit_ids = fields.One2many(
        'partner.delivery.zone.visit',
        'delivery_zone_id',
        string='Delivery Zone Visit',
        auto_join=True,
    )
    sale_order_ids = fields.One2many(
        'sale.order',
        'delivery_zone_id',
        string='Delivery Zone',
        auto_join=True,
    )

    @api.multi
    def set_values(self):
        super(PartnerDeliveryZone, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("partner.delivery.zone", self.code or '')

