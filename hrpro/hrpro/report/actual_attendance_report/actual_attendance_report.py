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
    column = [
        _("Employee Name") + ":Data:200",
          _("Employee") + ":Link/Employee:100",
                 _("Shift") + ":Data:150",
       _("Contractor Name") + ":Data:180",
      _("IN Time") + ":Data:70",
       _("Out Time") + ":Data:70",
        _("Working Hours") + ":Data:150",
         _("Extra Hours") + ":Data:150",]

    return column

def get_data(filters):
    data= []
    if filters.from_date:
        actual = frappe.get_all('Attendance',{'attendance_date':filters.from_date},['employee','employee_name','contractor','in' ,'out','shift','total_working_hours'])
        
    for value in actual:
        extra_hr = timedelta(0,0,0)
        work_hours = timedelta(0,0,0)
        if value.total_working_hours:
            # frappe.errprint(type(value.total_working_hours))
            if value.total_working_hours > datetime.timedelta(hours=8):
                extra_hr = value.total_working_hours - datetime.timedelta(hours=8)
                work_hours = datetime.timedelta(hours=8)
            else:
                extra_hr = timedelta(0,0,0)
                work_hours =value.total_working_hours
        row = [value.employee_name,value.employee,value.shift,value.contractor,value['in'],value.out,work_hours,extra_hr]   
        data.append(row)
    return data
