frappe.query_reports["RC Summary"] = {
	"filters": [
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.month_start()
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.month_end()
		},
        {
			"fieldname":"plant",
			"label": __("Plant"),
			"fieldtype": "Select",
            "options":["Linear Alkyl Benzene","Heavy Chemicals Division","Propylene Oxide Division"],
			"reqd": 1,
			"default": "Linear Alkyl Benzene"
		}
    ]
}