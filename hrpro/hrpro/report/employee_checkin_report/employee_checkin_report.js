frappe.query_reports["Employee Checkin Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
		},
		
    ]
}