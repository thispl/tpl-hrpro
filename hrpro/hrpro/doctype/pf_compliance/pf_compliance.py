# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.csvutils import read_csv_content

class PFCompliance(Document):
    pass

@frappe.whitelist()
def validate_pf(name,filename,start_date):
    from frappe.utils.file_manager import get_file
    _file = frappe.get_doc("File", {"file_url": filename})
    filepath = get_file(filename)
    pps = read_csv_content(filepath[1])
    ss_list = []
    emp_list = []
    for pp in pps:
        emp = frappe.db.exists("Employee",{"uan":pp[0]})
        frappe.errprint(emp)
        if emp:
            ss = frappe.db.get_value("Salary Slip",{"employee":emp,"start_date":start_date})
            pf = frappe.db.get_value("Salary Detail", {'abbr': 'PF', 'parent':ss }, ['amount'])
            rpf = pf - 5
            frappe.errprint(pf)
            frappe.errprint(rpf)
            if frappe.db.get_value("Salary Slip",ss,["pf_paid"]) == 0:
                frappe.db.set_value("Salary Slip",ss,"pf_paid",pp[6])
                if float(pp[6]) < rpf:
                    frappe.db.set_value("Salary Slip",ss,"pf_non_compliance",1)
            elif frappe.db.get_value("Salary Slip",ss,["pf_paid"]) > 0:
                if frappe.db.get_value("Salary Slip",ss,["pf_non_compliance"]):
                    apf = frappe.db.get_value("Salary Slip",ss,["pf_paid"])+float(pp[6])
                    if apf < rpf:
                        frappe.db.set_value("Salary Slip",ss,"pf_non_compliance",1)
                        frappe.db.set_value("Salary Slip",ss,"pf_paid",apf)
                    else:
                        frappe.db.set_value("Salary Slip",ss,"pf_non_compliance",0)
                        frappe.db.set_value("Salary Slip",ss,"pf_paid",apf)

                    
            # rv = int(pp[3])
        #     # if pp[0] != "UAN":
        #     frappe.errprint(pp[0])
        #     # frappe.errprint(rv)
        #     if pf < int(pp[3]):
        #         ss_list.append(ss)
        #         emp_list.append(emp)
    # return ss_list,emp_list

        # cl = frappe.get_doc("Candidate",{'name':pp[0]})
        # cl.pending_for = 'IDB'
        # cl.db_update()
        # frappe.db.commit()
