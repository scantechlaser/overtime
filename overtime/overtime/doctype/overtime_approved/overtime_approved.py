# -*- coding: utf-8 -*-
# Copyright (c) 2018, scantech laser and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe import utils


class OvertimeApproved(Document):

	def validate(self):

		validApprover = validate_approver(self.approver_id)
		if(str(validApprover) == 'False'):

			frappe.throw(__("Sorry You Dont have permission to Approved Over Time"))

	# 	my_sql = "SELECT E.name as name FROM `tabEmployee` E RIGHT JOIN `tabEmployee OT Approver` A ON A.parent = E.name WHERE E.is_ot_applicable = '1' and E.name != '"+str(getEmployee[0].name)+"' and A.ot_approver = '"+str(userId)+"'"
	

	def on_submit(self):

		temp = 1

		checkInc = 0


		validApprover = validate_approver(self.approver_id)
		if(str(validApprover) == 'False'):
			
			frappe.throw(__("Sorry You Dont have permission to Approved Over Time"))

		my_sql = "SELECT * FROM `tabEmployee Over Time` WHERE parent = '"+str(self.name)+"'"
		getEmployeeOT = frappe.db.sql(my_sql, as_dict = True)
		if getEmployeeOT:
			for i in getEmployeeOT:
				my_sql = "SELECT * FROM `tabovertime` WHERE name = '"+str(i.ot_id)+"' and docstatus= 1 "
				getOvertime = frappe.db.sql(my_sql, as_dict=True)
				if getOvertime:
					checkInc += 1
					temp = 1
					frappe.throw(_('Row '+str(checkInc)+' Is already submitted to kindly che status to Rejected'))

		my_sql = "SELECT * FROM `tabEmployee Over Time` WHERE parent = '"+str(self.name)+"' and status = 'Approved'"
		getEmployeeOT = frappe.db.sql(my_sql, as_dict = True)
		if getEmployeeOT:
			for m in getEmployeeOT:

				doc = frappe.get_doc("overtime", m.ot_id)
				doc.submit()



@frappe.whitelist()
def get_employee_ot_details(userId = '', fromDate = '', toDate = ''):

	response = []

	my_sql = "SELECT * FROM `tabEmployee` WHERE user_id = '"+str(userId)+"'"
	getEmployee = frappe.db.sql(my_sql, as_dict=True)
	if getEmployee:

		my_sql = "SELECT E.name as name FROM `tabEmployee` E RIGHT JOIN `tabEmployee OT Approver` A ON A.parent = E.name WHERE E.is_ot_applicable = '1' and E.name != '"+str(getEmployee[0].name)+"' and A.ot_approver = '"+str(userId)+"'"

		getOtValidEmployee = frappe.db.sql(my_sql, as_dict=True)
		if getOtValidEmployee:

			for i in getOtValidEmployee:


				my_sql = "SELECT * FROM `tabovertime` WHERE employee = '"+str(i.name)+"' and date >= DATE('"+str(fromDate)+"') AND date <= DATE('"+str(toDate)+"') and docstatus = '0' AND total_ot IS NOT NULL ORDER BY employee"
				getOtDetails = frappe.db.sql(my_sql, as_dict=True)
				if getOtDetails:
					for j in getOtDetails:

						my_sql = "SELECT * FROM `tabEmployee Over Time` WHERE ot_id = '"+str(j.name)+"'"
						getEmployeeOverTime = frappe.db.sql(my_sql, as_dict = True)
						if not getEmployeeOverTime:

							# frappe.throw(_(my_sql))

							response.append({"name":j.name, 
								"employee": j.employee, 
								"employee_name": j.employee_name,
								"date":j.date,
								"total_ot":j.total_ot,
								"total_rs":j.total_rs,
								"in_time":j.in_time,
								"out_time":j.out_time
								})
							

		return response



@frappe.whitelist()
def validate_approver(approver=''):

	my_sql = "SELECT * FROM `tabHas Role` WHERE parent = '"+str(approver)+"'"
	getRole = frappe.db.sql(my_sql, as_dict=True)
	if getRole:

		for i in getRole:

			if(str(i.role) == 'HR User' or str(i.role) == 'HR Manager'):
				return "True"

	
	my_sql = "SELECT * FROM `tabEmployee OT Approver` WHERE ot_approver = '"+str(approver)+"'"
	validateEmployee = frappe.db.sql(my_sql)
	if validateEmployee:
		return "True"
	else:
		return "False"

