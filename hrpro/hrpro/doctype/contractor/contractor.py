# -*- coding: utf-8 -*-
# Copyright (c) 2020, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.data import today, add_days,get_last_day
from datetime import datetime

class Contractor(Document):
	pass


def wc_expiry_alert():
	contractors = frappe.get_all("Contractor")
	check_date = add_days(today(),7)
	wc_list = frappe.db.sql("""select `tabContractor`.name,`tabWC Insurance`.insurance_no,`tabWC Insurance`.isp,`tabWC Insurance`.to from `tabContractor`
	left join `tabWC Insurance` on `tabContractor`.name = `tabWC Insurance`.parent 
	where `tabWC Insurance`.to between %s and %s and `tabContractor`.status = "Active" """,(today(),check_date),as_dict=True)
	if wc_list:
		content = """Dear Sir,<br><br>Please find the WC Expiry Status till %s.<br><br>
		<table class='table table-bordered'>
		<th>S.No</th><th>Contractor Name</th><th>Insurance No</th><th>Insurance Service Provider</th><th>Expiry Date</th><th>Status</th>"""%(frappe.utils.format_date(check_date))
		i = 1
		for wc in wc_list:
			status = "Expires Soon"
			if wc.to < datetime.now().date():
				status = "Expired"
			if wc.to == datetime.now().date():
				status = "Expires Today"
			content += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"""%(i,wc.name,str(wc.insurance_no or ''),str(wc.isp or ''),frappe.utils.format_date(wc.to),status)
			i +=1
		message = content + "</table><br><br>Regards,<br>CLMS"
		frappe.sendmail(
					recipients=['anil.p@groupteampro.com','exehr@tnpetro.com'],
					subject='WC Expiry Alert',
					message="""%s"""%(message)
				)

def expired_wc():
	contractors = frappe.get_all("Contractor")
	wc_list = frappe.db.sql("""select `tabContractor`.name,`tabWC Insurance`.insurance_no,`tabWC Insurance`.isp,`tabWC Insurance`.to from `tabContractor`
	left join `tabWC Insurance` on `tabContractor`.name = `tabWC Insurance`.parent 
	where `tabWC Insurance`.to < %s and `tabContractor`.status = "Active" """,(today()),as_dict=True)
	if wc_list:
		content = """Dear Sir,<br><br>Please find the List WC Expired.<br><br>
		<table class='table table-bordered'>
		<th>S.No</th><th>Contractor Name</th><th>Insurance No</th><th>Insurance Service Provider</th><th>Expiry Date</th><th>Status</th>"""
		i = 1
		for wc in wc_list:
			content += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Expired</td></tr>"""%(i,wc.name,str(wc.insurance_no or ''),str(wc.isp or ''),frappe.utils.format_date(wc.to))
			i +=1
		message = content + "</table><br><br>Regards,<br>CLMS"
		frappe.sendmail(
					recipients=['anil.p@groupteampro.com','exehr@tnpetro.com'],
					subject='Expired WC List',
					message="""%s"""%(message)
				)

@frappe.whitelist()
def rc_expiry_alert():
	contractors = frappe.get_all("Contractor")
	check_date = get_last_day(today())
	rc_list = frappe.db.sql("""select `tabContractor`.name,`tabRC Child`.rc_number,`tabRC Child`.plant,`tabRC Child`.completion_of_work from `tabContractor`
	left join `tabRC Child` on `tabContractor`.name = `tabRC Child`.parent 
	where `tabRC Child`.completion_of_work between %s and %s and `tabContractor`.status = "Active" """,(today(),check_date),as_dict=True)
	if rc_list:
		content = """Dear Sir,<br><br>Please find the RC Expiry Status till %s.<br><br>
		<table class='table table-bordered'>
		<th>S.No</th><th>Contractor Name</th><th>Plant</th><th>RC Number</th><th>Expiry Date</th><th>Status</th>"""%(frappe.utils.format_date(check_date))
		i = 1
		for rc in rc_list:
			content += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Expires Soon</td></tr>"""%(i,rc.name,str(rc.plant or ''),str(rc.rc_number or ''),frappe.utils.format_date(rc.completion_of_work))
			i +=1
		message = content + "</table><br><br>Regards,<br>CLMS"
		frappe.sendmail(
					recipients=['anil.p@groupteampro.com','exehr@tnpetro.com'],
					subject='RC Expiry Alert',
					message="""%s"""%(message)
				)
				
@frappe.whitelist()
def no_rc_wc_alert():
	contractors = frappe.get_all("Contractor")
	check_date = get_last_day(today())
	rc_list = frappe.db.sql("""select `tabContractor`.name,`tabRC Child`.rc_number from `tabContractor`
	left join `tabRC Child` on `tabContractor`.name = `tabRC Child`.parent 
	where `tabRC Child`.rc_number is null and `tabContractor`.status = "Active" """,as_dict=True)
	if rc_list:
		rc_content = """Dear Sir,<br><br>Please find the List of Contractors without RC and WC.<br><br>List of Contractors without RC:<br>
		<table class='table table-bordered'>
		<th>S.No</th><th>Contractor Name</th>"""
		i = 1
		for rc in rc_list:
			rc_content += """<tr><td>%s</td><td>%s</td></tr>"""%(i,rc.name)
			i +=1
		rc_content = rc_content + "</table><br><br><br>"

	wc_list = frappe.db.sql("""select `tabContractor`.name,`tabWC Insurance`.isp from `tabContractor`
		left join `tabWC Insurance` on `tabContractor`.name = `tabWC Insurance`.parent 
		where `tabWC Insurance`.isp is null and `tabContractor`.status = "Active" """,as_dict=True)
	if wc_list:
		wc_content = """List of Contractors without WC:<br><br>
		<table class='table table-bordered'>
		<th>S.No</th><th>Contractor Name</th>"""
		i = 1
		for wc in wc_list:
			wc_content += """<tr><td>%s</td><td>%s</td></tr>"""%(i,wc.name)
			i +=1
		wc_content = wc_content + "</table>"
		
		message = rc_content + wc_content + "<br><br>Regards,<br>CLMS"
		frappe.sendmail(
					recipients=['exehr@tnpetro.com'],
					subject='No RC & WC Alert',
					message="""%s"""%(message)
				)

	# for contractor in contractors:
	# 	con = frappe.get_doc("Contractor",contractor)
	# 	for c in con.rc_child:
	# 		if  check_date == c.completion_of_work:
	# 			content = """Dear Sir,<br><br>RC - <b>%s</b> of contractor %s for TPL Plant <b>%s</b> is going to get expired in 15 days.<br><br>Regards,<br>TPL HR Department"""%(c.rc_number,contractor,c.plant)
	# 			frappe.sendmail(
	# 			recipients=['anil.p@groupteampro.com','exehr@tnpetro.com','subash.p@groupteampro.com'],
	# 			subject='RC Expiry Alert',
	# 			message="""%s"""%(content)
	# 		)
	# 	for c in con.wc_child:
	# 		if  check_date == c.to:
	# 			content = """Dear Sir,<br><br>Workmen's Compensation  <b>(%s)</b> for %s is going to get expired in 15 days.<br><br>Regards,<br>TPL HR Department"""%(c.insurance_no,contractor)
	# 			frappe.sendmail(
	# 			recipients=['anil.p@groupteampro.com','exehr@tnpetro.com','subash.p@groupteampro.com'],
	# 			subject='RC Expiry Alert',
	# 			message="""%s"""%(content)
	# 		)
	# 	for c in con.rc_child:
	# 		if  (datetime.today()).date() == c.completion_of_work:
	# 			content = """Dear Sir,<br><br>RC - <b>%s</b> for TPL Plant <b>%s</b> is expired.<br><br>Regards,<br>TPL HR Department"""%(c.rc_number,c.plant)
	# 			frappe.sendmail(
	# 			recipients=['anil.p@groupteampro.com','exehr@tnpetro.com'],
	# 			subject='RC Expiry Alert',
	# 			message="""%s"""%(content)
	# 		)
	# 	for c in con.wc_child:
	# 		if  (datetime.today()).date() == c.to:
	# 			content = """Dear Sir,<br><br>Workmen's Compensation  <b>(%s)</b> for TPL is expired.<br><br>Regards,<br>TPL HR Department"""%(c.insurance_no)
	# 			frappe.sendmail(
	# 			recipients=['anil.p@groupteampro.com','exehr@tnpetro.com'],
	# 			subject='RC Expiry Alert',
	# 			message="""%s"""%(content)
	# 		)



@frappe.whitelist()
def wc_expiring_tomorrow():
	check_date = add_days(today(),1)
	wc_list = frappe.db.sql("""select `tabContractor`.name,`tabWC Insurance`.insurance_no,`tabWC Insurance`.isp,`tabWC Insurance`.to from `tabContractor`
	left join `tabWC Insurance` on `tabContractor`.name = `tabWC Insurance`.parent 
	where `tabWC Insurance`.to = %s and `tabContractor`.status = "Active" """,(check_date),as_dict=True)
	if wc_list:
		content = """Dear Sir,<br><br>Please find the WC Expiring Tomorrow - %s.<br><br>
		<table class='table table-bordered'>
		<th>S.No</th><th>Contractor Name</th><th>Insurance No</th><th>Insurance Service Provider</th><th>Expiry Date</th><th>Status</th>"""%(frappe.utils.format_date(check_date))
		i = 1
		for wc in wc_list:
			content += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Expires Tomorrow</td></tr>"""%(i,wc.name,str(wc.insurance_no or ''),str(wc.isp or ''),frappe.utils.format_date(wc.to))
			i +=1
		message = content + "</table><br><br>Regards,<br>CLMS"
		frappe.sendmail(
					recipients=['anil.p@groupteampro.com','exehr@tnpetro.com'],
					subject='WC Expiring Tomorrow',
					message="""%s"""%(message)
				)