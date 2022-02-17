from __future__ import unicode_literals
from six import string_types
import frappe
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate

def execute(filters=None):
    column = get_column()
    data = get_data(filters)
    return column,data

def get_column():
    column = [
        _("Employee") + ":Link/Employee:100",
        _("Employee Name") + ":Data:200",
       _("Contractor") + ":Data:180",
       _("Date") + ":Data:150",
       _("IN Time") + ":Data:70",
       _("Out Time") + ":Data:70",]
    return column

def get_data(filters):
    data= []
    if filters.from_date:
        checkin = frappe.get_all('Attendance',{'attendance_date':filters.from_date},['employee','employee_name','contractor','in' ,'out','attendance_date'])
    for value in checkin:
        row = [value.employee,value.employee_name,value.contractor,value.attendance_date,value['in']]
        row.append(value.out)
        data.append(row)

    return data
