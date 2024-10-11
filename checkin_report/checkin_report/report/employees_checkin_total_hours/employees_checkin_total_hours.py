# # # import frappe
# # # from frappe import _

# # # def execute(filters=None):
# # #     data = get_data(filters)
# # #     return data

# # # def get_data(filters):
# # #     # Initialize an empty conditions dictionary
# # #     conditions = {}
    
# # #     # Add filters if they exist
# # #     if filters and filters.get("employee"):
# # #         conditions["employee"] = filters.get("employee")
# # #     if filters and filters.get("employee_name"):
# # #         conditions["employee_name"] = filters.get("employee_name")
    
# # #     # Fetch employee data
# # #     employees = frappe.get_list("Employee Checkin", fields=["employee"], filters=conditions)

# # #     # Optionally, you could enhance this to include additional employee details
# # #     for emp in employees:
# # #         emp["designation"] = frappe.get_value('Employee', emp['employee'], 'designation')
# # #         emp["branch"] = frappe.get_value('Employee', emp['employee'], 'branch')

# # #     return employees






# # # Copyright (c) 2024, ahmed reda and contributors
# # # For license information, please see license.txt

# # import frappe
# # from frappe import _

# # def execute(filters=None):
# # 	columns = get_columns()
# # 	data = get_data(filters)
# # 	return  columns, data

# # # //g


# # def get_columns():
# # 	return[
# # 		{
# # 			'fieldname':'employee',
# # 			'fieldtype':'Link',
# # 			'options':'Employee',
# # 			'label':_('Employee Code'),
# # 			"width": 100
# # 		},
# # 		{
# # 			'fieldname':'employee_name',
# # 			'fieldtype':'Data',
# # 			'options':'Employee',
# # 			'label':_('Employee Name'),
# # 			"width": 100
# # 		},
# # 		{
# # 			'fieldname':'designation',
# # 			'fieldtype':'Link',
# # 			'options':'Designation',
# # 			'label':_('Designation'),
# # 			"width": 100
# # 		},
# # 		{
# # 			'fieldname':'branch',
# # 			'fieldtype':'Link',
# # 			'options':'Branch',
# # 			'label':_('Branch'),
# # 			"width": 100
# # 		},
# # 		{
# # 			'fieldname':'time',
# # 			'fieldtype':'Date',		
# # 			'label':_('Date'),
# # 			"width": 100
# # 		},
# # 	]
	
# # def get_data(filters):
# # 	conditions={}
# # 	if filters.get("employee"):
# # 		conditions["employee"] = filters.get("employee")
# # 	# if filters.get("employee_name"):
# # 	# 	conditions["employee_name"] = filters.get("employee_name")
# # 		employees = frappe.get_list('Employee Checkin',filters={'employee': '2233'}, fields = ['employee','employee_name','time'])
# # 		print('employeessssssssssssssssssssssssssssssssssdddsss',conditions,len(employees))
# # 		for emp in employees:
# # 			emp["designation"] = frappe.db.get_value('Employee',emp['employee'],'designation')
# # 			emp["branch"] = frappe.db.get_value('Employee',emp['employee'],'branch')
# # 			# print('employees',employees)
# # 			return emp
# # 		# 	# print('employees',emp)

# import frappe
# from frappe import _

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         {
#             'fieldname': 'employee',
#             'fieldtype': 'Link',
#             'options': 'Employee',
#             'label': _('Employee Code'),
#             'width': 200
#         },
#         {
#             'fieldname': 'employee_name',
#             'fieldtype': 'Data',
#             'options': 'Employee',
#             'label': _('Employee Name'),
#             'width': 200
#         },
#         {
#             'fieldname': 'designation',
#             'fieldtype': 'Link',
#             'options': 'Designation',
#             'label': _('Designation'),
#             'width': 200
#         },
#         {
#             'fieldname': 'branch',
#             'fieldtype': 'Link',
#             'options': 'Branch',
#             'label': _('Branch'),
#             'width': 200
#         },
#         {
#             'fieldname': 'time',
#             'fieldtype': 'Datetime',
#             'label': _('Date'),
#             'width': 200
#         },
#         {
#             'fieldname': 'working_hours',
#             'fieldtype': 'Data',
#             'label': _('working_hours'),
#             'width': 200
#         },
#         {
#             'fieldname': 'attendance_date',
#             'fieldtype': 'Date',
#             'label': _('Date'),
#             'width': 200
#         },
#     ]

# def get_data(filters):
#     conditions = {}
    

#     if filters and filters.get("employee"):
#         conditions["employee"] = filters["employee"]
	
#     if filters.get("attendance_date"):
#         conditions["attendance_date"] = filters["attendance_date"]


#     employees = frappe.get_list(
#         'Employee Checkin',
#         filters=conditions,
#         fields=['employee', 'employee_name', 'time','attendance']
#     )

#     data = []
#     for emp in employees:
#         emp["designation"] = frappe.db.get_value('Employee', emp['employee'], 'designation')
#         emp["branch"] = frappe.db.get_value('Employee', emp['employee'], 'branch')
#         emp["working_hours"] = frappe.db.get_value('Attendance', emp['attendance'], 'working_hours')
#         emp["attendance_date"] = frappe.db.get_value('Attendance', [emp['attendance'],conditions], 'attendance_date')
#         data.append(emp)

#     return data



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
            'width': 200
        },
        {
            'fieldname': 'attendance_date',
            'fieldtype': 'Date',
            'label': _('Attendance Date'),
            'width': 200
        },
    ]
from datetime import datetime

def get_data(filters):
    conditions = []
    params = []
    data = []

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
            conditions.append("a.attendance_date = %s")
            print("daaaaaaaaaa",filters.get("attendance_date"),"conditions",conditions)
            params.append(filters.get("attendance_date"))
        except ValueError:
            raise ValueError(f"Invalid date  Provided")
    condition_str = " AND ".join(conditions)
    sql_query = f"""
        SELECT 
            ec.employee,
            ec.employee_name,
            ec.time,
            ec.attendance,
            e.designation,
            e.branch,
            a.working_hours,
            a.attendance_date
        FROM 
            `tabEmployee Checkin` ec
        JOIN 
            `tabEmployee` e ON ec.employee = e.name
        LEFT JOIN 
            `tabAttendance` a ON ec.attendance = a.name
        WHERE 
            {condition_str if condition_str else '1=1'}
    """
    employees = frappe.db.sql(sql_query, params, as_dict=True)

    
    for emp in employees:
        data.append(emp)
    return data






