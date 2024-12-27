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
    commission_percen1 = 0
    total_com = 0
    target_amount = 0
    for x in doc.items:
        if x.discount_amount <0:
            x.discount_percentage = 0
            x.discount_percentage = (x.discount_amount / x.price_list_rate ) * 100
    for d in doc.items:
        role_item_parent = frappe.db.sql(""" select `tabCommission Item`.item as item_code ,
														`tabCommission Item`.parent as parent
														from `tabCommission Item` 
														where 
														`tabCommission Item`.item = '{role_item}'
														""".format( role_item = d.item_code),  as_dict=True)


        for par in role_item_parent:
            commission_perc = frappe.db.sql(""" select `tabCommission Details`.discount_from as discount_from ,
                                                        `tabCommission Details`.discount_to as discount_to ,
                                                        ifnull(`tabCommission Details`.commission_percent,0) as commission_percent
                                                        from `tabCommission Details` 
                                                        where 
                                                        `tabCommission Details`.parent = '{parent}'
                                                        and  '{discount_percentage}' >= `tabCommission Details`.discount_from 
                                                        and  '{discount_percentage}' <= `tabCommission Details`.discount_to
                                                        """.format( parent = par.parent, discount_percentage = d.discount_percentage ),  as_dict=True)

            for commission in commission_perc:
                
                commission_percen1 = commission.commission_percent
        d.item_commission_rate = commission_percen1
        d.total_commission = (commission_percen1 * d.amount ) / 100
        
        total_com += d.total_commission
        doc.commission_amount = total_com
        target_amount = frappe.db.get_value('Sales Partner', {'name': doc.sales_partner}, 'target_amount')
        doc.target_amount = target_amount
    
@frappe.whitelist()
def on_submit(doc, method=None):
    pass
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
