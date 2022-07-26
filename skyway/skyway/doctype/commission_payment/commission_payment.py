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
	pass
	def validate(self):
		if self.total_payable ==0:
			self.get_details()

	def on_submit(self):
		self.update_invoice_partner1()
		self.make_jv_partner()

	def on_cancel(self):
		self.update_invoice_partner0()
	
	@frappe.whitelist()
	def get_details(self):
		invoices =frappe.db.sql(""" select `tabSales Invoice`.name as name ,
									`tabSales Invoice`.customer as customer,
									`tabSales Invoice`.posting_date as posting_date,
									`tabSales Invoice Item`.item_code as item_code,
									`tabSales Invoice Item`.item_group as item_group,
									`tabSales Invoice Item`.brand as brand,
									`tabSales Invoice Item`.amount as amount														
									from `tabSales Invoice` INNER JOIN `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
									where 
									`tabSales Invoice`.docstatus = 1 
									and `tabSales Invoice`.posting_date BETWEEN '{from_date}' and '{to_date}'
									and paid = 0 
									and sales_partner = '{sales_partner}' 
									""".format( sales_partner=self.sales_partner,from_date = self.from_date, to_date= self.to_date),  as_dict=True)
		for comm in invoices:
			row = self.append('commission_table', {})
			row.sales_invoice = comm.name
			row.customer = comm.customer
			row.posting_date = comm.posting_date
			row.item = comm.item_code
			row.amount = comm.amount
			





	def update_invoice_partner1(self):
		for inv in self.commission_details:
			frappe.db.sql("""  update `tabSales Invoice` set paid = 1 where name = %s """,inv.sales_invoice)

	def update_invoice_partner0(self):
		for inv in self.commission_details:
			frappe.db.sql("""  update `tabSales Invoice` set paid = 0 where name = %s """,inv.sales_invoice)
	
	def make_jv_partner(self):
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
			"posting_date": self.posting_date,
			"accounts": accounts,
			"cheque_no": self.name,
			"cheque_date": self.posting_date,
			"user_remark": _('Accrual Journal Entry for Sales Commission for {0}').format(self.sales_partner),
			"total_debit": self.total_payable,
			"total_credit": self.total_payable,
			"remark":  _('Accrual Journal Entry for Sales Commission for {0}').format(self.sales_partner)

		})
		doc.insert()
		doc.submit()