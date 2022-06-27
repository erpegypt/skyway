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
    user = frappe.session.user
    lang = frappe.db.get_value("User", {'name': user}, "language")

    ## Auto Create Project On Submit
    if doc.auto_create_project_on_submit:
        new_doc2 = frappe.get_doc({
            "doctype": "Project",
            "project_name": str(doc.customer_name) + " - " + str(doc.customer_address),
            "customer": doc.customer,
            "sales_order": doc.name,
            "status": "Open",
            "expected_start_date": doc.transaction_date,
            "priority": "High",
            "cost_center": "Main - Sky",
        })
        new_doc2.insert(ignore_permissions=True)
        doc.project = new_doc2.name
        if lang == "ar":
            frappe.msgprint("  تم إنشاء مشروع رقم " + new_doc2.name)
        else:
            frappe.msgprint(" Project " + new_doc2.name + " Created ")

    ## Auto Create Draft Delivery Note On Submit
    new_doc = frappe.get_doc({
        "doctype": "Delivery Note",
        "customer": doc.customer,
        "customer_group": doc.customer_group,
        "territory": doc.territory,
        "sales_order": doc.name,
        "posting_date": doc.delivery_date,
        "po_no": doc.po_no,
        "po_date": doc.po_date,
        "customer_address": doc.customer_address,
        "shipping_address_name": doc.shipping_address_name,
        "dispatch_address_name": doc.dispatch_address_name,
        "company_address": doc.company_address,
        "contact_person": doc.contact_person,
        "tax_id": doc.tax_id,
        "currency": doc.currency,
        "conversion_rate": doc.conversion_rate,
        "selling_price_list": doc.selling_price_list,
        "price_list_currency": doc.price_list_currency,
        "plc_conversion_rate": doc.plc_conversion_rate,
        "ignore_pricing_rule": doc.ignore_pricing_rule,
        "set_warehouse": doc.set_warehouse,
        "tc_name": doc.tc_name,
        "terms": doc.terms,
        "apply_discount_on": doc.apply_discount_on,
        "base_discount_amount": doc.base_discount_amount,
        "additional_discount_percentage": doc.additional_discount_percentage,
        "discount_amount": doc.discount_amount,
        "project": doc.project,
        "cost_center": "Main - Sky",
    })

    so_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.item_name, a.description, a.qty, a.stock_qty, a.uom, a.stock_uom, a.conversion_factor, a.rate, a.amount,
                                       a.price_list_rate, a.base_price_list_rate, a.base_rate, a.base_amount, a.net_rate, a.net_amount, a.margin_type, a.margin_rate_or_amount, a.rate_with_margin,
                                       a.discount_percentage, a.discount_amount, a.base_rate_with_margin, a.item_tax_template
                                       from `tabSales Order Item` a join `tabSales Order` b
                                       on a.parent = b.name
                                       where b.name = '{name}'
                                   """.format(name=doc.name), as_dict=1)

    for c in so_items:
        items = new_doc.append("items", {})
        items.idx = c.idx
        items.item_code = c.item_code
        items.item_name = c.item_name
        items.description = c.description
        items.qty = c.qty
        items.uom = c.uom
        items.stock_uom = c.stock_uom
        items.conversion_factor = c.conversion_factor
        items.price_list_rate = c.price_list_rate
        items.base_price_list_rate = c.base_price_list_rate
        items.base_rate = c.base_rate
        items.base_amount = c.base_amount
        items.rate = c.rate
        items.net_rate = c.net_rate
        items.net_amount = c.net_amount
        items.amount = c.amount
        items.margin_type = c.margin_type
        items.margin_rate_or_amount = c.margin_rate_or_amount
        items.rate_with_margin = c.rate_with_margin
        items.discount_percentage = c.discount_percentage
        items.discount_amount = c.discount_amount
        items.base_rate_with_margin = c.base_rate_with_margin
        items.item_tax_template = c.item_tax_template
        items.so_detail = c.name
        items.against_sales_order = doc.name

    so_taxes = frappe.db.sql(""" select a.charge_type, a.row_id, a.account_head, a.description, a.included_in_print_rate, a.included_in_paid_amount, a.rate, a.account_currency, a.tax_amount,
                                    a.total, a.tax_amount_after_discount_amount, a.base_tax_amount, a.base_total, a.base_tax_amount_after_discount_amount, a.item_wise_tax_detail, a.dont_recompute_tax
                                   from `tabSales Taxes and Charges` a join `tabSales Order` b
                                   on a.parent = b.name
                                   where b.name = '{name}'
                               """.format(name=doc.name), as_dict=1)

    for x in so_taxes:
        taxes = new_doc.append("taxes", {})
        taxes.charge_type = x.charge_type
        taxes.row_id = x.row_id
        taxes.account_head = x.account_head
        taxes.description = x.description
        taxes.included_in_print_rate = x.included_in_print_rate
        taxes.included_in_paid_amount = x.included_in_paid_amount
        taxes.rate = x.rate
        taxes.account_currency = x.account_currency
        taxes.tax_amount = x.tax_amount
        taxes.total = x.total
        taxes.tax_amount_after_discount_amount = x.tax_amount_after_discount_amount
        taxes.base_tax_amount = x.base_tax_amount
        taxes.base_total = x.base_total
        taxes.base_tax_amount_after_discount_amount = x.base_tax_amount_after_discount_amount
        taxes.item_wise_tax_detail = x.item_wise_tax_detail
        taxes.dont_recompute_tax = x.dont_recompute_tax

    new_doc.insert(ignore_permissions=True)
    if lang == "ar":
        frappe.msgprint("  تم إنشاء إذن تسليم العميل بحالة مسودة رقم " + new_doc.name)
    else:
        frappe.msgprint(" Delivery Note " + new_doc.name + " Created ")

    ## Auto Create Draft Installation Note On Submit
    if doc.auto_create_installation_note_on_submit:
        new_doc3 = frappe.get_doc({
                "doctype": "Installation Note",
                "sales_order": doc.name,
                "delivery_note": new_doc.name,
                "customer": doc.customer,
                "customer_group": doc.customer_group,
                "territory": doc.territory,
                "customer_address": doc.customer_address,
                "contact_person": doc.contact_person,
                "inst_date": doc.transaction_date,
            })
        so_items = frappe.db.sql(""" select a.name, a.idx, a.item_code, a.item_name, a.description, a.qty, a.rate, a.amount
                                           from `tabSales Order Item` a join `tabSales Order` b
                                           on a.parent = b.name
                                           where b.name = '{name}'
                                       """.format(name=doc.name), as_dict=1)

        for c in so_items:
            items = new_doc3.append("items", {})
            items.idx = c.idx
            items.item_code = c.item_code
            items.item_name = c.item_name
            items.description = c.description
            items.qty = c.qty
            items.rate = c.rate
            items.amount = c.amount
            items.prevdoc_detail_docname = c.name
            items.prevdoc_docname = doc.name
            items.prevdoc_doctype = "Sales Order"

        new_doc3.insert(ignore_permissions=True)
        if lang == "ar":
            frappe.msgprint("  تم إنشاء إذن تركيب رقم " + new_doc.name)
        else:
            frappe.msgprint(" Installation Note " + new_doc.name + " Created ")
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
