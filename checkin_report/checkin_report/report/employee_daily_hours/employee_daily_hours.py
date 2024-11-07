# Copyright (c) 2024, ahmed reda and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "label": _("Employee Code"),
            "width": 200,
        },
        {
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "label": _("Employee Name"),
            "width": 200,
        },
        {
            "fieldname": "attendance_date",
            "fieldtype": "Date",
            "label": _("Attendance Date"),
            "width": 200,
        },
        {
            "fieldname": "namech",
            "fieldtype": "Link",
            "options": "Employee Checkin",
            "label": _("Checkin"),
            "width": 200,
        },
        {
            "fieldname": "late",
            "fieldtype": "Date",
            "label": _("late"),
            "width": 200,
        },
        {
            "fieldname": "early",
            "fieldtype": "Date",
            "label": _("Early"),
            "width": 200,
        },
    ]


def get_data(filters):
    conditions = []
    params = []
    data = []

    if filters and filters.get("employee"):
        print("conditions ready!!!!:")
        conditions.append("ec.employee = %s")
        params.append(filters["employee"])

    if filters and filters.get("attendance_date"):
        try:
            conditions.append("a.attendance_date = %s")
            conditions.append("a.attendance_date is not null")

            print("day is:", filters.get("attendance_date"), "conditions", conditions)
            params.append(filters.get("attendance_date"))
        except ValueError:
            raise ValueError(f"Invalid date  Provided")

    condition_str = " AND ".join(conditions)
    print("condition_str :", condition_str)
    sql_query = f"""
        SELECT 
            ec.employee AS employee,
            ec.employee_name,
			a.attendance_date AS attendance_date,
           	ec.name AS namech,
			ec.custom_deduction AS late,
            ec.custom_early_diiference AS early
        FROM 
            `tabAttendance` a 
        left join 
        	`tabEmployee Checkin` ec
		ON ec.attendance = a.name    
        Where 
			{condition_str if condition_str else '1=1'}
    """
    employees = frappe.db.sql(sql_query, params, as_dict=True)
    return employees

