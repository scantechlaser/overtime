from frappe import _

def get_data():
	return {
		'fieldname': 'overtime_approved',
		'internal_links': {
			'Employee': ['items', 'ot_id']
		}
	}