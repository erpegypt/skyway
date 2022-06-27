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
    pass
    '''
    user = frappe.session.user
    lang = frappe.db.get_value("User", {'name': user}, "language")
    ## Auto Create Draft Installation Note On Submit
    new_doc = frappe.get_doc({
        "doctype": "Installation Note",
        "delivery_note": doc.name,
        "customer": doc.customer,
        "customer_group": doc.customer_group,
        "territory": doc.territory,
        "customer_address": doc.customer_address,
        "contact_person": doc.contact_person,
        "inst_date": doc.posting_date,
    })
    dn_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.item_name, a.description, a.qty, a.rate, a.amount
                                       from `tabDelivery Note Item` a join `tabDelivery Note` b
                                       on a.parent = b.name
                                       where b.name = '{name}'
                                   """.format(name=doc.name), as_dict=1)

    for c in dn_items:
        items = new_doc.append("items", {})
        items.idx = c.idx
        items.item_code = c.item_code
        items.item_name = c.item_name
        items.description = c.description
        items.qty = c.qty
        items.rate = c.rate
        items.amount = c.amount
        items.prevdoc_detail_docname = c.name
        items.prevdoc_docname = doc.name
        items.prevdoc_doctype = "Delivery Note"

    new_doc.insert(ignore_permissions=True)
    if lang == "ar":
        frappe.msgprint("  تم إنشاء إذن تركيب رقم " + new_doc.name)
    else:
        frappe.msgprint(" Installation Note " + new_doc.name + " Created ")
    '''
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
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
