// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Ticket', {
    get_serial_details: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_serial_details",
                callback: function(r) {
                refresh_field("items");
                cur_frm.save('Save');
            }
        });
	}
});

frappe.ui.form.on('Ticket', {
    create_payment_entry: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "create_payment_entry",
                callback: function(r) {
                refresh_field("payment_entry");
            }
        });
	}
});

frappe.ui.form.on("Ticket Items", "create_stock_entry", function(frm,cdt,cdn) {
    var d = locals[cdt][cdn];
    frappe.route_options = {
        "stock_entry_type": "Material Issue",
        "ticket": frm.doc.name,
        "ticket_item": d.name

    };
    frappe.new_doc("Stock Entry");
});





