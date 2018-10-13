# -*- coding: utf-8 -*-
# Copyright (c) 2018, scantech laser and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate
from frappe import msgprint, _
from calendar import monthrange
import re
from datetime import timedelta
from calendar import monthrange
from frappe import _
from frappe.model.document import Document
from frappe.utils import time_diff_in_hours
from datetime import datetime

class OvertimeSlip(Document):
	pass


@frappe.whitelist()
def validate_employee(employee='', date = ''):

	ot_in_seconds = 0
	total_ot_rupees = 0.0
	
	my_sql = "SELECT * FROM `tabEmployee` where is_ot_applicable = '1' and employee = '"+employee+"'"
	validateEmployee = frappe.db.sql(my_sql)
	if validateEmployee:
		posting_date = str(date)
		posting_date = posting_date.split("-")


		getTotalMonths = monthrange(int(posting_date[0]), int(posting_date[1]))[1]

		# frappe.throw(_(getTotalMonths))
		fromDate = str(posting_date[0])+'-'+str(posting_date[1])+'-'+str(0)+''+str(1)
		toDate = str(posting_date[0])+'-'+str(posting_date[1])+'-'+str(getTotalMonths)

		my_sql = "SELECT * FROM `tabovertime` WHERE employee = '"+str(employee)+"' and date >= DATE('"+str(fromDate)+"') AND date <= DATE('"+str(toDate)+"') and docstatus = '1' AND total_ot IS NOT NULL"
		getOvertimeData = frappe.db.sql(my_sql, as_dict=True)
		if getOvertimeData:

			for i in getOvertimeData:

				total_ot_rupees = total_ot_rupees + float(i['total_rs'])

				total_ot_details = re.findall('\d+', str(i['total_ot']))
				ot_detalils_len = len(total_ot_details)
				for j in range(ot_detalils_len):
					if int(j) == 0:

						ot_in_seconds = ot_in_seconds + (int(total_ot_details[j]) * 60 * 60)
						
					elif int(j) == 1:

						ot_in_seconds = ot_in_seconds + (int(total_ot_details[j]) * 1 * 60)

		hour = ot_in_seconds // 3600
		ot_in_seconds %= 3600
		minutes = ot_in_seconds // 60

		response = str(hour)+" hour(s) and " + str(minutes) + " minute(s)."

		return {"ot_hours":response, "total_ot_rupees":round(total_ot_rupees)}

		# return myTime, total_ot_rupees


		# my_sql = "SELECT * FROM `tabovertime` WHERE employee = '"+employee+"' and "
		# return "True"
	else:
		return "False"