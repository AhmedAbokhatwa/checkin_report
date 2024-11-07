
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
        # {
        #     'fieldname': 'name_att',
        #     'fieldtype': 'Data',
        #     'label': _('Name att'),
        #     'width': 200
        # },
        {
            'fieldname': 'time',
            'fieldtype': 'Date',
            'label': _('Attendance Date'),
            'width': 100
        },
        {
            'fieldname': 'deduction',
            'fieldtype': 'Float',
            'label': _('Deduction'),
            'width': 100
        },
        {
            'fieldname': 'diff',
            'fieldtype': 'Float',
            'label': _('diff in Minutes'),
            'width': 200
        },
		
    ]
from datetime import datetime

def get_data(filters):
    conditions =  ["ec.custom_deduction > '0'"]
    params = []
    data = []
    # conditions.append("dl.punch = '0'")
    # conditions.append("ec.attendance <> 'null'")
    
    
    if filters and filters.get("employee_name"):
        conditions.append("e.employee = %s")
        params.append(filters["employee_name"])
        
    if filters and filters.get("designation"):
        conditions.append("e.designation = %s")
        params.append(filters["designation"])
        
    if filters and filters.get("branch"):
        conditions.append("e.branch = %s")
        params.append(filters["branch"])	
    if filters and filters.get("from_date") and filters.get("to_date"):
        try:
            conditions.append("DATE(ec.time) BETWEEN %s AND %s")
            params.append(filters["from_date"])
            params.append(filters["to_date"])   
        except ValueError:
            raise ValueError(f"Invalid date  Provided")
    condition_str = " AND ".join(conditions)
    sql_query = f"""
        SELECT 
				
            e.employee AS employee,
            e.employee_name AS employee_name,
            e.designation,
            e.branch,
            a.name AS name_att,
            DATE(ec.time) AS time,
            ec.custom_deduction AS deduction,
            (ec.custom_deduction*60 ) AS diff
        FROM 
            `tabEmployee Checkin` ec 
        left JOIN 
            `tabAttendance` a ON ec.attendance = a.name
        left join
            `tabEmployee` e ON e.employee_name = ec.employee_name
        WHERE    
            {condition_str if condition_str else '1=1'}
    """
    employees = frappe.db.sql(sql_query, params, as_dict=True)

    
    for emp in employees:
        data.append(emp)
    return data





