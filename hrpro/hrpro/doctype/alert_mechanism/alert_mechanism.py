# -*- coding: utf-8 -*-
# Copyright (c) 2020, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import calendar
from frappe.model.document import Document
from frappe.utils import today
from datetime import datetime, timedelta, date

class AlertMechanism(Document):
	pass

@frappe.whitelist()
def alert_list():
	item_name = frappe.db.get_values('Alert List',{'parent': 'Alert Mechanism'}, '*')
	for i in item_name:
		now_date = frappe.utils.datetime.datetime.now().date()
		date = frappe.utils.datetime.datetime.now().strftime("%d")
		alert_on = i.alert_on.strftime("%d")
		due_date = i.date.strftime("%d")
		if i.period == "Yearly":
			if (now_date >= i.alert_on and now_date <= i.date):
				frappe.sendmail(
				recipients=["barathprathosh@groupteampro.com"],
				subject= i.alert_title,
				message= """<p>Dear Sir/Madam,</p>
				<h4>Info:</h4><p>Due Date of %s is ending soon, so Kindly work on it.
				</p><br> Regards <br>ERP Team"""
                % i.alert_title)
		elif i.period == "Monthly":
			if (date >= alert_on and date <= due_date):
				frappe.sendmail(
				recipients=["barathprathosh@groupteampro.com"],
				subject= i.alert_title,
				message= """<p>Dear Sir/Madam,</p>
				<h4>Info:</h4><p>Due Date of %s is ending soon, so Kindly work on it.
				</p><br> Regards <br>ERP Team"""
                % i.alert_title)
		elif i.period == "Weekly":
			days = frappe.utils.datetime.datetime.now().strftime("%A")
			alert_on = i.alert_on.strftime("%A")
			due_date = i.date.strftime("%A")
			if (days >= alert_on and days <= due_date):
				frappe.sendmail(
				recipients=["barathprathosh@groupteampro.com"],
				subject= i.alert_title,
				message= """<p>Dear Sir/Madam,</p>
				<h4>Info:</h4><p>Due Date of %s is ending soon, so Kindly work on it.
				</p><br> Regards <br>ERP Team"""
                % i.alert_title)
		else:
			frappe.sendmail(
				recipients=["barathprathosh@groupteampro.com"],
				subject= i.alert_title,
				message= """<p>Dear Sir/Madam,</p>
				<h4>Info:</h4><p>Due Date of %s is ending soon, so Kindly work on it.
				</p><br> Regards <br>ERP Team"""
                % i.alert_title)
			