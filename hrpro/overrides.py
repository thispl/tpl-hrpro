import frappe
from erpnext.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
import mysql.connector

class CustomPayrollEntry(PayrollEntry):
    def get_filter_condition(self):
        self.check_mandatory()

        cond = ''
        for f in ['company', 'branch', 'department', 'designation', 'employment_type']:
            if self.get(f):
                cond += " and t1." + f + " = " + frappe.db.escape(self.get(f))
        frappe.errprint(cond)
        return cond

# class CustomSalarySlip(SalarySlip):
#     def on_update(self):
#         biometric_pin = frappe.get_value('Employee',self.employee,'biometric_pin')
#         if biometric_pin:
#             import mysql.connector
#             mydb = mysql.connector.connect(
#             host="192.9.200.171",
#             user="root",
#             password="Pa55w0rd@",
#             database="biotime"
#             )

#             mycursor = mydb.cursor()
#             if self.non_compliance:
#                 sql = "update personnel_employee set verify_mode=4,update_time=NOW(6) WHERE emp_code='%s'" % biometric_pin
#             else:
#                 sql = "update personnel_employee set verify_mode=0,update_time=NOW(6) WHERE emp_code='%s'" % biometric_pin
#             mycursor.execute(sql)

#             mydb.commit()

#             frappe.errprint(str(mycursor.rowcount) + " record(s) affected")

        

