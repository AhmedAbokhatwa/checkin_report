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
        # {
        #     "fieldname": "log_type",
        #     "fieldtype": "Data",
        #     "label": _("Log Type"),
        #     "width": 100,
        # },
        # {
        #     "fieldname": "namech_in",
        #     "fieldtype": "Link",
        #     "options": "Employee Checkin",
        #     "label": _("Checkin"),
        #     "width": 300,
        # },
        {
            "fieldname": "custom_shift_hours",
            "fieldtype": "INT",
            "label": _("Shift Hours"),
            "width": 200,
        },
        #   {
        #     "fieldname": "shift_actual_end",
        #     "fieldtype": "Time",
        #     "label": _("shift_actual_end"),
        #     "width": 200,
        # },
        #   {
        #     "fieldname": "shift_actual_start",
        #     "fieldtype": "Time",
        #     "label": _("shift_actual_start"),
        #     "width": 200,
        # },
        {
            "fieldname": "time_diff",
            "fieldtype": "datetime",
            "label": _("time"),
            "width": 200,
        },
        {
            "fieldname": "time_diff2",
            "fieldtype": "Time",
            "label": _("Difference"),
            "width": 200,
        },
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
        # conditions.append("ec.log_type IN ('IN', 'OUT')")

    # Construct the base SQL query
    sql = f"""
        SELECT 
        ec_in.employee AS employee,
        ec_in.name AS namech_in,
        ec_out.name AS namech_out,
        ec_in.employee_name,
        DATE(ec_in.time) AS attendance_date,
        ec_in.time AS in_time,
        ec_out.time AS out_time,
        TIME(ec_in.shift_actual_start) AS shift_actual_start,
        TIME(ec_in.shift_actual_end) AS shift_actual_end,
        st.custom_shift_hours,
        TIMEDIFF(ec_out.time, ec_in.time) AS time_diff,
       TIMEDIFF(st.custom_shift_hours,TIMEDIFF(ec_out.time, ec_in.time)) AS time_diff2
    FROM 
    `tabEmployee Checkin` ec_in
    JOIN 
        `tabEmployee Checkin` ec_out ON ec_in.employee = ec_out.employee 
            AND DATE(ec_in.time) = DATE(ec_out.time)
            AND ec_in.log_type = 'IN'
            AND ec_out.log_type = 'OUT'
    LEFT JOIN
        `tabShift Type` st ON st.name = ec_in.shift
"""


    # Append conditions if there are any
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

        # Add a LIMIT if required (e.g., LIMIT 2 for testing)
        sql += " LIMIT 2"

    # Execute the query with the filter values
    mydata = frappe.db.sql(sql, params, as_dict=True)
    return mydata






# SELECT 
#     ec_in.employee AS employee_id,
#     ec_in.name AS namech_in,
#     ec_in.employee_name,
#     DATE(ec_in.time) AS attendance_date,
#     MIN(ec_in.time) AS first_checkin_time,
#     MAX(ec_in.time) AS last_checkin_time,
#     TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)) AS time_difference,
#     COUNT(ec_in.name) AS checkin_count,
#     st.custom_shift_hours,
    
#     CASE 
#         WHEN TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)) > st.custom_shift_hours 
#         THEN time(TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)) - st.custom_shift_hours)
#         ELSE NULL
#     END AS diff_positive,
    
#     CASE 
#         WHEN TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)) < st.custom_shift_hours 
#         THEN time(st.custom_shift_hours - TIMEDIFF(MAX(ec_in.time), MIN(ec_in.time)))
#         ELSE NULL
#     END AS diff_negative

# FROM 
#     `tabEmployee Checkin` ec_in
# LEFT JOIN 
#     `tabShift Type` st ON st.name = ec_in.shift
# WHERE 
#     ec_in.employee_name IS NOT NULL
    
# GROUP BY 
#     ec_in.employee, DATE(ec_in.time)
# ORDER BY 
#     ec_in.employee, attendance_date;
