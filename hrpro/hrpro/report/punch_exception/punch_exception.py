# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)


def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()

    data = []
    # row = []
    conditions, filters = get_conditions(filters)
    checkin = get_checkin(conditions, filters)
    for check in checkin:
        data.append(check)
    return columns, data


def get_columns():
    columns = [
        _("ID") + ":Link/Attendance:200",
        _("Attendance Date") + ":Data:200",
        _("Employee") + ":Data:120",
        _("Employee Name") + ":Data:120",
        _("Plant") + ":Data:120",
        _("Shift") + ":Data:120",
        _("In Time") + ":Data:120",
        _("Out Time") + ":Data:120"
    ]
    return columns


def get_checkin(conditions, filters):
    if filters.from_date == nowdate() or filters.to_date == nowdate():
        frappe.throw(_("From Date and To Date not equal to Today Date"))
    else:
        attendance = frappe.db.sql("""Select name,employee, employee_name, department, plant, attendance_date, shift,status, tabAttendance.in as in_time,tabAttendance.out as out_time
        From `tabAttendance` Where %s group by employee,attendance_date"""% conditions,filters, as_dict=1)
        row = []
        for att in attendance:
            if not att.out_time:
                row += [(att.name,att.attendance_date,att.employee,att.employee_name,att.plant,att.shift,att.in_time,att.out_time)]
            if not att.in_time:
                row += [(att.name,att.attendance_date,att.employee,att.employee_name,att.plant,att.shift,att.in_time,att.out_time)]
        return row

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"): conditions += " attendance_date >= %(from_date)s"
    if filters.get("to_date"): conditions += " and attendance_date <= %(to_date)s"
    return conditions, filters