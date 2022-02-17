frappe.query_reports["Daily Gate Entry"] = {
	"filters": [
		{
			"fieldname":"attendance_date",
			"label": __("Attendance Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.nowdate()
		},
		{
			"fieldname":"plant",
			"label": __("Plant"),
			"fieldtype": "Select",
			"reqd": 1,
            "options":["Linear Alkyl Benzene","Heavy Chemicals Division","Propylene Oxide Division"],
            "default":"Linear Alkyl Benzene"
		},
        {
			"fieldname":"shift",
			"label": __("Shift"),
			"fieldtype": "Link",
			"reqd": 1,
			"options":"Shift Type",
            "default":"A Shift"
		},
    ]
}