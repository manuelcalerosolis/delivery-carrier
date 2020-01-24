# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api

import logging


class DeliveryZonePartnerRel(models.Model):
    _name = 'delivery_zone.partner_rel'
    _table = 'delivery_zone_partner_rel'
    _description = 'Partner delivery zone relation'
    _rec_name = 'partner_id'

    delivery_zone_id = fields.Many2one(
        'partner.delivery.zone',
        string='Delivery Zone',
        ondelete='cascade',
        required=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        ondelete='cascade',
        required=True
    )

    @api.multi
    def _get_next_sequence(self):
        logging.info("Next sequence*******************")
        return self.env['ir.sequence'].next_by_code('res.partner.delivery.zone')

    sequence = fields.Integer(
        string='Sequence',
        default=_get_next_sequence,
    )
    display_name = fields.Char(
        related='partner_id.display_name',
        store=False,
        readonly=True,
    )
    street = fields.Char(
        related='partner_id.street',
        store=False,
        readonly=True,
    )
    street2 = fields.Char(
        related='partner_id.street2',
        store=False,
        readonly=True,
    )
    city = fields.Char(
        related='partner_id.city',
        store=False,
        readonly=True,
    )
    zip = fields.Char(
        related='partner_id.zip',
        store=False,
        readonly=True,
    )
    phone = fields.Char(
        related='partner_id.phone',
        store=False,
        readonly=True,
    )

    _sql_constraints = [
        ('unique_delivery_zone',
         'unique (delivery_zone_id, partner_id)',
         'Partner cannot be subscribed multiple times to the same list!')
    ]

    @api.model
    def create(self, vals):
        logging.info("Create*******************")
        logging.info(vals)
        return super(DeliveryZonePartnerRel, self).create(vals)

    @api.multi
    def write(self, vals):
        logging.info("Write*******************")
        logging.info(vals)
        return super(DeliveryZonePartnerRel, self).write(vals)


class PartnerDeliveryZone(models.Model):
    _name = 'partner.delivery.zone'
    _description = 'Partner delivery zone'

    name = fields.Char(
        string='Zone',
        required=True,
    )
    partner_ids = fields.Many2many(
        'res.partner',
        'delivery_zone_partner_rel',
        'delivery_zone_id',
        'partner_id',
        string='Partners',
    )
    partner_zones_ids = fields.One2many(
        'delivery_zone.partner_rel',
        'delivery_zone_id',
        string='Partner Zones',
        auto_join=True,
    )
    visit_ids = fields.One2many(
        'partner.delivery.zone.visit',
        'delivery_zone_id',
        string='Delivery Zone Visit',
        auto_join=True,
    )

    @api.multi
    def set_values(self):
        super(PartnerDeliveryZone, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("partner.delivery.zone", self.code or '')

    def get_partners(self):
        for partner in self.partner_ids:
            logging.info("#"*80)
            logging.info(partner)
            logging.info(partner.name)


