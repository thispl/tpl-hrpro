# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
from frappe import msgprint, _
from calendar import monthrange

def execute(filters=None):
	if not filters: filters = {}

	conditions, filters = get_conditions(filters)
	columns = get_columns(filters)
	data = get_employees(conditions, filters)

	return columns, data

def get_columns(filters):
	return [
		_("ID") + ":Link/Attendance:120",
		_("Employee") + ":Link/Employee:120", 
		_("Name") + ":Data:200", 
		_("Date")+ ":Date:100",
		_("Department") + ":Link/Department:120",
		_("Contractor") + ":Link/Contractor:120",
		_("Working Hours") + ":Float:200"
		# _("Extra Hours") + ":Data:200",
	]

def get_employees(conditions, filters):
	conditions = get_conditions(filters)
	# frappe.errprint(conditions)
	# frappe.errprint(filters)
	query = """Select name, employee, employee_name, attendance_date,
	department, contractor, working_hours From `tabAttendance` Where docstatus = 1 %s """ % conditions, filters
	# frappe.errprint(query)
	return frappe.db.sql(query, as_list=1)

# def get_conditions(filters):
# 	conditions = ""
# 	if filters.get("month"):
# 		month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
# 			"Dec"].index(filters["month"]) + 1
# 		conditions += " and month(date_of_joining) = '%s'" % month

# 	if filters.get("company"): conditions += " and company = '%s'" % \
# 		filters["company"].replace("'", "\\'")

# 	return conditions

def get_conditions(filters):
	if not (filters.get("month") and filters.get("year")):
		msgprint(_("Please select month and year"), raise_exception=1)

	filters["total_days_in_month"] = monthrange(cint(filters.year), cint(filters.month))[1]

	conditions = " and month(attendance_date) = %(month)s and year(attendance_date) = %(year)s"

	if filters.get("company"): conditions += " and company = %(company)s"
	if filters.get("employee"): conditions += " and employee = %(employee)s"
	frappe.errprint(conditions)
	return conditions, filters