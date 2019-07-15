# © 2019 Jim Sports
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def _get_customer_prices_count(self):
        for tmpl in self:
            tmpl.customer_prices_count = len(tmpl.customer_tmpl_prices)

    customer_tmpl_prices = fields.One2many('customer.price', 'product_tmpl_id', 'Customer Prices')
    customer_prices_count = fields.Integer(compute='_get_customer_prices_count', string='#Prices')

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def _get_customer_prices_count(self):
        for prod in self:
            prod.customer_prices_count = len(prod.customer_product_prices)

    customer_product_prices = fields.One2many('customer.price', 'product_id', 'Customer Prices')
    product_item_ids = fields.One2many('product.pricelist.item', 'product_id', 'Pricelist Product Items')
    customer_prices_count = fields.Integer(compute='_get_customer_prices_count', string='#Prices')

    def _compute_product_price(self):
        """
        Al leer precios, buscar en precios específicos primero
        """
        self_super = self.env['product.product']
        partner_id = self._context.get('partner', False)
        qty = self._context.get('quantity', 1.0)

        if partner_id:
            for product in self:
                customer_price = self.env['customer.price'].get_customer_price(partner_id, product, qty)
                if customer_price:
                    product.price = customer_price
                else:
                    self_super += product

                print(customer_price)
        else:
            self_super = self

        return super(ProductProduct, self_super)._compute_product_price()