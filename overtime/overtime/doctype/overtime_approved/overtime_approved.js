// Copyright (c) 2018, scantech laser and contributors
// For license information, please see license.txt


frappe.ui.form.on('Overtime Approved', {


	onload: function(frm) {

		frm.trigger("validate_approver");
		
	},
	
	refresh: function(frm) {

		// alert()

		// print 
		// print user_doc.last_name
		
		
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Overtime'), function() {

				var userId = frappe.session.user;

				return frappe.call({
					method: "overtime.overtime.doctype.overtime_approved.overtime_approved.get_employee_ot_details",
					args: {

						userId :userId,
						fromDate : frm.doc.from_date,
						toDate : frm.doc.to_date
	
					},
					callback: function(r) {
						if (!r.exc && r.message) {

							console.log(frm.doc.overt_time);
							frm.doc.overt_time = [];


							for (var i=0; i<(r.message).length; i++){

								// alert(frm.doc.overtime);
								

								

								var child = cur_frm.add_child("overt_time");
								frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee_name);
								frappe.model.set_value(child.doctype, child.name, "ot_id", r.message[i].name);
								frappe.model.set_value(child.doctype, child.name, "in_time", r.message[i].in_time);
								frappe.model.set_value(child.doctype, child.name, "out_time", r.message[i].out_time);
								frappe.model.set_value(child.doctype, child.name, "date", r.message[i].date);
								frappe.model.set_value(child.doctype, child.name, "total_ot", r.message[i].total_ot);
								frappe.model.set_value(child.doctype, child.name, "total_rs", r.message[i].total_rs);
						
								cur_frm.refresh_field("overt_time");
								
							}
			
						}
					}
				});

				

			}, __("Get Employee from"));
			
		}

		if (frm.doc.docstatus===0) {

			var Current_User = frappe.session.user;
			cur_frm.set_value("approver_id", Current_User);
			
			frappe.call({
				method:"frappe.client.get",
				args: {
					doctype:"User",
					filters: {'email': Current_User
					},
				},
				callback: function(r) {
					cur_frm.set_value("approver", r.message["full_name"]);
				}
			});
		}



	},

	from_date: function(frm) {

        var myDate = new Date(frm.doc.from_date);
        var today = new Date();
        if ( myDate > today ) { 
            frappe.throw(__("From Date should be less then or equal to todays date"))
        }


		var userId = frappe.session.user;

		return frappe.call({
			method: "overtime.overtime.doctype.overtime_approved.overtime_approved.get_employee_ot_details",
			args: {

				userId :userId,
				fromDate : frm.doc.from_date,
				toDate : frm.doc.to_date

			},
			callback: function(r) {
				if (!r.exc && r.message) {
					// alert(cur_frm);
					console.log(frm.doc.overt_time);
					frm.doc.overt_time = [];

					for (var i=0; i<(r.message).length; i++){


								var child = cur_frm.add_child("overt_time");
								frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee_name);
								frappe.model.set_value(child.doctype, child.name, "ot_id", r.message[i].name);
								frappe.model.set_value(child.doctype, child.name, "in_time", r.message[i].in_time);
								frappe.model.set_value(child.doctype, child.name, "out_time", r.message[i].out_time);
								frappe.model.set_value(child.doctype, child.name, "date", r.message[i].date);
								frappe.model.set_value(child.doctype, child.name, "total_ot", r.message[i].total_ot);
								frappe.model.set_value(child.doctype, child.name, "total_rs", r.message[i].total_rs);
								
								cur_frm.refresh_field("overt_time");
								
							}
	
				}
			}
		});

	},

	to_date: function(frm) {

		var myDate = new Date(frm.doc.to_date);
        var today = new Date();
        if ( myDate > today ) { 
            frappe.throw(__("From Date should be less then or equal to todays date"))
        }

		var userId = frappe.session.user;

		return frappe.call({
			method: "overtime.overtime.doctype.overtime_approved.overtime_approved.get_employee_ot_details",
			args: {

				userId :userId,
				fromDate : frm.doc.from_date,
				toDate : frm.doc.to_date

			},
			callback: function(r) {
				if (!r.exc && r.message) {

					// alert(cur_frm);
					console.log(frm.doc.overt_time);
					frm.doc.overt_time = [];

					for (var i=0; i<(r.message).length; i++){


								var child = cur_frm.add_child("overt_time");
								frappe.model.set_value(child.doctype, child.name, "employee", r.message[i].employee_name);
								frappe.model.set_value(child.doctype, child.name, "ot_id", r.message[i].name);
								frappe.model.set_value(child.doctype, child.name, "in_time", r.message[i].in_time);
								frappe.model.set_value(child.doctype, child.name, "out_time", r.message[i].out_time);
								frappe.model.set_value(child.doctype, child.name, "date", r.message[i].date);
								frappe.model.set_value(child.doctype, child.name, "total_ot", r.message[i].total_ot);
								frappe.model.set_value(child.doctype, child.name, "total_rs", r.message[i].total_rs);
								
								cur_frm.refresh_field("overt_time");
								
							}
	
				}
			}
		});

	},
	validate_approver: function(frm) {
		return frappe.call({
				method: "overtime.overtime.doctype.overtime_approved.overtime_approved.validate_approver",
				args: {

					approver :frappe.session.user
					
				},
				callback: function(r) {
					if (!r.exc && r.message) {
						if(r.message == "False"){
							frappe.throw(__("Sorry You Dont have permission to Approved Over Time"))
						}
						
					}
				}
			});
	}
})

