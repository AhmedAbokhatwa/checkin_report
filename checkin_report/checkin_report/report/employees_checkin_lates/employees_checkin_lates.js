// Copyright (c) 2024, ahmed reda and contributors
// For license information, please see license.txt

frappe.query_reports["employees Checkin Lates"] = {
	"filters": [
			//  {
			// 	'fieldname':'employee',
			// 	'fieldtype':'Link',
			// 	'options':'Employee',
			// 	'label':__('Employee Code')
			// },
			{
				'fieldname':'employee_name',
				'fieldtype':'Link',
				'options':'Employee',
				'label':__('Employee Name')
			},
			{
				'fieldname':'designation',
				'fieldtype':'Link',
				'options':'Designation',
				'label':__('Designation')
			},
			{
				'fieldname':'branch',
				'fieldtype':'Link',
				'options':'Branch',
				'label':__('Branch')
			},
			{
				'fieldname':'attendance_date',
				'fieldtype':'Date',
				'label':__('Date')
			},
	]
};
