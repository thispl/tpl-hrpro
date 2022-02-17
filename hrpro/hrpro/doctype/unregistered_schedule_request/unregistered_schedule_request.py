# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UnregisteredScheduleRequest(Document):
	pass

@frappe.whitelist()
def get_history(start_date,end_date,plant,department):
    plants = frappe.get_list("User Permission",{"user":frappe.session.user,"allow":"Plant"},["for_value"])
    plant = []
    for p in plants:
        plant.append(p.for_value)
    if len(plant) > 0:
        return frappe.db.sql("""select manpower_count as count,contractor, workflow_state,plant,name from `tabRC Schedule Request` where start_date between %s and %s and plant in %s and department = %s""",(start_date,end_date,plant,department),as_dict=True)
    else:
        return frappe.db.sql("""select manpower_count as count,contractor, workflow_state,plant,name from `tabRC Schedule Request` where start_date between %s and %s and department = %s""",(start_date,end_date,department),as_dict=True)