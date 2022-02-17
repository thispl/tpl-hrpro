frappe.query_reports["Attendance Report Daily"] = {
	"filters": [
        {
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options":"Employee",
            "reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
            "reqd": 1
		},
        {
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
            "reqd": 1
		},
        
    ]
}