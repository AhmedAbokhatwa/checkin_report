import frappe
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns = [
        # {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "width": 200},
        {"fieldname": "employee_name", "label": "Employee Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "first_log", "label": "First Log", "fieldtype": "Datetime", "width": 200},
        {"fieldname": "last_log_within_24_hours", "label": "Last Log", "fieldtype": "Datetime", "width": 200},
        {"fieldname": "shift", "label": "Shift", "fieldtype": "Data", "width": 70},
        {"fieldname": "custom_shift_hours", "label": "Shift Hours", "fieldtype": "Time", "width": 100},
        {"fieldname": "over_time", "label": "Overtime", "fieldtype": "Time", "width": 100},
        {"fieldname": "deduction", "label": "Deduction", "fieldtype": "Time", "width": 100},
        {"fieldname": "diff_time", "label": "Total Hrs", "fieldtype": "Time", "width": 100},
        
    ]
    return columns

def get_data(filters):
    employee = filters.get("employee")
    from_date = filters.get("from")
    to_date = filters.get("to")
    shift = filters.get("shift")
    employee_filter = f"AND ec_in.employee = %(employee)s" if employee else ""
    # shift_filter = f"AND ec_in.shift = %(shift)s" if shift else ""
    date_filter = f"AND DATE(ec_in.time) BETWEEN %(from_date)s AND %(to_date)s" if from_date and to_date else ""
    if filters.get("employee") and filters.get("from") and filters.get("to"):
        sql = f"""
              WITH previous_log_in AS (
    SELECT 
        ec_in.employee,
        ec_in.employee_name,
        ec_in.shift,
        ec_in.time AS first_log,
        LAG(ec_in.time) OVER (PARTITION BY ec_in.employee ORDER BY ec_in.time) AS previous_log,
        DATE(ec_in.time) AS date_of_log_in,
        TIMESTAMPDIFF(HOUR, LAG(ec_in.time) OVER (PARTITION BY ec_in.employee ORDER BY ec_in.time), ec_in.time) >= 24 AS stamp
    FROM 
        `tabEmployee Checkin` ec_in
    WHERE 
        ec_in.log_type = 'IN'
        AND ec_in.shift = 'General'
        {employee_filter}
        {date_filter}
),
LastLogWithin24Hours AS (
    SELECT 
        fl.employee,
        fl.first_log,
        MAX(ec_out.time) AS last_log_within_24_hours,
        st.custom_shift_hours,
        COALESCE(TIMEDIFF(MAX(ec_out.time), fl.first_log), '00:00:00') AS diff_time,
        COALESCE(TIMESTAMPDIFF(SECOND, fl.first_log, MAX(ec_out.time)) / 3600.0, 0) AS diff_time_float,
        -- Overtime: Time worked beyond shift hours
        CASE
            WHEN TIMESTAMPDIFF(SECOND, fl.first_log, MAX(ec_out.time)) > TIME_TO_SEC(st.custom_shift_hours) THEN
                SEC_TO_TIME(TIMESTAMPDIFF(SECOND, fl.first_log, MAX(ec_out.time)) - TIME_TO_SEC(st.custom_shift_hours))
            ELSE '00:00:00'
        END AS over_time,

        -- Deduction: Missing time to complete shift hours
        CASE
            WHEN TIMESTAMPDIFF(SECOND, fl.first_log, MAX(ec_out.time)) < TIME_TO_SEC(st.custom_shift_hours) THEN
                SEC_TO_TIME(TIME_TO_SEC(st.custom_shift_hours) - TIMESTAMPDIFF(SECOND, fl.first_log, MAX(ec_out.time)))
            ELSE '00:00:00'
        END AS deduction
        
    FROM 
        previous_log_in fl
    JOIN 
        `tabEmployee Checkin` ec_out ON ec_out.employee = fl.employee
    LEFT JOIN 
        `tabShift Type` st ON st.name = fl.shift
    WHERE 
        ec_out.log_type = 'OUT'
        AND ec_out.shift = 'General'  -- Filter only General shift
        AND ec_out.time > fl.first_log
        AND ec_out.time <= fl.first_log + INTERVAL 1 DAY
    GROUP BY 
        fl.employee, fl.first_log, st.custom_shift_hours
)
SELECT * 
FROM LastLogWithin24Hours
JOIN previous_log_in fl 
    ON fl.employee = LastLogWithin24Hours.employee 
    AND fl.first_log = LastLogWithin24Hours.first_log
WHERE fl.previous_log IS NULL OR fl.stamp = 1;



            """
        return frappe.db.sql(sql, 
                             {
            "employee": filters.get("employee"),
            "from_date": filters.get("from"),
            "to_date": filters.get("to"),
            "shift": filters.get("shift"),
        },
          as_dict=True)
