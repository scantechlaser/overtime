# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate
from frappe import msgprint, _
from calendar import monthrange
import re
from datetime import timedelta

def execute(filters=None):
	if not filters: filters = {}

	conditions, filters = get_conditions(filters)
	columns = get_columns(filters)
	att_map = get_attendance_list(conditions, filters)
	emp_map = get_employee_details()
	

	data = []
	# leave_types = frappe.db.sql("""select name from `tabLeave Type`""", as_list=True)
	# leave_list = [d[0] for d in leave_types]
	# columns.extend(leave_list)

	for emp in sorted(att_map):

		emp_det = emp_map.get(emp)
		if not emp_det:
			continue
		row = []

		emp_total_ot_hours = get_total_ot_hours(conditions, filters)
		emp_total_ot_rupees = get_total_ot_rupees(conditions, filters)

		row = [emp, emp_det.employee_name]

		total_ot = total_ot = total_ot = 0.0

		# row += [total_ot]


		if not filters.get("employee"):
			filters.update({"employee": emp})
			conditions += " and employee = %(employee)s"
		elif not filters.get("employee") == emp:
			filters.update({"employee": emp})

		# row['over_time'] = 0

		ot_in_seconds = 0
		myTime = ''
		total_ot_rupees = 0.0

		for d in range(0,filters["total_days_in_month"]):

			#to Get date 
			date = ''

			month = filters.month
			year = cint(filters.year)

			currentDay = int(d+1)

			if int(d) < 9:
				currentDay = '0'+str(int(d+1))

			if (int(month)) < 10:
				month = '0'+str(int(month))

			date  = str(year)+'-'+str(month)+'-'+str(currentDay)

			my_sql = "SELECT total_ot, total_rs FROM `tabovertime` where docstatus = 1 AND employee = '"+str(emp)+"' AND date = '"+str(date)+"'  order by employee, date"
			
			getTimeDetails = frappe.db.sql(my_sql,as_dict=True)
			if getTimeDetails:
				
				total_ot_rupees = total_ot_rupees + float(getTimeDetails[0]['total_rs'])

				ot_detalils_len = 0

				row.append(getTimeDetails[0]['total_ot'])
				total_ot_details = re.findall('\d+', str(getTimeDetails[0]['total_ot']))
				ot_detalils_len = len(total_ot_details)
				for j in range(ot_detalils_len):
					if int(j) == 0:

						ot_in_seconds = ot_in_seconds + (int(total_ot_details[j]) * 60 * 60)
						
					elif int(j) == 1:

						ot_in_seconds = ot_in_seconds + (int(total_ot_details[j]) * 1 * 60)

			else:
				row.append(0.0)

		

		# myTime = str(timedelta(minutes=ot_in_seconds))[:-3]

		hour = ot_in_seconds // 3600
		ot_in_seconds %= 3600
		minutes = ot_in_seconds // 60

		myTime = str(hour)+" hour(s) and " + str(minutes) + " minute(s)."

		total_ot_rupees = round(float(total_ot_rupees), 2)

		row.append(myTime)
		row.append(total_ot_rupees)

		data.append(row)
	return columns, data

def get_columns(filters):
	columns = [
		_("Employee") + ":Link/Employee:120", _("Employee Name") + "::140", 
	]

	for day in range(filters["total_days_in_month"]):
		columns.append(cstr(day+1) +"::20")

	columns += [_("Total OT Hours") + "::140", _("Total Over Time In Rs.") + "::140"]

	return columns

def get_attendance_list(conditions, filters):
	attendance_list = frappe.db.sql("""select employee, day(date) as day_of_months from `tabovertime` where docstatus = 1 %s order by employee, date""" %
		conditions, filters, as_dict=1)

	att_map = {}
	for d in attendance_list:
		att_map.setdefault(d.employee, frappe._dict()).setdefault(d.day_of_month, "")
		# att_map[d.employee][d.day_of_month] = d.status

	return att_map

def get_total_ot_hours(conditions, filters):
	return 0 

def get_total_ot_rupees(conditions, filters):
	return 0


def get_conditions(filters):
	if not (filters.get("month") and filters.get("year")):
		msgprint(_("Please select month and year"), raise_exception=1)

	filters["month"] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
		"Dec"].index(filters.month) + 1

	filters["total_days_in_month"] = monthrange(cint(filters.year), filters.month)[1]

	conditions = " and month(date) = %(month)s and year(date) = %(year)s"

	# if filters.get("company"): conditions += " and company = %(company)s"
	if filters.get("employee"): conditions += " and employee = %(employee)s"

	return conditions, filters

def get_employee_details():
	emp_map = frappe._dict()
	for d in frappe.db.sql("""select name, employee_name, designation, department, branch, company,
		holiday_list from tabEmployee""", as_dict=1):
		emp_map.setdefault(d.name, d)

	return emp_map


@frappe.whitelist()
def get_attendance_years():
	year_list = frappe.db.sql_list("""select distinct YEAR(attendance_date) from tabAttendance ORDER BY YEAR(attendance_date) DESC""")
	if not year_list:
		year_list = [getdate().year]

	return "\n".join(str(year) for year in year_list)
