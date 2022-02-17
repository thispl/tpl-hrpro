// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Wage Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From"),
			"fieldtype": "Date",
			 "default": '2021-08-01',
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"default": '2021-08-30',
			"reqd": 1,
			"width": "100px"
		},
	
		// {
		// 	"fieldname":"plant",
		// 	"label": __("Plant"),
		// 	"fieldtype": "Link",
		// 	"options": "Plant",
		// 	"width": "100px"
		// },
		{
			"fieldname":"conractor",
			"label": __("Contractor"),
			"fieldtype": "Link",
			"options": "Contractor",
			"width": "100px"
		},
		// {
		// 	"fieldname":"employment_type",
		// 	"label": __("Employment Type"),
		// 	"fieldtype": "Link",
		// 	"options": "Employment Type",
		// 	"width": "100px"
		// },
	]
}