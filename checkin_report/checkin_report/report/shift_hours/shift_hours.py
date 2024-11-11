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
            "width": 220,
        },
        {
            "fieldname": "log_type",
            "fieldtype": "Data",
            "label": _("Log Type"),
            "width": 100,
        },
        {
            "fieldname": "namech",
            "fieldtype": "Link",
            "options": "Employee Checkin",
            "label": _("Checkin"),
            "width": 300,
        },
        {
            "fieldname": "custom_shift_hours",
            "fieldtype": "INT",
            "label": _("Shift Hours"),
            "width": 200,
        },
        #   {
        #     "fieldname": "shift_actual_end",
        #     "fieldtype": "Data",
        #     "label": _("shift_actual_end"),
        #     "width": 200,
        # },
        #   {
        #     "fieldname": "shift_actual_start",
        #     "fieldtype": "Data",
        #     "label": _("shift_actual_start"),
        #     "width": 200,
        # },
        {
            "fieldname": "diff",
            "fieldtype": "Time",
            "label": _("Difference"),
            "width": 200,
        },
    ]

def get_data(filters):
    conditions = []
    params = []

    if filters and filters.get("employee"):
        conditions.append("ec.employee = %s")
        params.append(filters["employee"])

    if filters and filters.get("attendance_date"):
        conditions.append("DATE(ec.time) = %s")
        params.append(filters["attendance_date"])

    conditions.append("ec.log_type IN ('IN', 'OUT')")

    # Construct the base SQL query
    sql = f"""
    SELECT 
        ec.employee AS employee,
        ec.name AS namech,
        ec.employee_name,
        DATE(ec.time) AS attendance_date,
        TIME(ec.time) AS attendance_time,
        TIME(ec.shift_actual_start) AS shift_actual_start,
        TIME(ec.shift_actual_end) AS shift_actual_end,
        st.custom_shift_hours,
        ec.log_type,
        CASE 
            WHEN ec.log_type = 'OUT' THEN TIMEDIFF(TIME(ec.time), TIME(ec.shift_actual_end))
            WHEN ec.log_type = 'IN' THEN TIMEDIFF(TIME(ec.time), TIME(ec.shift_actual_start))
            ELSE NULL
        END AS diff,
        (CASE 
            WHEN ec.log_type = 'OUT' THEN TIMEDIFF(TIME(ec.time), TIME(ec.shift_actual_end))
            WHEN ec.log_type = 'IN' THEN TIMEDIFF(TIME(ec.time), TIME(ec.shift_actual_start))
            ELSE NULL
        END) - st.custom_shift_hours AS diff_actual
    FROM    
        `tabEmployee Checkin` ec
    LEFT JOIN
        `tabShift Type` st ON st.name = ec.shift
"""


    # Append conditions if there are any
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    # Add a LIMIT if required (e.g., LIMIT 2 for testing)
    sql += " LIMIT 2"

    # Execute the query with the filter values
    mydata = frappe.db.sql(sql, params, as_dict=True)
    return mydata
