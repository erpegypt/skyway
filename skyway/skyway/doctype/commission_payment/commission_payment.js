// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Commission Payment', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Commission Payment',  'validate',  function(frm, cdt, cdn) {
    if(frm.doc.__islocal ? 0 : 1){
         var dw = locals[cdt][cdn];
        var total = 0;
        frm.doc.commission_details.forEach(function(dw) { total += dw.commissions; });
        frm.set_value("total_payable", total);
        refresh_field("total_payable");
    }
});