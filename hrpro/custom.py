import frappe,os
import random
from datetime import datetime
from frappe.utils.data import today, add_days, add_years
from dateutil.relativedelta import relativedelta
from datetime import timedelta, time,date
from frappe.utils import time_diff_in_hours, formatdate, get_first_day,get_last_day, nowdate, now_datetime

# def submit_user():
#     emp = frappe.get_all("Employee",{'docstatus':1})
#     print(emp)
    # for e in emp:
        # doc = frappe.get_doc("Employee",e.name)
        # print(doc.biometric_pin)
        # doc.cancel()
            # frappe.db.commit()

@frappe.whitelist()
def block_other_modules(doc,method):
    if doc.role_profile_name == 'Contractor':
        block_modules = frappe.get_list('Block Module',{'parent':'anuenterprises666@gmail.com'},['module'])
        blocked_modules = []
        bms_dict = frappe.get_all('Block Module',{'parent':doc.name},['module'])

        for bm_dict in bms_dict:
            blocked_modules.append(bm_dict.module)
        if not blocked_modules:
            for block_module in block_modules[:5]:
                bm = frappe.new_doc('Block Module')
                bm.module = block_module.module
                bm.parent = doc.name
                bm.parenttype = 'user'
                bm.parentfield = 'block_modules'
                bm.save(ignore_permissions=True)


@frappe.whitelist()
def create_employee(doc,method):
    # doc = frappe.get_doc("Biometric User",doc)
    if not doc.skip:
        if not frappe.db.exists("Employee",{"biometric_pin":doc.biometric_pin}):
            if doc.contractor:
                sc =  frappe.get_value("Contractor",doc.contractor,["short_code"])
                emps = frappe.db.sql("""select name from `tabEmployee` where contractor_id = %s order by creation""",doc.contractor,as_dict=True)
                frappe.errprint(emps)
                # if doc.code:
                # count = 54
                try :
                    emp = emps[-1].name
                    c = emp.split("-")
                    count = int(c[-1])+1
                except:
                    count = 1
                try:
                    emp = frappe.new_doc("Employee")
                    emp.first_name = doc.first_name
                    emp.last_name = doc.last_name
                    emp.biometric_pin = doc.biometric_pin
                    emp.employee_number = sc+'-'+str(count)
                    emp.employment_type = doc.employment_type
                    emp.contractor_id = doc.contractor
                    emp.uan = doc.uan_no
                    emp.esi_ip_no = doc.esi_ip_no
                    emp.flags.ignore_mandatory = True
                    emp.save(ignore_permissions = True)
                    frappe.db.commit()
                except:
                    emp = frappe.new_doc("Employee")
                    emp.first_name = doc.first_name
                    emp.last_name = doc.last_name
                    emp.biometric_pin = doc.biometric_pin
                    emp.employee_number = sc+'-'+ str(frappe.db.count('Employee',{'contractor_id':doc.contractor})+1)
                    emp.employment_type = doc.employment_type
                    emp.contractor_id = doc.contractor
                    emp.uan = doc.uan_no
                    emp.esi_ip_no = doc.esi_ip_no
                    emp.flags.ignore_mandatory = True
                    emp.save(ignore_permissions = True)
                    frappe.db.commit()

@frappe.whitelist()
def assign_salary_structure(employee,date,structure):
    if frappe.db.exists("Salary Structure Assignment",{"employee":employee,'docstatus':1}):
        if not frappe.db.exists("Salary Structure Assignment",{"employee":employee,"salary_structure":structure,'docstatus':1}):
            doc = frappe.new_doc("Salary Structure Assignment")
            doc.employee = employee
            doc.salary_structure = structure
            doc.from_date = today()
            doc.save(ignore_permissions=True)
            doc.submit()
            frappe.db.commit()
    else:
        doc = frappe.new_doc("Salary Structure Assignment")
        doc.employee = employee
        doc.salary_structure = structure
        doc.from_date = date
        doc.save(ignore_permissions=True)
        doc.submit()
        frappe.db.commit()

@frappe.whitelist()
def fetch_salary_components(employee,structure):
    b = 0
    da = 0
    hra = 0
    sa = 0
    if structure == "Daily Wage":
        b = frappe.db.get_value("Salary Detail", {'abbr': 'B', 'parent':structure }, ['amount'])
        da = frappe.db.get_value("Salary Detail", {'abbr': 'DA', 'parent':structure }, ['amount'])
        hra = frappe.db.get_value("Salary Detail", {'abbr': 'HRA', 'parent':structure }, ['amount'])
        sa = frappe.db.get_value("Salary Detail", {'abbr': 'SA', 'parent':structure }, ['amount'])
        return b,da,hra,sa
    else:
        return b,da,hra,sa


@frappe.whitelist()
def calculate_hours(in_t,out,shift,contractor):
    time_list = []
    s_list = ["C Shift","Night Shift"]
    in_time = datetime.strptime(in_t, '%H:%M:%S')
    out_time = datetime.strptime(out, '%H:%M:%S')
    if contractor != "i3 Security":
        if shift not in ["C Shift","Night Shift"]:
            total_twh = datetime.strptime(str(out_time - in_time), '%H:%M:%S')
        else:
            o_time = (add_days(out_time,1))
            total_twh = datetime.strptime(str(o_time - in_time), '%H:%M:%S')
        max_twh = datetime.strptime('08:00', '%H:%M')
        extra_hrs = time(0,0,0)
        ot_hrs  = time(0,0,0)
        if total_twh >= max_twh:
            extra_hrs = total_twh - max_twh
            if extra_hrs >= timedelta(minutes=30):
                extra_hr = datetime.strptime(str(extra_hrs), "%H:%M:%S")
                if extra_hr.minute <= 30:
                    ot_hrs = time(extra_hr.hour,0,0)
                elif extra_hr.minute >= 31:
                    ot_hrs = time(extra_hr.hour + 1,0,0)
        return {"twh":str(total_twh.time()),"ext":str(extra_hrs),"ot":str(ot_hrs)}
    if contractor == "i3 Security":
        if shift != "Night Shift":
            total_twh = datetime.strptime(str(out_time - in_time), '%H:%M:%S')
        else:
            o_time = (add_days(out_time,1))
            total_twh = datetime.strptime(str(o_time - in_time), '%H:%M:%S')
        max_twh = datetime.strptime('12:00', '%H:%M')
        extra_hrs = time(0,0,0)
        ot_hrs  = time(0,0,0)
        if total_twh >= max_twh:
            extra_hrs = total_twh - max_twh
            if extra_hrs >= timedelta(minutes=30):
                extra_hr = datetime.strptime(str(extra_hrs), "%H:%M:%S")
                if extra_hr.minute <= 30:
                    ot_hrs = time(extra_hr.hour,0,0)
                elif extra_hr.minute >= 31:
                    ot_hrs = time(extra_hr.hour + 1,0,0)
        return {"twh":str(total_twh.time()),"ext":str(extra_hrs),"ot":str(ot_hrs)}


# @frappe.whitelist()
# def generate_employee_number(doc,method):
#     frappe.errprint(doc.)
#     # emp.biometric_pin = doc.biometric_pin
#     # emp.flags.ignore_mandatory = True
#     # emp.save(ignore_permissions = True)
#     # frappe.db.commit()

@frappe.whitelist()
def blocking_start_date():
    emps = frappe.get_list("Employee",{'new_employee':1})
    for emp in emps:
        j_date = frappe.db.get_value("Employee",emp.name,["date_of_joining"])
        month_end = get_last_day(j_date)
        b_date = add_days(month_end,20)
        if datetime.now().date() > b_date:
            frappe.db.set_value("Employee",emp,"new_employee",0)

@frappe.whitelist()
def new_employee(doj,name):
    month_end = get_last_day(doj)
    b_date = add_days(month_end,20)
    if datetime.now().date() < b_date:
        return doj

@frappe.whitelist()
def new_contract_employee():
    emp_list = frappe.db.sql("""select count(*) as count,contractor_id,plant from `tabContractor Employee` where date(creation) = %s group by contractor_id,plant """,today(),as_dict=True)
    if emp_list:    
        table = """
        Dear Sir<br><br>
        Please find the summary of New Contract Employees requested.<br><br>
        <table class='table table-bordered'>
            <tr>
            <td>S.No</td><td>Contractor Name</td><td>Plant</td><td>Nos of Employees</td>
            </tr>
            """
        i = 1
        for emp in emp_list:
            table += """
            <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
            """%(i,emp.contractor_id,emp.plant,emp.count)
            i+=1
        content = table + "</table><br><br>Regards,<br><br>CLMS"
        frappe.sendmail(
            recipients=['anil.p@groupteampro.com','exehr@groupteampro.com'],
            subject='New Contract Employee Request - '+formatdate(today()),
            message="""%s"""%(content)
        )

@frappe.whitelist()
def block_employee():
    emp_list = frappe.get_all("Employee",{"employment_type":"Subcontract","status":"Active"})
    for emp in emp_list:
        att = frappe.db.count("Attendance",{"employee":emp.name,"status":"Present","docstatus":1})
        if att > 60:
            if not frappe.db.get_value("Employee",emp.name,["block_employee"]):
                frappe.db.set_value("Employee",emp.name,"block_employee",1)

@frappe.whitelist()
def get_retirement_date(dob):
    return add_years(dob,58)

@frappe.whitelist()
def generate_qr(employee):
    can = frappe.get_doc("Employee",employee)
    import qrcode
    import qrcode.image.pil
    from PIL import Image



    # Create qr code instance
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 4,
        border = 4,
    )
   
    # The data that you want to store
    data = """Employee Name:%s\nImage:%s\nCategory:%s\nUAN:%s\nESI IP No:%s\nSubContractor ID:%s\nSubContractor Name:%s\nGender:%s\nDate of Birth:%s\nBlood Group:%s"""%(can.employee_name,can.image,can.category,can.uan,can.esi_ip_no,can.subcontractor_id,can.
subcontractor_name,can.gender,can.date_of_birth,can.blood_group)
    # Add data
    qr.add_data(data)
    qr.make(fit=True)
    # Create an image from the QR Code instance
    img = qr.make_image()
    path = frappe.get_site_path('public', 'files')
    qr_name = can.employee_name + '_qr.png'
    # basewidth = 64
    # wpercent = (basewidth / float(img.size[0]))
    # hsize = int((float(img.size[1]) * float(wpercent)))
    # img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(path +"/%s"% qr_name)
    frappe.errprint(can.name)
    frappe.db.set_value("Employee",can.name,"qr_code","/files/%s"%qr_name)
    return qr_name

@frappe.whitelist()
def check_gross_against_ss(doc,method):
    from erpnext.payroll.doctype.salary_structure.salary_structure import make_salary_slip
    ss = make_salary_slip(doc.salary_structure,employee = doc.employee)
    frappe.errprint(ss.gross_pay)
    frappe.errprint(doc.base)

@frappe.whitelist()
def employment_age():
    employee = frappe.get_all("Employee" ,{"status":"Active"}, ['name','date_of_joining'])
    for emp in employee:
        if emp.date_of_joining:
            now_date = frappe.utils.datetime.datetime.now().date()
            age = now_date.year - emp.date_of_joining.year - ((now_date.month, now_date.day) < (emp.date_of_joining.month, emp.date_of_joining.day))
            if age:
                frappe.db.set_value("Employee",emp.name, "age", age)


@frappe.whitelist()
def mark_monthly():
    start_date = get_first_day(nowdate())
    end_date = get_last_day(nowdate())
    checkins = frappe.db.sql(
        """select * from `tabEmployee Checkin` where attendance_marked = 0 and log_type = "IN" and log_date between '%s' and '%s'""" %(start_date,end_date), as_dict=1)
    # checkins = frappe.db.sql(
    #     """select * from `tabEmployee Checkin` where attendance_marked = 0 and log_type = "IN" and log_date = %s """,(today()), as_dict=1)
    if checkins:
        for c in checkins:
            att = mark_attendance_from_checkin(c.name,c.employee,c.device_area,c.log_date,c.biometric_pin,c.log_type,c.time,c.contractor)
            if att:
                frappe.db.set_value("Employee Checkin",
                                    c.name, "attendance_marked", "1")
        return "ok"

@frappe.whitelist()
def mark_in():
    # checkins = frappe.db.sql(
    #     """select * from `tabEmployee Checkin` where attendance_marked = 0 and log_type = "IN" and log_date between '2021-11-01' and '2021-12-10' """, as_dict=1)
    checkins = frappe.db.sql(
        """select * from `tabEmployee Checkin` where attendance_marked = 0 and log_type = "IN" and log_date = %s """,(today()), as_dict=1)
    if checkins:
        for c in checkins:
            att = mark_attendance_from_checkin(c.name,c.employee,c.device_area,c.log_date,c.biometric_pin,c.log_type,c.time,c.contractor)
            if att:
                frappe.db.set_value("Employee Checkin",
                                    c.name, "attendance_marked", "1")
        return "ok"

def mark_attendance_from_checkin(checkin,employee,device_area,log_date,biometric_pin,log_type,time,contractor):
    a_min_time = datetime.strptime('06:00', '%H:%M')
    a_max_time = datetime.strptime('07:00', '%H:%M')
    b_min_time = datetime.strptime('14:00', '%H:%M')
    b_max_time = datetime.strptime('15:00', '%H:%M')
    c_min_time = datetime.strptime('21:30', '%H:%M')
    c_max_time = datetime.strptime('22:30', '%H:%M')
    g_min_time = datetime.strptime('07:45', '%H:%M')
    g_max_time = datetime.strptime('08:45', '%H:%M')
    nyt_min_time = datetime.strptime('18:00', '%H:%M')
    nyt_max_time = datetime.strptime('19:00', '%H:%M')
    att_time = time.time()
    a_min = a_min_time.time()
    a_max = a_max_time.time()
    b_min = b_min_time.time()
    b_max = b_max_time.time()
    c_min = c_min_time.time()
    c_max = c_max_time.time()
    g_min = g_min_time.time()
    g_max = g_max_time.time()
    nyt_min = nyt_min_time.time()
    nyt_max = nyt_max_time.time()
    is_active = frappe.db.get_value("Employee", {
        "biometric_pin": biometric_pin, "status": "Active"})
    # is_active = frappe.db.get_value("Employee", {"status": "Active"})
    if is_active:
        emp = frappe.get_doc("Employee", employee)
        if device_area:
            if device_area == "HCD IN":
                plant = "Heavy Chemicals Division"
            elif device_area == "LAB IN":
                plant = "Linear Alkyl Benzene"
            elif device_area == "PO IN":
                plant = "Propylene Oxide Division"
        if contractor !="i3 Security":
            if not frappe.db.exists("Attendance",{"employee":employee,"attendance_date":log_date}):
                status = "Present"
                if att_time >= a_min and att_time <= a_max:
                    shift = "A Shift"
                elif att_time >= b_min and att_time <= b_max:
                    shift = "B Shift"
                elif att_time >= c_min and att_time <= c_max:
                    shift = "C Shift"
                elif att_time >= g_min and att_time <= g_max:
                    shift = "General Shift"
                else:
                    shift = ""
                if frappe.db.get_value('Employee',employee,'date_of_joining'):
                    if frappe.db.get_value('Employee',employee,'date_of_joining') <= log_date:
                        attendance = frappe.new_doc("Attendance")
                        attendance.update({
                            "employee": employee,
                            "status": status,
                            "attendance_date":log_date,
                            "plant":plant,
                            "in": att_time,
                            "out":"",
                            "total_working_hours":"",
                            "extra_hours":"",
                            "approved_ot_hours":"",
                            "shift": shift
                        })
                        attendance.save(ignore_permissions=True)
                        frappe.db.set_value("Employee Checkin",checkin,"attendance",attendance.name)
                        frappe.db.commit()
                        return "ok"
                else:
                    attendance = frappe.new_doc("Attendance")
                    attendance.update({
                        "employee": employee,
                        "status": status,
                        "attendance_date":log_date,
                        "plant":plant,
                        "in": att_time,
                        "out":"",
                        "total_working_hours":"",
                        "extra_hours":"",
                        "approved_ot_hours":"",
                        "shift": shift
                    })
                    attendance.save(ignore_permissions=True)
                    frappe.db.set_value("Employee Checkin",checkin,"attendance",attendance.name)
                    frappe.db.commit()
                    return "ok"
        elif contractor == "i3 Security":
            if not frappe.db.exists("Attendance",{"employee":employee,"attendance_date":log_date}):
                status = "Present"
                if att_time >= a_min and att_time <= a_max:
                    shift = "Day Shift"
                elif att_time >= nyt_min and att_time <= nyt_max:
                    shift = "Night Shift"
                else:
                    shift = ""
                if frappe.db.get_value('Employee',employee,'date_of_joining'):
                    if frappe.db.get_value('Employee',employee,'date_of_joining') <= log_date:
                        attendance = frappe.new_doc("Attendance")
                        attendance.update({
                            "employee": employee,
                            "status": status,
                            "attendance_date":log_date,
                            "plant":plant,
                            "in": att_time,
                            "out":"",
                            "total_working_hours":"",
                            "extra_hours":"",
                            "approved_ot_hours":"",
                            "shift": shift
                        })
                        attendance.save(ignore_permissions=True)
                        frappe.db.set_value("Employee Checkin",checkin,"attendance",attendance.name)
                        frappe.db.commit()
                        return "ok"
                else:
                    attendance = frappe.new_doc("Attendance")
                    attendance.update({
                        "employee": employee,
                        "status": status,
                        "attendance_date":log_date,
                        "plant":plant,
                        "in": att_time,
                        "out":"",
                        "total_working_hours":"",
                        "extra_hours":"",
                        "approved_ot_hours":"",
                        "shift": shift
                    })
                    attendance.save(ignore_permissions=True)
                    frappe.db.set_value("Employee Checkin",checkin,"attendance",attendance.name)
                    frappe.db.commit()
                    return "ok"    


def mark_ab_out():
    # att_list = frappe.db.sql(""" select name, employee,attendance_date,shift,tabAttendance.in,contractor from `tabAttendance` where  docstatus = 0 and attendance_date between '2021-11-01' and  '2021-12-10'""",as_dict=True)
    att_list = frappe.db.sql(""" select name, employee,attendance_date,tabAttendance.in, shift,contractor from `tabAttendance` where  docstatus = 0 and attendance_date = %s """,(today()),as_dict=True)
    c_max = datetime.strptime('07:00', '%H:%M')
    c_max_out = c_max.time()
    s_list = ["C Shift","Night Shift"]
    for att in att_list:
        if att.shift not in s_list:
            # check = frappe.db.sql("""select name,time from `tabEmployee Checkin` where log_date = %s and employee = %s and attendance_marked = 0 and log_type='OUT' ORDER BY time """,(att.attendance_date,att.employee),as_dict=True)
            check = frappe.db.sql("""select name,time from `tabEmployee Checkin` where log_date = %s and employee = %s and log_type='OUT' ORDER BY time """,(att.attendance_date,att.employee),as_dict=True)
            doc = frappe.get_doc("Attendance",att.name)
            if len(check) > 0:
                approved_ot_hours = time(0,0,0)
                extra_hours = time(0,0,0)
                doc.out = (check[-1].time).time()
                # if len(check) > 4:
                    # print(check[0].time,check[-1].time)
                    # check_in = frappe.db.sql("""select name,time from `tabEmployee Checkin` where log_date = %s and employee = %s and log_type='IN' and time between %s and %s """,(att.attendance_date,att.employee,check[0].time,check[-1].time),as_dict=True)
                    # print(check_in)
                total_wh = ((check[-1].time) - att["in"]).time()
                doc.total_working_hours = total_wh
                # if time(8,0,0) > total_wh > time(4,0,0):
                #     status = "Half Day"
                # elif time(8,0,0) < total_wh:
                #     status = "Present"
                # else:
                #     status = "Absent"
                if att.contractor != "i3 Security":
                    max_wh = time(8,0,0)
                elif att.contractor == "i3 Security":
                    max_wh = time(12,0,0)
                doc.status = 'Present'
                if total_wh > max_wh:
                    datetime1 = datetime.combine(date(1,1,1), total_wh)
                    datetime2 = datetime.combine(date(1,1,1), max_wh)
                    extra_hours = datetime1 - datetime2
                    doc.extra_hours = extra_hours
                    if extra_hours >= timedelta(minutes=30):
                        extra_hr = datetime.strptime(str(extra_hours), "%H:%M:%S")
                        if extra_hr.minute <= 30:
                            approved_ot_hours = time(extra_hr.hour,0,0)
                        elif extra_hr.minute >= 31:
                            approved_ot_hours = time(extra_hr.hour + 1,0,0)
                    doc.approved_ot_hours = approved_ot_hours
                    doc.save()
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",check[-1].name,"attendance_marked",1)
                    frappe.db.set_value("Employee Checkin",check[-1].name,"attendance",doc.name)
                doc.save()
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",check[-1].name,"attendance_marked",1)
                frappe.db.set_value("Employee Checkin",check[-1].name,"attendance",doc.name)

        
def mark_c_out():
    yesterday = add_days(today(),-1)
    # att_list = frappe.db.sql(""" select name, employee,attendance_date,shift,tabAttendance.in,contractor from `tabAttendance` where  docstatus = 0 and attendance_date between '2021-11-01' and  '2021-12-10'""",as_dict=True)
    # yesterday = "2021-04-13"
    att_list = frappe.db.sql(""" select name, employee,attendance_date,shift,tabAttendance.in from `tabAttendance` where  docstatus = 0 and attendance_date = %s """,(yesterday),as_dict=True)
    s_list = ["C Shift","Night Shift"]
    for att in att_list:
        if att.shift in s_list:
            # check = frappe.db.sql("select name,time from `tabEmployee Checkin` where log_date = '2021-02-14' and employee = %s and log_type = 'OUT' ORDER BY time ",(att.employee),as_dict=True)
            check = frappe.db.sql("select name,time from `tabEmployee Checkin` where log_date = %s and employee = %s and log_type = 'OUT' ORDER BY time ",(today(),att.employee),as_dict=True)
            doc = frappe.get_doc("Attendance",att.name)
            if len(check) > 0:
                approved_ot_hours = time(0,0,0)
                extra_hours = time(0,0,0)
                doc.out = (check[-1].time).time()
                total_wh = ((check[-1].time) - att["in"]).time()
                doc.total_working_hours = total_wh
                # if time(8,0,0) > total_wh > time(4,0,0):
                #     status = "Half Day"
                # elif time(8,0,0) < total_wh:
                #     status = "Present"
                # else:
                #     status = "Absent"
                doc.status = 'Present'
                if att.contractor != "i3 Security":
                    max_wh = time(8,0,0)
                elif att.contractor == "i3 Security":
                    max_wh = time(12,0,0)
                if total_wh > max_wh:
                    datetime1 = datetime.combine(date(1,1,1), total_wh)
                    datetime2 = datetime.combine(date(1,1,1), max_wh)
                    extra_hours = datetime1 - datetime2
                    doc.extra_hours = extra_hours
                    if extra_hours >= timedelta(minutes=30):
                        extra_hr = datetime.strptime(str(extra_hours), "%H:%M:%S")
                        if extra_hr.minute <= 30:
                            approved_ot_hours = time(extra_hr.hour,0,0)
                        elif extra_hr.minute >= 31:
                            approved_ot_hours = time(extra_hr.hour + 1,0,0)
                    doc.approved_ot_hours = approved_ot_hours
                    doc.save()
                    # doc.submit()
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",check[-1].name,"attendance_marked",1)
                    frappe.db.set_value("Employee Checkin",check[-1].name,"attendance",doc.name)
                doc.save()
                # doc.submit()
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",check[-1].name,"attendance_marked",1)
                frappe.db.set_value("Employee Checkin",check[-1].name,"attendance",doc.name)

def multi_checkin():
    today = '2021-04-08'
    att_list = frappe.db.sql("""select name,employee from `tabAttendance` where attendance_date = %s """,(today),as_dict=True)
    for att in att_list:
        checkins = frappe.db.sql("""select log_type,employee,time from `tabEmployee Checkin` where log_date = %s and employee = %s ORDER BY time """,(today,att.employee),as_dict=True)
        in_time = ""
        out_time = ""
        if len(checkins) > 3:
            print(checkins)
            # for (i=0; i < len(checkins); i++):
            for i in range(len(checkins)) :
                if checkins[i].log_type == "IN":
                    in_time = checkins[i].time
                    print(i,'i')
                    print(in_time,'IN')
                    j = i
                    print(j)
                else:
                    for j in range(len(checkins)):
                        if checkins[i].log_type == "OUT":
                            out_time = checkins[i].time
                            if in_time and out_time:
                                wh = out_time - in_time
                            print(j,'j')
                            print(out_time,'OUT')
                            print(wh,'WH')
                            in_time = ''
                            out_time = ''
                            # i = j
            # for c in checkins:
            #     if c.log_type == 'IN':
            #         print(c)
            #         in_time = c.time
            #     print(in_time)
    # doc = frappe.get_doc("Attendance",att.name)
    # if len(check) > 4:
    #     print(check[0].time,check[-1].time)
    #     check_in = frappe.db.sql("""select name,time from `tabEmployee Checkin` where log_date = %s and employee = %s and log_type='IN' and time between %s and %s """,(att.attendance_date,att.employee,check[0].time,check[-1].time),as_dict=True)
    #     print(check_in)

def gate_entry_morning():
    count = """ <table class='table table-bordered'>
    <tr><td>A Shift : %s</td></tr>
    <tr><td>Day Shift : %s</td></tr>
    <tr><td>General Shift : %s</td></tr>
    </table>"""%(frappe.db.count("Attendance",{"shift":"A Shift","attendance_date":today()}),frappe.db.count("Attendance",{"shift":"Day Shift","attendance_date":today()}),frappe.db.count("Attendance",{"shift":"General Shift","attendance_date":today()}))
    att_list = frappe.db.sql(""" select employee,employee_name,plant,shift,tabAttendance.in from `tabAttendance` where attendance_date = %s and shift in ("A Shift","Day Shift","General Shift") """,today(),as_dict=True)
    table = """
    <table class='table table-bordered'>
        <tr>
        <td>S.No</td><td>Employee Code</td><td>Employee Name</td><td>Plant</td><td>Shift</td><td>IN Time</td>
        </tr>
        """
    i = 1
    for att in att_list:
        table += """
        <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
        """%(i,att.employee,att.employee_name,att.plant,att.shift,att["in"])
        i+=1
    content = count + table + "</table>"
    print(content)
    frappe.sendmail(
        recipients=['subash.p@groupteampro.com','anil.p@groupteampro.com'],
        subject='Daily Gate Entry Report - '+formatdate(today()),
        message="""%s"""%(content)
    )

def gate_entry_afternoon():
    count = """ <table class='table table-bordered'>
    <tr><td>B Shift : %s</td></tr>
    </table>"""%(frappe.db.count("Attendance",{"shift":"B Shift","attendance_date":today()}))
    att_list = frappe.db.sql(""" select employee,employee_name,plant,shift,tabAttendance.in from `tabAttendance` where attendance_date = %s and shift = "B Shift" """,today(),as_dict=True)
    table = """
    <table class='table table-bordered'>
        <th>
        <td>S.No</td><td>Employee Code</td><td>Employee Name</td><td>Plant</td><td>Shift</td><td>IN Time</td>
        </th>
        """
    i = 1
    for att in att_list:
        table += """
        <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
        """%(i,att.employee,att.employee_name,att.plant,att.shift,att["in"])
        i+=1
    content = count + table + "</table>"
    print(content)
    frappe.sendmail(
        recipients=['subash.p@groupteampro.com','anil.p@groupteampro.com'],
        subject='Daily Gate Entry Report - '+formatdate(today()),
        message="""%s"""%(content)
    )

def gate_entry_night():
    count = """ <table class='table table-bordered'>
    <tr><td>C Shift : %s</td></tr>
    <tr><td>Night Shift : %s</td></tr>
    </table>"""%(frappe.db.count("Attendance",{"shift":"C Shift","attendance_date":today()}),frappe.db.count("Attendance",{"shift":"Night Shift","attendance_date":today()}))
    att_list = frappe.db.sql(""" select employee,employee_name,plant,shift,tabAttendance.in from `tabAttendance` where attendance_date = %s and shift in ("C Shift","Night Shift") """,today(),as_dict=True)
    table = """
    <table class='table table-bordered'>
        <th>
        <td>S.No</td><td>Employee Code</td><td>Employee Name</td><td>Plant</td><td>Shift</td><td>IN Time</td>
        </th>
        """
    i = 1
    for att in att_list:
        table += """
        <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
        """%(i,att.employee,att.employee_name,att.plant,att.shift,att["in"])
        i+=1
    content = count + table + "</table>"
    print(content)
    frappe.sendmail(
        recipients=['subash.p@groupteampro.com','anil.p@groupteampro.com'],
        subject='Daily Gate Entry Report - '+formatdate(today()),
        message="""%s"""%(content)
    )

def no_out_report():
    att_list = frappe.db.sql("select employee, employee_name,plant,shift,`tabAttendance`.in, hour(timediff(time(now()), `tabAttendance`.in)) from `tabAttendance` where attendance_date = %s and `tabAttendance`.out is null and hour(timediff(time(now()), `tabAttendance`.in)) > 12",today(),as_dict=True)
    if att_list:    
        table = """
        Dear Sir,<br><br>Please find the list of employee for whom no out reported in Biometric Machine for 12 hours,<br><br>
        <table class='table table-bordered'>
            <tr>
            <td>S.No</td><td>Employee Code</td><td>Employee Name</td><td>Plant</td><td>Shift</td><td>IN Time</td>
            </tr>
            """
        i = 1
        for att in att_list:
            table += """
            <tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>
            """%(i,att.employee,att.employee_name,att.plant,att.shift,att["in"])
            i+=1
        content = table + "</table><br><br>Regards,<br><br>CLMS"
        print(content)
        frappe.sendmail(
            recipients=['subash.p@groupteampro.com','anil.p@groupteampro.com'],
            subject='No Exit Report - '+formatdate(today()),
            message="""%s"""%(content)
        )


# def update_attendance():
#     atts = frappe.db.sql("""select name from `tabAttendance` where attendance_date between '2021-03-01' and '2021-03-31' """)
#     for att in atts:
#         print(att[0])
#         doc = frappe.get_doc("Attendance",att[0])
#         doc.submit()
#         frappe.db.commit()
        # frappe.db.set_value("Attendance",att[0],"status","Present")

# def update_structure():
#     # frappe.get
#     emps = frappe.get_all("Employee",{'employment_type':'Subcontract','daily':1})
#     print(len(emps))
#     for emp in emps:
#         if not frappe.db.exists("Salary Structure Assignment",{'employee':emp.name}):
#             print(emp.name)
#             doc = frappe.new_doc("Salary Structure Assignment")
#             doc.employee = emp.name
#             doc.salary_structure = 'Daily Wage'
#             doj = frappe.db.get_value("Employee",emp.name,'date_of_joining')
#             if doj:
#                 doc.from_date = doj
#             else:
#                 doc.from_date = '2021-03-01'
#             doc.save(ignore_permissions=True)
#             doc.submit()
#             frappe.db.commit()

# def update_account():
#     ss = frappe.get_all("Salary Structure Assignment")
#     for s in ss:
#         print(s.name)
#         frappe.db.set_value("Salary Structure Assignment",s.name,'payroll_payable_account','Payroll Payable - TPL')

# def update_doj():
#     emps = frappe.db.sql("select name from `tabEmployee` where date_of_joining is null")
#     print(len(emps))
#     for emp in emps:
#         print(emp)
#         frappe.db.set_value("Employee",emp[0],'date_of_joining','2021-03-01')

def submit_ss():
    ss = frappe.get_all("Salary Slip")
    for s in ss:
        print(s)
        doc = frappe.get_doc("Salary Slip",s.name)
        doc.submit()
        frappe.db.commit()

@frappe.whitelist()
def change_verify_mode(biometric_pin,verify_mode):
    frappe.get_all('Employee',{'status':"Left","relieving_date":add_days(nowdate(),-1)},['biometric_pin'])
    import mysql.connector
    mydb = mysql.connector.connect(
    host="192.8.222.149",
    user="root",
    password="Pa55w0rd@",
    database="biotime"
    )

    mycursor = mydb.cursor()
    sql = "update personnel_employee set verify_mode='%s',update_time=NOW(6) WHERE emp_code='%s'" % (verify_mode,biometric_pin)
    mycursor.execute(sql)

    mydb.commit()

    return str(mycursor.rowcount) + " record(s) affected"

@frappe.whitelist()
def bulk_mark_left():
    employees = frappe.get_all('Biometric User',{'docstatus':0},['biometric_pin'])
    for emp in employees:
        verify_mode = 4
        import mysql.connector
        mydb = mysql.connector.connect(
        host="192.8.222.149",
        user="root",
        password="Pa55w0rd@",
        database="biotime"
        )

        mycursor = mydb.cursor()
        sql = "update personnel_employee set verify_mode='%s',update_time=NOW(6) WHERE emp_code='%s'" % (verify_mode,emp.biometric_pin)
        mycursor.execute(sql)

        mydb.commit()
        frappe.log_error(message=str(mycursor.rowcount) + " record(s) affected for " + emp.biometric_pin,title='Left Employee blocked in Device')

@frappe.whitelist()
def update_data():
    employees = frappe.get_all('Employee',{'subsidy_amount':0,'employment_type': ('!=','Subcontract') },'name')
    for emp in employees:
        frappe.db.set_value('Employee',emp.name,'subsidy_amount',80)
        frappe.db.commit()