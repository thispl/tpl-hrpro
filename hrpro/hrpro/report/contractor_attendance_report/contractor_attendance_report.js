frappe.query_reports["Contractor Attendance Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
		},
        {
			"fieldname":"contractor",
			"label": __("Contractor"),
			"fieldtype": "Link",
            "options":'Contractor',
			"reqd": 1
		},
    ]
}