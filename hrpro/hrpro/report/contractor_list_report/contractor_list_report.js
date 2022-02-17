frappe.query_reports["Contractor List Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __(" From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default": frappe.datetime.nowdate()
			"default": '2021-08-05'
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default": frappe.datetime.nowdate()
			"default": '2021-08-05'
		},
		
		
    ]
}