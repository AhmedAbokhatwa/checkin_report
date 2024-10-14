import frappe


@frappe.whitelist()
def test():
    # Define SQL query
    sql_query = """
        SELECT 
            e.employee AS employee,
            e.employee_name AS employee_name,
            e.designation,
            e.branch,
            a.name AS name_att,
            a.attendance_date AS attendance_date,
            ec.custom_early_diiference AS deduction,
            (ec.custom_early_diiference * 60) AS diff
        FROM 
            `tabEmployee Checkin` ec 
        right JOIN 
            `tabAttendance` a ON ec.attendance = a.name
        left join `tabEmployee` e
        ON a.employee_name = e.employee_name
    """
    # Execute SQL query and return result as a dictionary
    emp = frappe.db.sql(sql_query, as_dict=True)

    # 
    print(emp)
    


