from __future__ import unicode_literals
from six import string_types
import frappe
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime, time, timedelta
import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate

def execute(filters=None):
	columns, data = get_column(), get_data(filters)
	return columns, data

def get_column():
	column = [ _("Contractor Name") + ":Data:200",
				 _("Count ") + ":Data:100",]
	return column

def get_data(filters):
	data = []
	
	contractor_list = frappe.get_all('Contractor',['*']) 
	for contractor in contractor_list:
		contractor_count = frappe.db.count('Attendance',{'attendance_date':filters.from_date},{'contractor':contractor.name})
		# frappe.errprint(contractor_count)
		row = [contractor.name,]
		if contractor_count:
			row.append(contractor_count)
		else:
			row.append('-')
		data.append(row)
	return data


