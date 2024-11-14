// Copyright (c) 2024, ahmed reda and contributors
// For license information, please see license.txt

frappe.query_reports["shift hours"] = {
	"filters": [
    { 
      fieldname: "employee",
      fieldtype: "Link",
      options: "Employee",
      label: __("Employee Name"),
    },
    {
      fieldname: "attendance_date",
      fieldtype: "Date",
      label: __("Date"),
    },
	]
};
