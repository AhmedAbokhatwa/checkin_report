// Copyright (c) 2024, ahmed reda and contributors
// For license information, please see license.txt

frappe.query_reports["employ early and late hours"] = {
	"filters": [
      {
        "fieldname":"employee",
        "label":__("الموظف"),
        "fieldtype":"Link",
        "options":"Employee",
        "width":"270"
      },
      {
        "fieldname":"employee",
        "label":__("اسم الموظف"),
        "fieldtype":"Link",
        "options":"Employee",
        "width":"270"
      },
      {
        "fieldname":"attendance_date",
        "label":__("تاريخ الحضور"),
        "fieldtype":"Date",
        
        "width":"270"
      }
	]
};
