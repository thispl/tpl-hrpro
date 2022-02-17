# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class ContractorEmployee(Document):
    def on_submit(self):
        if self.biometric_pin:
            sc =  frappe.get_value("Contractor",self.contractor_id,["short_code"])
            emps = frappe.db.sql("""select name from `tabEmployee` where contractor_id = %s order by creation""",self.contractor_id,as_dict=True)
            # frappe.errprint(emps)
            # if doc.code:
            #     count = doc.code
            # else:
            try :
                emp = emps[-1].name
                c = emp.split("-")
                count = int(c[-1])+1
            except:
                count = 1
            doc = frappe.new_doc("Employee")
            doc.salutation = self.salutation
            doc.first_name = self.first_name
            doc.middle_name = self.last_name
            doc.biometric_pin = self.biometric_pin
            doc.employment_type = self.employment_type
            doc.gender = self.gender
            doc.employee_number = sc+'-'+str(count)
            doc.date_of_joining = self.date_of_joining
            doc.date_of_birth = self.date_of_birth
            doc.marital_status = self.marital_status
            doc.blood_group = self.blood_group
            doc.cell_number = self.cell_number
            doc.personal_email = self.personal_email
            doc.contractor_id = self.contractor_id
            doc.flat = self.flat
            doc.flat_name = self.flat_name
            doc.street_road = self.street_road
            doc.area_locality = self.area_locality
            doc.village_town_city = self.village_town_city
            doc.district = self.district
            doc.state = self.state
            doc.pin_code = self.pin_code
            doc.pf_number = self.pf_number
            doc.esi_ip_no = self.esi_ip_no
            doc.uan = self.uan
            doc.aadhar_number = self.aadhar_number
            doc.flags.ignore_mandatory = True
            doc.save(ignore_permissions=True)
            frappe.db.commit()
        else:
            frappe.throw(_("Please Enter Biometric PIN"))
