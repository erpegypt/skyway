from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def price_before_insert(doc, method=None):
    pass
@frappe.whitelist()
def price_after_insert(doc, method=None):
    pass
@frappe.whitelist()
def price_onload(doc, method=None):
    pass
@frappe.whitelist()
def price_before_validate(doc, method=None):
    pass
@frappe.whitelist()
def price_validate(doc, method=None):
    pass
@frappe.whitelist()
def price_before_save(doc, method=None):
    pass
@frappe.whitelist()
def price_on_update(doc, method=None):
    pass
