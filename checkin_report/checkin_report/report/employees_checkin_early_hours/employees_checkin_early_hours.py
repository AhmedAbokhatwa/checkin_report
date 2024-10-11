# Copyright (c) 2024, ahmed reda and contributors
# For license information, please see license.txt

# import frappe
#  SELECT 
#             ec.employee AS employee,
#             e.employee_name AS employee_name,
#             ec.time,
#             ec.attendance AS attendance,
#             e.designation,
#             e.branch,
#             a.working_hours AS working_hours,
#             a.attendance_date AS attendance_date, 
#             dl.punch
#         FROM 
#             `tabEmployee Checkin` ec
#         JOIN 
#             `tabEmployee` e ON ec.employee = e.name
#         LEFT JOIN 
#             `tabAttendance` a ON ec.attendance = a.name
# 		LEFT JOIN 
#             `tabDevice Log` dl ON dl.name = ec.device_log    
#         WHERE  ec.employee ='2233'

import frappe
from frappe import _
from frappe.utils import (
	add_days,
	add_months,
	add_to_date,
	date_diff,
	flt,
	format_date,
	get_datetime,
	nowdate,
)
def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            'fieldname': 'employee',
            'fieldtype': 'Link',
            'options': 'Employee',
            'label': _('Employee Code'),
            'width': 200
        },
        {
            'fieldname': 'employee_name',
            'fieldtype': 'Data',
            'options': 'Employee',
            'label': _('Employee Name'),
            'width': 200
        },
        {
            'fieldname': 'designation',
            'fieldtype': 'Link',
            'options': 'Designation',
            'label': _('Designation'),
            'width': 200
        },
        {
            'fieldname': 'branch',
            'fieldtype': 'Link',
            'options': 'Branch',
            'label': _('Branch'),
            'width': 200
        },
        {
            'fieldname': 'time',
            'fieldtype': 'Datetime',
            'label': _('Time'),
            'width': 200
        },
        {
            'fieldname': 'working_hours',
            'fieldtype': 'Data',
            'label': _('Working Hours'),
            'width': 100
        },
        {
            'fieldname': 'attendance_date',
            'fieldtype': 'Date',
            'label': _('Attendance Date'),
            'width': 200
        },
        # {
        #     'fieldname': 'punch',
        #     'fieldtype': 'Int',
        #     'label': _('punch'),
        #     'width': 200
        # },
        {
            'fieldname': 'shift_actual_start',
            'fieldtype': 'Datetime',
            'label': _('shift Actual start'),
            'width': 200
        },
        {
            'fieldname': 'diff',
            'fieldtype': 'Int',
            'label': _('diff in Minutes'),
            'width': 200
        },
		
    ]
from datetime import datetime

def get_data(filters):
    conditions = []
    params = []
    data = []
    # conditions.append("dl.punch = '1'")
    conditions.append("ec.attendance <> 'null'")
    
    
    if filters and filters.get("employee_name"):
        conditions.append("ec.employee = %s")
        params.append(filters["employee_name"])
        
    if filters and filters.get("designation"):
        conditions.append("e.designation = %s")
        params.append(filters["designation"])
        
    if filters and filters.get("branch"):
        conditions.append("e.branch = %s")
        params.append(filters["branch"])	
    if filters and filters.get("attendance_date"):
        try:
            conditions.append("ec.attendance_date = %s")
            print("daaaaaaaaaa",filters.get("attendance_date"),"conditions",conditions)
            params.append(filters.get("attendance_date"))
        except ValueError:
            raise ValueError(f"Invalid date  Provided")
    condition_str = " AND ".join(conditions)
    sql_query = f"""
        SELECT 
			TIMESTAMPDIFF(MINUTE, ec.shift_actual_start, ec.time) AS diff,	
            ec.employee AS employee,
            e.employee_name AS employee_name,
            ec.time,
            ec.attendance AS attendance,
            e.designation,
            e.branch,
            ec.shift_actual_start AS shift_actual_start,
            a.working_hours AS working_hours,
            a.attendance_date AS attendance_date, 
            dl.punch
        FROM 
            `tabEmployee Checkin` ec
        JOIN 
            `tabEmployee` e ON ec.employee = e.name
        LEFT JOIN 
            `tabAttendance` a ON ec.attendance = a.name
		LEFT JOIN 
            `tabDevice Log` dl ON dl.name = ec.device_log    
        WHERE 
	
            {condition_str if condition_str else '1=1'}
    """
    employees = frappe.db.sql(sql_query, params, as_dict=True)

    
    for emp in employees:
        data.append(emp)
    return data






