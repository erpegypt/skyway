# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MinimumSellingItems(Document):

	@frappe.whitelist()
	def get_items(self):
		if self.get_items_from == "Item Group":
			items = frappe.db.sql(""" select item_code, item_name, item_group, brand from `tabItem` where `tabItem`.disabled = 0 and `tabItem`.is_sales_item = 1 and `tabItem`.item_group = '{item_group}'
										 """.format(item_group=self.item_group), as_dict=1)

			if items:
				for x in items:
					y = self.append("commission_item", {})
					y.item = x.item_code
					y.item_name = x.item_name
					y.item_group = x.item_group
					y.brand = x.brand

		if self.get_items_from == "Brand":
			items = frappe.db.sql(""" select item_code, item_name, item_group, brand from `tabItem` where `tabItem`.disabled = 0 and `tabItem`.is_sales_item = 1 and `tabItem`.brand = '{brand}'
										 """.format(brand=self.brand), as_dict=1)

			if items:
				for x in items:
					y = self.append("commission_item", {})
					y.item = x.item_code
					y.item_name = x.item_name
					y.item_group = x.item_group
					y.brand = x.brand

		if self.get_items_from == "Item Group-Brand":
			items = frappe.db.sql(""" select item_code, item_name, item_group, brand from `tabItem` where `tabItem`.disabled = 0 and `tabItem`.is_sales_item = 1 and `tabItem`.brand = '{brand}' and `tabItem`.item_group = '{item_group}'
										 """.format(brand=self.brand, item_group=self.item_group), as_dict=1)

			if items:
				for x in items:
					y = self.append("commission_item", {})
					y.item = x.item_code
					y.item_name = x.item_name
					y.item_group = x.item_group
					y.brand = x.brand
	@frappe.whitelist()
	def validate(self):
		self.get_items_from = ""
		self.item_group = ""
