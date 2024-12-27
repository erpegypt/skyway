# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
# import frappe
from frappe.model.document import Document

class Ticket(Document):
    @frappe.whitelist()
    def validate(self):
        self.calculate_total()

    @frappe.whitelist()
    def on_submit(self):
        self.check_mandatory_fields()

    @frappe.whitelist()
    def calculate_total(self):
        totals = 0
        for x in self.items:
            totals += x.cost
        self.total_cost = totals

    @frappe.whitelist()
    def check_mandatory_fields(self):
        for x in self.items:
            if not x.warranty:
                frappe.throw("Row #" + str(x.idx) + ": Please Select The Warranty Status")
            if not x.issue_description:
                frappe.throw("Row #" + str(x.idx) + ": Please Mention The Issue Description")

    @frappe.whitelist()
    def get_serial_details(self):
        # التحقق من إدخال رقم تسلسلي
        if not self.serial_no:
            frappe.throw("Please Enter A Serial Number")

        # تعيين الحقل المستخدم في الاستعلام بناءً على قيمة serial_now
        search_field = "serial_no" if self.serial_now else "serial"

        # التحقق من وجود الرقم التسلسلي المدخل بشكل مكرر في جدول Ticket Items
        check = frappe.db.sql(""" select serial, idx
                                  from `tabTicket Items` 
                                  where parent = '{parent}' and serial = '{serial}' 
                              """.format(parent=self.name, serial=self.serial_no), as_dict=1)
        for z in check:
            if z.serial:
                frappe.throw("Duplicated Entry: Serial " + z.serial + " Has Been Added In Row #" + str(z.idx))

        # جلب تفاصيل الرقم التسلسلي من Delivery Note و Delivery Note Item
        details = frappe.db.sql(f"""
            SELECT 
                `tabDelivery Note`.name AS delivery_note,
                `tabDelivery Note`.posting_date AS dn_date,
                `tabDelivery Note`.customer AS customer,
                `tabDelivery Note Item`.item_code AS item_code,
                `tabDelivery Note Item`.name AS dn_item_name,
                `tabDelivery Note Item`.item_name AS item_name
            FROM 
                `tabDelivery Note Item`
            JOIN 
                `tabDelivery Note` 
            ON 
                `tabDelivery Note Item`.parent = `tabDelivery Note`.name
            WHERE 
                `tabDelivery Note`.docstatus = 1 
                AND `tabDelivery Note Item`.{search_field} LIKE %s
        """, (f"%{self.serial_no}%",), as_dict=1)

        # إضافة التفاصيل إلى جدول العناصر items
        for x in details:
            y = self.append("items", {})
            y.customer = x.customer
            y.delivery_note = x.delivery_note
            y.dn_item_name = x.dn_item_name
            y.dn_date = x.dn_date
            y.item_code = x.item_code
            y.item_name = x.item_name
            y.serial = self.serial_no
            y.cost = 0

            #self.save()

    @frappe.whitelist()
    def create_payment_entry(self):
        if self.total_cost == 0:
            frappe.throw(" Please Add The Cost In The Items Table")
        pe_doc = frappe.get_doc({
            "doctype": "Payment Entry",
            "posting_date": self.posting_date,
            "payment_method": self.payment_method,
            "payment_type": "Receive",
            "mode_of_payment": "بدل صيانة",
            "reference_doctype": "Ticket",
            "reference_name": self.name,
            "paid_to": "خزينة الادارة - Sky",
            "party_type": "Customer",
            "party": self.customer,
            "paid_amount": self.total_cost,
            "received_amount": self.total_cost,
            "reference_date": self.posting_date,
            "source_exchange_rate": 1,
            "target_exchange_rate": 1,
        })
        pe_doc.insert(ignore_permissions=True)
        self.payment_entry = pe_doc.name
        self.payment_entry_status = pe_doc.status
        self.save()
        self.reload()

    pass