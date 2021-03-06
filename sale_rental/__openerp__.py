# -*- encoding: utf-8 -*-
##############################################################################
#
#    Rental module for Odoo
#    Copyright (C) 2014-2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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


{
    'name': 'Rental',
    'version': '0.1',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': 'Manage Rental of Products',
    'description': """
Rental
======

This module will allows you to rent products with OpenERP. On the form view of a stockable product or consumable, there is a wizard to generate the corresponding rental service. On the warehouse, you have two additionnal stock locations: *Rental In* (stock of products to rent) and *Rental Out* (products currently rented).

In a sale order line (form view, not tree view), if you select a rental service, you can :

* create a new rental with a start date and an end date: when the sale order is confirmed, it will generate a delivery order and an incoming shipment.

* extend an existing rental: the incoming shipment will be postponed to the end date of the extension.

In a sale order line, if you select a product that has a corresponding rental service, you can decide to sell the rented product that the customer already has. If the sale order is confirmed, the incoming shipment will be cancelled and a new delivery order will be created with a stock move from *Rental Out* to *Customers*.

To use the module, you need to have access to the form view of sale order lines. For that, you must add your user to one of these groups:

* Manage Product Packaging

* Properties on lines

A screencast that explains how to install, configure and use this module is available on Akretion's Youtube channel: https://www.youtube.com/watch?v=9o0QrGryBn8

Known limitations of the current implementation:

* the unit of measure of the rental services must be *Day* (we don't support the rental per hours / per week / per month...)

This module has been developped by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_start_end_dates', 'stock', 'stock_reserve'],
    'data': [
        'sale_view.xml',
        'stock_view.xml',
        'rental_view.xml',
        'rental_data.xml',
        'wizard/create_rental_product_view.xml',
        'product_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': ['rental_demo.xml'],
    'installable': True,
}
