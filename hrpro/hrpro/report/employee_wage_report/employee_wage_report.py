from __future__ import unicode_literals
from six import string_types
import frappe
import json
from frappe.utils import (data, getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime, time, timedelta
import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate

def execute(filters=None):
    columns, data = get_column(),get_data(filters)
    # frappe.errprint(data)
    return columns, data

def get_column():
    column =[  _("Employee Name") + ":Data:250",
          _("Employee") + ":Link/Employee:100",
          _("Total Payment Days") + ":Data:70",
       _("Basic") + ":Data:100",
          _("DA") + ":Data:100",
           _("PF Employee") + ":Data:100",
       _("PF Employer") + ":Data:100",
        _(" ESI Employee") + ":Data:100",
        _(" ESI Employer") + ":Data:100",
         _("Total PF") + ":Data:100",
         _("Total ESI") + ":Data:100",
         _("Gross Salary") + ":Data:100",
         _("Net Salary") + ":Data:100"]
    return column

def get_data(filters):
    data = []
    values = frappe.db.sql("select name,`tabSalary Slip`.employee_name as employee_name,`tabSalary Slip`.employee as employee,`tabSalary Slip`.payment_days as payment_days,`tabSalary Slip`.net_pay as net_pay,`tabSalary Slip`.gross_pay as gross_pay from `tabSalary Slip` where `tabSalary Slip`.start_date between '%s'and '%s'"%(filters.from_date,filters.to_date),as_dict=True)
    if filters.contractor:
        values = frappe.db.sql("select name,`tabSalary Slip`.employee_name as employee_name,`tabSalary Slip`.employee as employee,`tabSalary Slip`.payment_days as payment_days,`tabSalary Slip`.net_pay as net_pay,`tabSalary Slip`.gross_pay as gross_pay from `tabSalary Slip` where `tabSalary Slip`.contractor = '%s' and `tabSalary Slip`.start_date between '%s'and '%s'"%(filters.contractor,filters.from_date,filters.to_date),as_dict=True)
    for value in values:
        
        row = [value.employee_name,value.employee,value.payment_days,]
        basic = frappe.db.get_value("Salary Detail",{'abbr':'B','parent':value.name},'amount' )
        dearness = frappe.db.get_value("Salary Detail",{'abbr':'DA','parent':value.name},'amount' )
        employee_pf = frappe.db.get_value("Salary Detail",{'abbr':'PF','parent':value.name},'amount' )
        employee_esi = frappe.db.get_value("Salary Detail",{'abbr':'ESI','parent':value.name},'amount')
        frappe.errprint(value.employee_name)
        # row.append(basic or 0)
        # row.append(dearness or 0)
        # row.append(employee_pf)
        if basic and dearness:
            basic_da = basic + dearness
        else:
            basic_da = 0

        employer_pf = basic_da * 0.12
        employer_esi = basic_da * 0.0075
        row.append(basic )  
        row.append(dearness)
        row.append(employee_pf)
        row.append(employer_pf)
        row.append(employee_esi)  
        row.append(employer_esi)
        if employee_pf and employer_pf:
            total_pf = employee_pf + employer_pf
        else:
            total_pf=0
        row.append(total_pf)
        if employee_esi and employer_esi:       
            total_esi = employee_esi + employer_esi
        else:
            total_esi = 0
        row.append(total_esi)
        row.append(value.gross_pay)
        row.append(value.net_pay)
        data.append(row)
    return data
