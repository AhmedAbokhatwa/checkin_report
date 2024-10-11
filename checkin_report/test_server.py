import frappe


@frappe.whitelist()
def test():
    employees = frappe.get_list('Employee Checkin',filters={'employee': '2233'}, fields = ['employee','employee_name','time'])
    # print('employeessssssssssssssssssssssssssssssssssdddsss',conditions,len(employees))
    # return employees
    for emp in employees:
        emp["designation"] = frappe.db.get_value('Employee',emp['employee'],'designation')
        emp["branch"] = frappe.db.get_value('Employee',emp['employee'],'branch')
        return emp