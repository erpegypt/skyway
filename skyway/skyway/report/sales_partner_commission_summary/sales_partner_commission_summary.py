# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters, columns)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Sales Invoice"),
			"options": "Sales Invoice",
			"fieldname": "name",
			"fieldtype": "Link",
			"width": 120
		},
		{
			"label": _("Customer"),
			"options": "Customer",
			"fieldname": "customer",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Territory"),
			"options": "Territory",
			"fieldname": "territory",
			"fieldtype": "Link",
			"width": 100
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 110
		},
		{
			"label": _("Item"),
			"options": "Item",
			"fieldname": "item_code",
			"fieldtype": "Link",
			"width": 100
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"label": _("Commission"),
			"fieldname": "sales_partner_commission",
			"fieldtype": "Currency",
			"width": 160
		},


		{
			"label": _("Sales Partner"),
			"options": "Sales Partner",
			"fieldname": "sales_partner",
			"fieldtype": "Link",
			"width": 140
		}
	]

	return columns
def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data


def get_item_price_qty_data(filters):
	sales_partner = filters.get("sales_partner")
	to_date = filters.get("to_date")
	from_date = filters.get("from_date")

	invoices = frappe.db.sql(""" SELECT  `tabSales Invoice`.name as name ,
										`tabSales Invoice`.customer as customer,
										`tabSales Invoice`.territory as territory,
										`tabSales Invoice`.sales_partner as sales_partner,
										`tabSales Invoice`.posting_date as posting_date,
										`tabSales Invoice Item`.item_code as item_code,
										`tabSales Invoice Item`.item_group as item_group,
										`tabSales Invoice Item`.brand as brand,
										`tabSales Invoice Item`.discount_percentage as discount_percentage,
										`tabSales Invoice Item`.amount as amount														
										from `tabSales Invoice` INNER JOIN `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
										where 
										`tabSales Invoice`.docstatus !=0 
										and `tabSales Invoice`.docstatus !=2 
										and `tabSales Invoice`.posting_date BETWEEN '{from_date}' and '{to_date}'
										and `tabSales Invoice`.outstanding_amount = 0
										and `tabSales Invoice`.paid = 0 
										and `tabSales Invoice`.sales_partner = '{sales_partner}' 
											""".format(from_date=from_date, to_date=to_date, sales_partner=sales_partner), filters, as_dict=1)

	result = []
	if invoices:
		for item_dict in invoices:
			data = {
				'sales_partner': item_dict.sales_partner,
				'name': item_dict.name,
				'customer': item_dict.customer,
				'territory': item_dict.territory,
				'posting_date': item_dict.posting_date,
				'item_code': item_dict.item_code,
				#'per': commission.commission_percent,
				'amount': item_dict.amount,
				#'sales_partner_commission': (commission_percen1 * amount) / 100,

			}
			commission_perc = frappe.db.sql(""" select 
													ifnull(`tabCommission Details`.commission_percent,0) as commission_percent
													from `tabCommission Details` 
													join `tabCommission Role` on `tabCommission Details`.parent = `tabCommission Role`.name
													join `tabCommission Item` on `tabCommission Item`.parent = `tabCommission Role`.name
													where 
													`tabCommission Item`.item = '{item}'
													and  '{discount_percentage}' >= `tabCommission Details`.discount_from 
													and  '{discount_percentage}' <= `tabCommission Details`.discount_to
													""".format(item=item_dict.item_code,discount_percentage=item_dict.discount_percentage),as_dict=True)

			for x in commission_perc:
				data['per']= x.commission_percent
				data['sales_partner_commission']= (x.commission_percent * item_dict.amount) / 100

			result.append(data)

	return result

	'''
	for comm in invoices:
		discount_percentage = comm.discount_percentage
		invoice_name = comm.name
		customer = comm.customer
		posting_date = comm.posting_date
		item_code = comm.item_code
		amount = comm.amount

		role_item_parent = frappe.db.sql(""" select `tabCommission Item`.item as item_code ,
													`tabCommission Item`.parent as parent
													from `tabCommission Item` 
													where 
													`tabCommission Item`.item = '{role_item}'
													""".format( role_item = comm.item_code),  as_dict=True)


		for par in role_item_parent:
			commission_perc = frappe.db.sql(""" select `tabCommission Details`.discount_from as discount_from ,
														`tabCommission Details`.discount_to as discount_to ,
														ifnull(`tabCommission Details`.commission_percent,0) as commission_percent
														from `tabCommission Details` join `tabCommission Role` on `tabCommission Details`.parent = `tabCommission Role`.name
														where 
														`tabCommission Role`.name = '{parent}'
														and  '{discount_percentage}' >= `tabCommission Details`.discount_from 
														and  '{discount_percentage}' <= `tabCommission Details`.discount_to
														""".format( parent = par.parent, discount_percentage = comm.discount_percentage ),  as_dict=True)

			for commission in commission_perc:
				commission_percen1 = commission.commission_percent
				per = commission.commission_percent


	'''