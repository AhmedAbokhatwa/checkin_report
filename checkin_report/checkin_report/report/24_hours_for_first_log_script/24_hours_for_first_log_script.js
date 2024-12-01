// Copyright (c) 2024, ahmed reda and contributors
// For license information, please see license.txt

frappe.query_reports["24 hours for first log Script"] = {
  "filters": [
    {
        "fieldname": "employee",
        "label": __("Employee Name"),
        "fieldtype": "Link",
        "options": "Employee",
        "width": 270
    },
    {
        "fieldname": "from",
        "label": __("From Date"),
        "fieldtype": "Date",
        "width": 270
    },
    {
        "fieldname": "to",
        "label": __("To Date"),
        "fieldtype": "Date",
        "width": 270
    },

    
]
};
