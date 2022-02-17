// Copyright (c) 2016, Teampro and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PF Report"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": '2021-07-01',
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default":'2021-07-05',
            "reqd": 1
        },
    ]
}