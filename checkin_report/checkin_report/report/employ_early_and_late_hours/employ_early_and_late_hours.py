# Copyright (c) 2024, ahmed reda and contributors
# For license information, please see license.txt

import frappe
from frappe import _ 

def execute(filters=None):
    columns = get_cols()
    data = get_data(filters)    
    return columns, data

def get_cols():
    return [
        {
            "fieldname": "employee",
            "label": _("الموظف"),
            "fieldtype": "Link",
            "options": "Employee",
            "width": "270"
        },
        {
            "fieldname": "attendance_date",
            "label": _("تاريخ الحضور"),
            "fieldtype": "Date",
            "width": "270"
        },
          {
            "fieldname": "custom_shift_hours",
            "label": _("عدد ساعات الشيفت"),
            "fieldtype": "Date",
            "width": "160"
        },
          {
            "fieldname": "diff_positive",
            "label": _("حضور الباكر"),
            "fieldtype": "Date",
            "width": "270"
        },
          {
            "fieldname": "diff_negative",
            "label": _("الحضور المتاخر"),
            "fieldtype": "Date",
            "width": "270"
        }
    ]

def get_data(filters):  
    conditions = [] 
    params = []
    if filters and filters.get("employee"):
        conditions.append("ec_in.employee = %s")
        params.append(filters["employee"])
        
    if filters and filters.get("attendance_date"):
        conditions.append("DATE(ec_in.time) = %s")
        params.append(filters["attendance_date"])

    sql = """
        SELECT 
            ec_in.employee AS employee_id,
            ec_in.name AS namech_in,
            ec_in.employee_name AS employee,
            DATE(ec_in.time) AS attendance_date,
            MIN(ec_in.time) AS first_checkin_time,
            MAX(ec_in.time) AS last_checkin_time,
            TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)) AS time_difference,
            COUNT(ec_in.name) AS checkin_count,
            st.custom_shift_hours,
            CASE 
                WHEN COUNT(ec_in.name) < 2 THEN TIME('00:00:00')
                WHEN TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)) > st.custom_shift_hours 
                THEN TIMEDIFF(TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)), st.custom_shift_hours)
                ELSE NULL
            END AS diff_positive,
            CASE 
                WHEN COUNT(ec_in.name) < 2 THEN TIME('00:00:00')
                WHEN TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)) < st.custom_shift_hours 
                THEN TIMEDIFF(st.custom_shift_hours, TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)))
                ELSE NULL
            END AS diff_negative
        FROM 
            `tabEmployee Checkin` ec_in
        LEFT JOIN 
            `tabShift Type` st ON st.name = ec_in.shift
        WHERE 
            ec_in.employee_name IS NOT NULL
    """

    if conditions:
        sql += " AND " + " AND ".join(conditions)

    sql += """
        GROUP BY 
            ec_in.employee, DATE(ec_in.time)
        ORDER BY 
            ec_in.employee, attendance_date;
    """

    data = frappe.db.sql(sql, params, as_dict=True)
    return data
