# -*- coding: utf-8 -*-
# Copyright (c) 2020, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document

class AnnualPF(Document):
    pass
def generate_pf():
    Employees = frappe.get_all("Employee",{"status": "Active"})
    spf=[]
    month=frappe._dict({
        1 :"January",
        2:"February",
        3:"March",
        4:"April",
        5:"May",
        6:"June",
        7 :"July",
        8:"August",
        9:"September",
        10:"October",
        11:"November",
        12:"December"
        })
        # print(month["July"])
    
    for emp in Employees:
        ss=frappe.db.sql("""SELECT MAX(start_date) ,name FROM `tabSalary Slip`  where `tabSalary Slip`.employee= %s """,emp.name,as_dict=True)
        print(list(ss.start_date))
        apf=frappe.db.sql("""SELECT MAX(start_date),name FROM `tabAnnual PF` where `tabAnnual PF`.name1= %s """,emp.name)
        date = datetime.datetime.strptime(str(ss[0][0]), "%Y-%m-%d").month
        if ss:
            spf=frappe.db.sql("""select amount as amount from `tabSalary Detail` where `tabSalary Detail`.parent= %s and `tabSalary Detail`.salary_component="Provident Fund" """,ss[0][1],as_dict=True)      
            # print(spf)
            if apf[0][1]:
                af=frappe.get_doc("Annual PF", apf[0][1])
                for a in af.monthly_pf:
                    # print(month[date])
                    # sd=[]
                    if a.month==month[date]:
                        sd=list(spf)
                        # print(apf[0][1])
                        print(sd)
                        for s in sd:
                            a.epf= s.amount
                        #     # print("hi")
                        #     # print(spf)
                        #     # print(a.month)
                        #     # print(month[date])
                        #     af.save(ignore_permissions=True)
                        #     frappe.db.commit()
                        #     print(af)
  