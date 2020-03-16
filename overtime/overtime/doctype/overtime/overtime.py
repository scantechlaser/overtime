# -*- coding: utf-8 -*-
# Copyright (c) 2018, scantech laser and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cstr, flt, cint, getdate, now_datetime, formatdate, strip,time_diff_in_hours
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from frappe.utils import getdate
import calendar
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
import datetime
from datetime import *

t_a = now_datetime()
t_b = now_datetime()


class overtime(Document):
	def validate(self):

		# frappe.throw(_(self.total_ot))
		if(str(self.total_ot) =="" or self.total_ot == None):
			frappe.throw(_("Overtime is consider after completion of 8:30 working hours, Kindly Enter valid time"))

		validateEmployee = validate_employee(self.employee)
		if(validateEmployee =='False'):
			frappe.throw(_("Overtime is not Applicable for "+str(self.employee_name)+"  Kindly contact to HR department for further details"))

		# if (self.between_days):
		# 	if(int(self.between_days) >2 or int(self.between_days) < 0):
		# 		frappe.throw(_("You cannot enter Overtime before Two days and Advanced"))
		if float(self.total_rs) <= 0.0:
			frappe.throw(_("Salary Structure is not created! Kindly call to HR Department"))

		validate_existing_entry = validate_already_existed_entry(self.employee, self.date, self.name)
		# frappe.throw(_(validate_existing_entry))
		if validate_existing_entry:
			frappe.throw(_(str(self.date)+"   dated entry is already Existed so you cannot submit this entry"))



	def on_submit(self):
		if(self.total_ot ==''):
			frappe.throw(_("Overtime is consider after completion of 8:30 working hours"))

		validateEmployee = validate_employee(self.employee)
		if(validateEmployee =='False'):
			frappe.throw(_("Overtime is not Applicable for "+str(self.employee_name)+"  Kindly contact to HR department for further details"))

		



@frappe.whitelist()
def validate_amount(totalMinutes=0, employee=''):

	# frappe.throw(_())
	if(int(totalMinutes) < 0):
		frappe.throw(_("In Time should be greater then out time"))
	else:
		if(int(totalMinutes) < 20):
			frappe.throw(_("Not Applicable"))
		else:
			finalAmount = 0.0
			my_sql = "SELECT * FROM `tabSalary Structure Assignment` where employee = '"+employee+"' and base != 0 order by creation desc"
			# frappe.throw(_(my_sql))
			validate_amount = frappe.db.sql(my_sql,as_dict=True)
			if validate_amount:

				data = get_setting()

				useFormula = str(data.formula)

				data = {"gross":int(validate_amount[0]['base']), "hours":1}

				amount = frappe.safe_eval(useFormula, None, data)
				# baseAmount = int(validate_amount[0]['base'])
				# daysInHours = float(26.0) * float(8.5) * float(60.0)
				# finalAmount = float(baseAmount) * float(totalMinutes)/daysInHours
				return round(amount)
			else:
				frappe.throw(_("Salary Structure is not created! Kindly call to HR Department"))


@frappe.whitelist()
def validate_employee(employee=''):
	
	my_sql = "SELECT * FROM `tabEmployee` where is_ot_applicable = '1' and employee = '"+employee+"'"
	validateEmployee = frappe.db.sql(my_sql)
	if validateEmployee:
		return "True"
	else:
		return "False"

@frappe.whitelist()
def validate_date(date='', between_days = 0):
	if(int(between_days) > 2 or int(between_days) < 0):
		return "False"

@frappe.whitelist()
def validate_already_existed_entry(employee, date, name=''):

	
	my_sql = "SELECT * FROM `tabovertime` where name = '"+str(name)+"'"
	
	getExisting = frappe.db.sql(my_sql, as_dict=True)
	if getExisting:

		if(str(date) == str(getExisting[0].date)):
			return False
		else:
			frappe.throw(_("You Cannot change the date, Please select "+str(getExisting[0].date)))
		
	else:
		return False


@frappe.whitelist(allow_guest=True)
def day(date):
	a=calendar.weekday(year,month,day)
	days=["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
	frappe.throw(_(days[a]))

@frappe.whitelist(allow_guest=True)
def diff(t_a = '10:00', t_b = '15:00'):
	in_time = t_a.split(':')
	out_time = t_b.split(':')
	t1 = timedelta(hours=int(in_time[0]), minutes=int(in_time[1]))
	t2 = timedelta(hours=int(out_time[0]), minutes=int(out_time[1]))
	t3 = timedelta(hours=13, minutes=7)
	t4 = timedelta(hours=21, minutes=0)

	arrival = t2 - t1
	lunch = (t3 - t2 - timedelta(hours=1))
	departure = t4 - t3
	return arrival


@frappe.whitelist(allow_guest=True)
def get_setting():

	return frappe.get_single('Overtime Setting')


@frappe.whitelist()
def get_holidays(employee, date):
	'''get holidays between two dates for the given employee'''

	check = False
	holiday_list = get_holiday_list_for_employee(employee)

	holidays = frappe.db.sql("select DATE_FORMAT(holiday_date,'%Y-%m-%d') as date FROM `tabHoliday` WHERE parent = '"+holiday_list+"' ", as_dict=True)
	if holidays:

		for i in holidays:
			holiday_date = str(i.date).split('-')
			posting_date = str(date).split('-')

			if int(posting_date[0]) == int(holiday_date[0]):

				if int(posting_date[1]) == int(holiday_date[1]):

					if int(posting_date[2]) == int(holiday_date[2]):

						return True

	return False

			# else:
			# 	return False
	