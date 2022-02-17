// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Approval', {
	onload(frm){
		frappe.call({
			method: "hrpro.hrpro.doctype.attendance_approval.attendance_approval.get_departments",
			args:{
				user:frappe.session.user
			},
			callback: function(r) {
				frm.set_df_property("department", "options", r.message)
			}
		});
	},
	refresh: function(frm) {
		frm.disable_save()
		frm.fields_dict['ot_child'].grid.wrapper.find('.grid-add-row').hide();
		frm.fields_dict['ot_child'].grid.wrapper.find('.grid-remove-rows').hide();
	},
	attendance_date(frm){
		if(frm.doc.attendance_date){
		if(frm.doc.plant){
			frm.trigger('fetch')
		}
	}
	},
	department(frm){
		if(frm.doc.attendance_date){
		if(frm.doc.plant){
			frm.trigger('fetch')
		}
	}
	},
	plant(frm){
		if(frm.doc.attendance_date){
		if(frm.doc.plant){
			frm.trigger('fetch')
		}
	}},
	without_ot(frm){
		if(frm.doc.attendance_date){
		if(frm.doc.plant){
			frm.trigger('fetch')
		}
	}
	},
	fetch(frm){
		if (frm.doc.plant != "TPL (All Plants)"){
		frappe.call({
			method:"hrpro.hrpro.doctype.attendance_approval.attendance_approval.get_attendance",
			args:{
				"attendance_date":frm.doc.attendance_date,
				"department":frm.doc.department,
				"plant":frm.doc.plant,
				"without_ot":frm.doc.without_ot
			},
			freeze:true,
			freeze_message:"Loading",
			callback(r){
				frm.clear_table('ot_child')
				frm.refresh_field('ot_child')
				$.each(r.message,function(i,v){
					frm.add_child('ot_child',{
						employee : v.employee,
						employee_name : v.employee_name,
						attendance : v.name,
						department:v.department,
						contractor:v.contractor,
						contract_type:v.contract_type,
						shift : v.shift,
						in : v.in,
						out : v.out,
						total_working_hours : v.total_working_hours,
						extra_hours : v.extra_hours,
						approved_ot_hours : v.approved_ot_hours

					})
					frm.refresh_field('ot_child')
				})
			}
		})
	}
	else{
		frappe.msgprint("Please select only one Plant")
	}
	},
	submit(frm){
		var table_list = []
        $.each(frm.doc.ot_child, function (i, d) {
            if (d.__checked == 1) {
				if(!d.shift){
					frappe.throw("Please select Shift")
				}
				if(!d.in){
					frappe.throw("Please enter IN Time")
				}
				if(!d.out){
					frappe.throw("Please enter Out Time")
				}
				if(!d.contract_type){
					frappe.throw("Please Choose Contract Type")
				}
				if(d.shift && d.in && d.out && d.contract_type){
                table_list.push({"idx":d.idx,"employee":d.employee,"attendance":d.attendance,"department":d.department,"shift":d.shift,"contractor":d.contractor,"contract_type":d.contract_type,"in":d.in,"out":d.out,"total_working_hours":d.total_working_hours,"extra_hours":d.extra_hours,"approved_ot_hours":d.approved_ot_hours})
			}
            }
        });
		if(table_list.length != 0){
			frappe.call({
				method:"hrpro.hrpro.doctype.attendance_approval.attendance_approval.update_attendance",
				args:{
					table: table_list,
					date:frm.doc.attendance_date
				},
				callback(r){
					if(r.message){
					$.each(r.message,function(i,v){
					frm.get_field("ot_child").grid.grid_rows[v-1].remove();
					})
					frm.refresh_field('ot_child')
					frappe.msgprint("Attendance Submitted Successfully")
					}
				}
			})
		}
		else{
			frappe.throw("Please choose atleast one Attendance")
		}
	}
});
frappe.ui.form.on('OT Child', {
	in(frm,cdt,cdn){
		let row = frappe.get_doc(cdt, cdn);
		if(row.in && row.out && row.shift){
		calculate_hours(frm,row,cdt,cdn)
		}
	},
	out(frm,cdt,cdn){
		let row = frappe.get_doc(cdt, cdn);
		if(row.in && row.out && row.shift){
		calculate_hours(frm,row,cdt,cdn)
		}
	},
	shift(frm,cdt,cdn){
		let row = frappe.get_doc(cdt, cdn);
		if(row.in && row.out && row.shift){
		calculate_hours(frm,row,cdt,cdn)
		}
	}
	
});
let calculate_hours = function(frm,row,cdt,cdn){
	frappe.call({
		method:"hrpro.hrpro.doctype.attendance_approval.attendance_approval.calculate_hours",
		args:{
			row:row,
		},
		callback(r){
			frappe.model.set_value(cdt,cdn,"total_working_hours",r.message.twh)
			frappe.model.set_value(cdt,cdn,"extra_hours",r.message.ext)
			frappe.model.set_value(cdt,cdn,"approved_ot_hours",r.message.ot)
		}
	})
}
