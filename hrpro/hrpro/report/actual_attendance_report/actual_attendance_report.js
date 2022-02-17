frappe.query_reports["Actual Attendance Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1,
			// "default": frappe.datetime.nowdate()
			"default": '2021-08-05'
		},
		
    ]
}