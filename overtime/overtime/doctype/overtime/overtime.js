// Copyright (c) 2018, scantech laser and contributors
// For license information, please see license.txt
cur_frm.add_fetch('employee','employee_name','employee_name');

frappe.ui.form.on('overtime', {
	refresh: function(frm) {
		// frm.trigger("validate_employee");
	},
	onload: function(frm) {

		frm.set_query("employee", erpnext.queries.employee);

		if (!frm.doc.date) {
			frm.set_value("date", frappe.datetime.get_today());
			dayDifference = frappe.datetime.get_day_diff(frappe.datetime.get_today(), frm.doc.date );
			
			frm.set_value('between_days', dayDifference);
		}
		
	},
	employee: function(frm){
		frm.trigger("validate_employee");
	},

	in_time: function(frm) {

		frm.trigger("calculate_total_ot_hours");
		frm.trigger("validate_time");

	},

	out_time: function(frm) {
		
		frm.trigger("calculate_total_ot_hours");
		frm.trigger("validate_time");

		
	},
	calculate_total_ot_hours: function(frm) {

		frappe.call({
				method: "overtime.overtime.doctype.overtime.overtime.get_setting",
				args: {

					
				},
				callback: function(r) {

					r.message;

					var standardStartTime = moment(r.message.start_time, 'hh:mm:ss a');
					var standardEndTimeOfCompany = moment(r.message.end_time, 'hh:mm:ss a');
					var startTime = moment(frm.doc.in_time, 'hh:mm:ss a');
					var endTime = moment(frm.doc.out_time, 'hh:mm:ss a');

					var otIsApplicableAfter = moment(r.message.overtime_is_applicable_after, 'hh:mm:ss a');

					var diff = endTime.diff(startTime, 'minute');
					var ans = '';
					var total_ot_ruppes = 0;
					var value = 30;
					var max_ot_hours_in_minute = 0;

					var maxOtHours = r.message.max_ot_hours;

					var roundMinutesAfter = r.message.round_hours_after;

					if(maxOtHours){

						var standard_ot_hours = maxOtHours.split(':');

						max_ot_hours_in_minute = parseInt(standard_ot_hours[0] * 60) + parseInt(standard_ot_hours[1]);
					}



					var calcualteOtInHours = r.message.if_overtime_based_on_hours;

					if (calcualteOtInHours ==1){
						calcualteOtInHours = true;
					}
					var standardWorkingHours = r.message.working_hours;

					var standardWorkingTime = standardWorkingHours.split(':');


					var timeInminutes = parseInt(standardWorkingTime[0] * 60) + parseInt(standardWorkingTime[1]);


					var standardDiff = standardEndTimeOfCompany.diff(startTime, 'minute');

					if(startTime > standardStartTime){

						var standardDiff = endTime.diff(startTime, 'minute');
					}

					if(standardStartTime >= startTime & endTime > otIsApplicableAfter){

						var finalStartTime = moment(standardEndTimeOfCompany, 'hh:mm:ss a');
						var finalEndTime = moment(frm.doc.out_time, 'hh:mm:ss a');
						var finalDiff = finalEndTime.diff(finalStartTime, 'minute');

						var actualDiff = finalDiff;

						
						total_ot_ruppes = actualDiff * value;

						if(max_ot_hours_in_minute > 0 && actualDiff > max_ot_hours_in_minute){
							actualDiff = max_ot_hours_in_minute;
						}
						var num = actualDiff;
						var hours = (num / 60);
						var rhours = Math.floor(hours);
						var minutes = (hours - rhours) * 60;
						var rminutes = Math.round(minutes);

						if(calcualteOtInHours ==true){

							if(roundMinutesAfter < parseInt(rminutes)){

								rhours = parseInt(rhours) + 1

								rminutes = 0;

							}else{
								return false
							}
						}
						
						ans  = rhours + ":" + rminutes;
						
						frm.set_value('total_ot', ans);
						
						return frappe.call({
							method: "overtime.overtime.doctype.overtime.overtime.validate_amount",
							args: {

								totalMinutes: actualDiff,
								employee :frm.doc.employee
								
							},
							callback: function(r) {
								if (r.message) {
									
										// frm.set_value('total_rs', r.message);
										amountPerhour = r.message;

										var time = ans.split(":");
									    var hours = time[0];
									    var mins = time[1];
									    var secs = time[2];

									    if (secs != undefined && secs > 29) {
									        mins++;
									    }
									    var amount = (+hours + +mins/60) * amountPerhour;
									
										frm.set_value('total_rs', amount);
									
								}
								else {

									frappe.throw(__("Cannot Calculate OT Amount"))
								}
							}
						});


					}

					if(endTime > otIsApplicableAfter && standardDiff > timeInminutes)
					{	

						standardDiff = standardDiff - timeInminutes;


						if(max_ot_hours_in_minute > 0 && standardDiff > max_ot_hours_in_minute){
							standardDiff = max_ot_hours_in_minute;
						}


						

						var num = standardDiff;
						var hours = (num / 60);
						var rhours = Math.floor(hours);
						var minutes = (hours - rhours) * 60;
						var rminutes = Math.round(minutes);


						if(calcualteOtInHours ==true){

							if(roundMinutesAfter < parseInt(rminutes)){

								rhours = parseInt(rhours) + 1

								rminutes = 0;

							}else{
								return false
							}
						}

						
						ans  = rhours + ":" + rminutes;

						var a = ans.split(':'); // split it at the colons

						var finalStartTime = moment(ans, 'hh:mm:ss a');

						var minutes = (+a[0]) * 60 + (+a[1]);

						if(minutes > 20){


							frm.set_value('total_ot', ans);
						

							return frappe.call({
								method: "overtime.overtime.doctype.overtime.overtime.validate_amount",
								args: {

									totalMinutes: minutes,
									employee :frm.doc.employee
									
								},
								callback: function(r) {
									if (r.message) {

											amountPerhour = r.message;

											var time = ans.split(":");
										    var hours = time[0];
										    var mins = time[1];
										    var secs = time[2];

										    if (secs != undefined && secs > 29) {
										        mins++;
										    }
										    var amount = (+hours + +mins/60) * amountPerhour;
										
											frm.set_value('total_rs', amount);
										
									}
									else {

										frappe.throw(__("Cannot Calculate OT Amount"))
									}
								}
							});

						}else{
							frm.set_value('total_ot', '');
							frm.set_value('total_rs', '');
						}

					}

					else{

						frm.set_value('total_ot', ans);
						frm.set_value('total_rs', total_ot_ruppes);

					}
			}
		});

		
	},
	validate_employee: function(frm) {
		return frappe.call({
				method: "overtime.overtime.doctype.overtime.overtime.validate_employee",
				args: {

					employee :frm.doc.employee
					
				},
				callback: function(r) {
					if (!r.exc && r.message) {
						if(r.message == "False"){
							frappe.throw(__("Sorry You have not permission to apply Over Time"))
						}
						
					}
				}
			});
	},
	validate_time: function(frm){

		var startTime = moment(frm.doc.in_time, 'hh:mm:ss a');
		var endTime = moment(frm.doc.out_time, 'hh:mm:ss a');
		if(startTime > endTime){
			frappe.throw(__("In Time Cannot be greater then out Time!"))
		}

	},
	save:function(frm){
		frappe.throw(__("OT Hours applicable only after completion of working hours!"))
	},
	date:function(frm){

		dayDifference = frappe.datetime.get_day_diff(frappe.datetime.get_today(), frm.doc.date );
		// console.log(dayDifference);
		frm.set_value('between_days', dayDifference);

		// alert(2323);

		return frappe.call({
				method: "overtime.overtime.doctype.overtime.overtime.validate_date",
				args: {

					date :frm.doc.date,
					between_days : frm.doc.between_days
					
				},
				callback: function(r) {
					if (!r.exc && r.message) {
						if(r.message == "False"){
							frappe.throw(__("You cannot enter Overtime Before Three days or after Todays date"))
						}
						
					}
				}
			});
	}

});
