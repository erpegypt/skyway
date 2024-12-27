from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    if doc.reference_name:
        frappe.db.set_value('Ticket', doc.reference_name, "payment_entry_status", doc.status)
@frappe.whitelist()
def on_cancel(doc, method=None):
    if doc.reference_name:
        frappe.db.set_value('Ticket', doc.reference_name, "payment_entry", "")
        frappe.db.set_value('Ticket', doc.reference_name, "payment_entry_status", "")

@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
