from __future__ import unicode_literals
from frappe import _
import frappe

def get_data():

	return [
		{
			"label": _("Overtime"),
			"items": [
				{
					"type": "doctype",
					"name": "overtime",
					"description": _("For overtime.")
				},
				{
					"type":"doctype",
					"name":"Overtime Slip",
					"description":_("For Overtime Slip.")
				},
				{
					"type":"doctype",
					"name":"Overtime Approved",
					"description":_("For Overtime Approved.")
				}
			]

		},
		{
			"label": _("Overtime Report"),
			"items": [
				{
					"type": "report",
					"name":"Monthly Overtime",
					"doctype": "overtime",
					"is_query_report": True,
				},
			]
		},
		{
			"label":_("Overtime Setting"),
			"items":[
				{
					"type":"doctype",
					"name":"Overtime Setting",
					"description":_("For Overtime Setting")
				}
			]
		},
		{
			"label": _("Help"),
			"items": [
				{
					"type": "dropdown",
					"label": _("Please Contact To HR Department")
				}
			]
		}
	]
