// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Commission Role', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Commission Role',{
    setup: function(frm) {
        cur_frm.fields_dict['commission_item'].grid.get_field("item_code").get_query = function(doc, cdt, cdn){
            return {
                filters:[
                    ["Item","is_sales_item", "=", 1]
                ]
            };
        };
    }
});

frappe.ui.form.on('Commission Role', {
    get_items: function(frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_items",
                callback: function(r) {
                refresh_field("commission_item");
                cur_frm.save('Save');
            }
        });
	}
})