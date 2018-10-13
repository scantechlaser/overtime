// Copyright (c) 2018, scantech laser and contributors
// For license information, please see license.txt

cur_frm.add_fetch('employee','employee_name','employee_name');


frappe.ui.form.on('Overtime Slip', {
	refresh: function(frm) {

	},
	onload: function(frm) {

		frm.set_query("employee", erpnext.queries.employee);
	},
	employee: function(frm){
		// alert(1);
		frm.trigger("validate_employee");
	},
	validate_employee: function(frm) {
		return frappe.call({
				method: "overtime.overtime.doctype.overtime_slip.overtime_slip.validate_employee",
				args: {

					employee :frm.doc.employee,
					date : frm.doc.posting_date
					
				},
				callback: function(r) {
					if (!r.exc && r.message) {

						cur_frm.set_value("total_ot_hours", r.message.ot_hours);
						cur_frm.set_value("total_ot_rupees", r.message.total_ot_rupees);

					
						// if(r.message == "False"){
						// 	frappe.throw(__("Sorry You have not permission to apply Over Time"))
						// }
						
					}
				}
			});
	}
});
