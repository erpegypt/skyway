# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe, erpnext, json
from frappe.utils import cstr, flt, fmt_money, formatdate, getdate, nowdate, cint, get_link_to_form
from frappe import msgprint, _, scrub
from erpnext.controllers.accounts_controller import AccountsController
from dateutil.relativedelta import relativedelta
from erpnext.accounts.utils import get_balance_on, get_stock_accounts, get_stock_and_account_balance, \
	get_account_currency
from erpnext.accounts.party import get_party_account
from erpnext.hr.doctype.expense_claim.expense_claim import update_reimbursed_amount
from erpnext.accounts.doctype.invoice_discounting.invoice_discounting \
	import get_party_account_based_on_invoice_discounting
from erpnext.accounts.deferred_revenue import get_deferred_booking_accounts
from frappe.model.document import Document
from six import string_types, iteritems

class CommissionPayment(Document):
	def validate(self):
		self.commission_table ={}
		self.get_details()
		self.get_minimum()
		self.edit_commission()

	def on_submit(self):
		self.update_invoice_partner1()
		self.make_jv_partner()

	def on_cancel(self):
		self.update_invoice_partner0()
	
	@frappe.whitelist()
	def get_details(self):
		self.target_amount = 0
		self.total_payable = 0
		self.total_selling = 0
		self.minimum_selling_item_percent = 0
		target_amount = frappe.db.get_value('Sales Partner', {'name': self.sales_partner}, 'target_amount')
		self.target_amount = target_amount
		self.commission_table ={}
		
		invoices =frappe.db.sql(""" select `tabSales Invoice`.name as name ,
									`tabSales Invoice`.customer as customer,
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
									""".format( sales_partner=self.sales_partner,from_date = self.from_date, to_date= self.to_date),  as_dict=True)
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
															from `tabCommission Details` 
															where 
															`tabCommission Details`.parent = '{parent}'
															and  '{discount_percentage}' >= `tabCommission Details`.discount_from 
															and  '{discount_percentage}' <= `tabCommission Details`.discount_to
															""".format( parent = par.parent, discount_percentage = comm.discount_percentage ),  as_dict=True)

				for commission in commission_perc:
					commission_percen1 = 0
					commission_percen1 = commission.commission_percent

				row = self.append('commission_table', {})
				row.sales_invoice = invoice_name
				row.customer = customer
				row.posting_date = posting_date
				row.item = item_code
				row.discount_percentage = discount_percentage
				row.amount = amount
				row.commissions_percent = 0
				row.commissions_percent = commission_percen1
				row.commission_amount = 0
				row.commission_amount = (commission_percen1 * amount) / 100
		for row_commission_amount in self.commission_table:
			self.total_payable += row_commission_amount.commission_amount
			self.total_selling += row_commission_amount.amount


	def update_invoice_partner1(self):
		for inv in self.commission_table:
			frappe.db.sql("""  update `tabSales Invoice` set paid = 1 where name = %s """,inv.sales_invoice)

	def update_invoice_partner0(self):
		for inv in self.commission_table:
			frappe.db.sql("""  update `tabSales Invoice` set paid = 0 where name = %s """,inv.sales_invoice)
	
	def make_jv_partner(self):
		mini_payable_amount = (self.target_amount * self.minimum_selling_percent) / 100
		if self.total_payable >= mini_payable_amount:
			company = frappe.db.get_value("Company", frappe.db.get_value("Global Defaults", None, "default_company"),"company_name")
			accounts = [
				{
					"account": self.sales_partner_account,
					"debit_in_account_currency": self.total_payable,
					"exchange_rate": "1"
				},
				{
					"account": self.payment_account,
					"credit_in_account_currency": self.total_payable,
					"exchange_rate": "1"
				}
			]
			doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"commission_payment": self.name,
				"company": company,
				"posting_date": self.to_date,
				"accounts": accounts,
				"cheque_no": self.name,
				"cheque_date": self.to_date,
				"user_remark": _('Accrual Journal Entry for Sales Commission for {0}').format(self.sales_partner),
				"total_debit": self.total_payable,
				"total_credit": self.total_payable,
				"remark":  _('Accrual Journal Entry for Sales Commission for {0}').format(self.sales_partner)

			})
			doc.insert()
			doc.submit()
			frappe.msgprint( "Journal Entry " + doc.name + "  Created For Cmmission Pay")
		else:
			frappe.msgprint( "Total Monthly Sales Amount Is Less Than Monthly Target Amount")

	def get_minimum(self):
		total_minimum = 0
		mini_item_parent = frappe.db.sql(""" select `tabMinimum Item`.item as item_code,
													`tabMinimum Item`.item_name as item_name
												from `tabMinimum Item` join `tabMinimum Selling Items` on `tabMinimum Item`.parent = `tabMinimum Selling Items`.name
													where `tabMinimum Selling Items`.disabled = 0 
													and  `tabMinimum Selling Items`.docstatus = 1
													""".format(sales_partner=self.sales_partner, from_date=self.from_date,
														   to_date=self.to_date ), as_dict=True)
		for x in mini_item_parent:
			mini_item_code = x.item
			mini_item_name = x.item_name
			invoices = frappe.db.sql(""" select `tabSales Invoice`.name as name ,
												`tabSales Invoice`.customer as customer,
												`tabSales Invoice`.posting_date as posting_date,
												`tabSales Invoice Item`.item_code as item_code,
												`tabSales Invoice Item`.item_name as item_name,
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
												and  `tabSales Invoice Item`.item_name = '{item}'
												""".format(sales_partner=self.sales_partner, from_date=self.from_date,
														   to_date=self.to_date, item=mini_item_name ), as_dict=True)
			for y in invoices:
				mini_payable_amount = (self.target_amount * self.minimum_selling_percent) / 100
				total_minimum += y.amount
				self.minimum_selling_item_percent = ( total_minimum / mini_payable_amount  )*100

	def edit_commission(self):
		self.total_payable = 0
		self.total_selling =0
		for x in self.commission_table:
			if x.commissions_percent <= 1:
				if self.minimum_selling_item_percent < 25 and self.minimum_selling_item_percent >= 20 and x.item in ["1","2","34","35","36","50"]:
					x.commissions_percent -= 0.1
				if self.minimum_selling_item_percent < 20 and self.minimum_selling_item_percent >= 15 and x.item in ["1","2","34","35","36","50"]:
					x.commissions_percent -= 0.2
				if self.minimum_selling_item_percent < 15 and self.minimum_selling_item_percent >= 10 and x.item in ["1","2","34","35","36","50"]:
					x.commissions_percent -= 0.3
				if self.minimum_selling_item_percent < 10 and self.minimum_selling_item_percent >= 5 and x.item in ["1","2","34","35","36","50"]:
					x.commissions_percent -= 0.4
				if self.minimum_selling_item_percent < 5 and self.minimum_selling_item_percent >= 0 and x.item in ["1","2","34","35","36","50"]:
					x.commissions_percent -= 0.5
				x.commission_amount= (x.commissions_percent * x.amount) / 100
			self.total_payable += x.commission_amount
			self.total_selling += x.amount

