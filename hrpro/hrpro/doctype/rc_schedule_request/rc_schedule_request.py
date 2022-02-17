# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe import _
from frappe.utils import get_link_to_form

class RCScheduleRequest(Document):
    def validate(self):
        self.check_availability()

    def check_availability(self):
        con = frappe.get_doc('Contractor',self.contractor)
        rc_reg = 0
        rc_av = 0
        wc_reg = 0
        wc_av = 0
        rc_child = frappe.get_value('RC Child',{'parent':self.contractor,'plant':self.plant},['completion_of_work','max'])
        if rc_child:
            if (datetime.strptime(str(self.end_date), '%Y-%m-%d')).date() < (rc_child[0]):
                rc_reg = rc_child[1]
            rc_utz = frappe.db.sql("""select sum(manpower_count) as count from `tabRC Schedule Request` where start_date between %s and %s and contractor = %s and plant = %s """,(self.start_date,self.end_date,self.contractor,self.plant),as_dict=True)
            if rc_utz[0].count:
                rc_av = rc_reg - int(rc_utz[0].count)
            else:
                rc_av = rc_reg
        wc_child = frappe.get_all('WC Insurance',{'parent':self.contractor},['to','persons_covered'])
        if wc_child:
            for wc in wc_child:
                if (datetime.strptime(str(self.end_date), '%Y-%m-%d')).date() < (wc.to):
                    wc_reg = wc_reg + int(wc.persons_covered)
            wc_utz = frappe.db.sql("""select sum(manpower_count) as count from `tabRC Schedule Request` where start_date between %s and %s and contractor = %s """,(self.start_date,self.end_date,self.contractor),as_dict=True)
            if wc_utz[0].count:
                wc_av = wc_reg - int(wc_utz[0].count)
            else:
                wc_av = wc_reg
        return rc_reg,rc_av,wc_reg,wc_av

    def get_hod_rc(self):
        if frappe.session.user != "Administrator":
            depts = frappe.db.sql("""select for_value from `tabUser Permission` where user = %s and allow = "Department" """,(frappe.session.user),as_dict=True)
            plants = frappe.db.sql("""select for_value from `tabUser Permission` where user = %s and allow = "Plant" """,(frappe.session.user),as_dict=True)
            dept_list = []
            plant_list = []
            for d in depts:
                dept_list.append(d.for_value)
            for p in plants:
                plant_list.append(p.for_value)
            if len(dept_list) > 0 and len(plant_list) > 0:
                return frappe.db.sql("""select * from `tabRC Schedule Request` where start_date between %s and %s and contractor = %s and plant in %s and department in %s and name !=%s """,(self.start_date,self.end_date,self.contractor,plant_list,dept_list,self.name),as_dict=True)
            if len(dept_list) > 0 and len(plant_list) == 0:
                return frappe.db.sql("""select * from `tabRC Schedule Request` where start_date between %s and %s and contractor = %s and department in %s and name !=%s """,(self.start_date,self.end_date,self.contractor,dept_list,self.name),as_dict=True)
    
    def get_gm_rc(self):
        if frappe.session.user != "Administrator":
            dept_list = ["Civil - TPL","Electrical - TPL","MECHANICAL - TPL","Instrumentation - TPL"]
            return frappe.db.sql("""select * from `tabRC Schedule Request` where start_date between %s and %s and contractor = %s and department in %s and name !=%s """,(self.start_date,self.end_date,self.contractor,dept_list,self.name),as_dict=True)
    
    def get_vp_rc(self):
        if frappe.session.user != "Administrator":
            return frappe.db.sql("""select * from `tabRC Schedule Request` where start_date between %s and %s and contractor = %s and name !=%s """,(self.start_date,self.end_date,self.contractor,self.name),as_dict=True)

    def validate(self):
        con = frappe.get_doc('Contractor',self.contractor)
        rc_reg = 0
        rc_av = 0
        wc_reg = 0
        wc_av = 0
        rc_child = frappe.get_value('RC Child',{'parent':self.contractor,'plant':self.plant},['completion_of_work','max'])
        if rc_child:
            if (datetime.strptime(str(self.end_date), '%Y-%m-%d')).date() < (rc_child[0]):
                rc_reg = rc_child[1]
            rc_utz = frappe.db.sql("""select sum(manpower_count) as count from `tabRC Schedule Request` where start_date between %s and %s and contractor = %s and plant = %s """,(self.start_date,self.end_date,self.contractor,self.plant),as_dict=True)
            if rc_utz[0].count:
                rc_av = rc_reg - int(rc_utz[0].count)
            else:
                rc_av = rc_reg
        wc_child = frappe.get_all('WC Insurance',{'parent':self.contractor},['to','persons_covered'])
        if wc_child:
            for wc in wc_child:
                if (datetime.strptime(str(self.end_date), '%Y-%m-%d')).date() < (wc.to):
                    wc_reg = wc_reg + int(wc.persons_covered)
            wc_utz = frappe.db.sql("""select sum(manpower_count) as count from `tabRC Schedule Request` where start_date between %s and %s and contractor = %s """,(self.start_date,self.end_date,self.contractor),as_dict=True)
            if wc_utz[0].count:
                wc_av = wc_reg - int(wc_utz[0].count)
            else:
                wc_av = wc_reg
        if rc_av < int(self.manpower_count or 0):
            frappe.throw(_("Requested Count cannot be greater than RC Available Count. Kindly raise unregistered request seperately"))
        if wc_av < int(self.manpower_count or 0):
            frappe.throw(_("Requested Count cannot be greater than WC Available Count. Kindly raise unregistered request seperately"))

    def send_mail(self,status):
        mail = ""
        if status == "Pending for HOD":
            mail = frappe.get_value("Approval Level",{"department":self.department,"plant":self.plant},["hod"])
        elif status == "Pending for GM":
            mail = frappe.get_value("Approval Level",{"department":self.department,"plant":self.plant},["gm"])
        elif status == "Pending for VP":
            mail = frappe.get_value("Approval Level",{"department":self.department,"plant":self.plant},["vp"])
        elif status == "Approved":
            mail = self.owner
        content = """Dear Sir,<br><br>
        RC Schedule Request from contractor <b>%s</b> is waiting for your approval.<br><br>
        Please click on %s to approve the request.<br><br>Regards,<br><br>CLMS"""%(self.contractor,get_link_to_form('RC Schedule Request', self.name))
        frappe.sendmail(
            recipients=['anil.p@groupteampro.com'],
            subject='RC Schedule Request - '+self.contractor,
            message="""%s"""%(content)
        )