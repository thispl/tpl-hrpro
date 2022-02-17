# Copyright (c) 2013, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from six.moves import range
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
from itertools import count



def execute(filters=None):
    if not filters:
        filters = {}
    columns = get_columns()
    data = []
    row = []
    conditions, filters = get_conditions(filters)
    attendance = get_attendance(conditions,filters)
    for att in attendance:
        data.append(att)
    return columns, data


def get_columns():
    columns = [
        _("ID") + ":Data:200",
        _("Start Date") + ":Date:200",
        _("End Date") + ":Date:200",
        _("Employee") + ":Data:120",
        _("Employee Name") + ":Data:120",
        _("PF Non-Compliance") + ":Check:120",
        _("PF Paid") + ":Currency:120",
        _("ESI Non-Compliance") + ":Check:120",
        _("ESI Paid") + ":Currency:120",
    ]
    return columns


def get_attendance(conditions,filters):
    salary_slip = frappe.db.sql("""Select name,employee, employee_name,start_date,end_date,pf_non_compliance,pf_paid,esi_non_compliance,esi_paid
    From `tabSalary Slip` Where non_compliance = 1 and %s """% conditions,filters, as_dict=1)
    row = []
    for ss in salary_slip:
        row += [(ss.name,ss.start_date,ss.end_date,ss.employee,ss.employee_name,ss.pf_non_compliance,ss.pf_paid,ss.esi_non_compliance,ss.esi_paid)]
    return row

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"): conditions += " start_date >= %(from_date)s"
    if filters.get("to_date"): conditions += " and end_date <= %(to_date)s"
    if filters.get("company"): conditions += " and company = %(company)s"
    if filters.get("employee"): conditions += " and employee = %(employee)s"
    if filters.get("department"): conditions += " and department = %(department)s"

    return conditions, filters