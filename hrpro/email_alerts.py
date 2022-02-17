import frappe

@frappe.whitelist()
def pf_notification():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for PF",
		message= "Content of the email")

@frappe.whitelist()
def esi_notification():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for ESI",
		message= "Content of the email")

@frappe.whitelist()
def esi_half_year():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for ESI Half Year Return(April to September)",
		message= "Content of the email")

@frappe.whitelist()
def esi_half_year_return():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for ESI Half Year Return(October to March)",
		message= "Content of the email")

@frappe.whitelist()
def pt_notification():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for PT",
		message= "Content of the email")

@frappe.whitelist()
def gst_notification():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for GST",
		message= "Content of the email")

@frappe.whitelist()
def tds_notification():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for TDS",
		message= "Content of the email")

@frappe.whitelist()
def tds_march_alone():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for TDS March Alone",
		message= "Content of the email")

@frappe.whitelist()
def it_filling():
    frappe.sendmail(
        recipients=["barathprathosh@groupteampro.com"],
		subject="Statutory Filling Due Date for IT Filling",
		message= "Content of the email")