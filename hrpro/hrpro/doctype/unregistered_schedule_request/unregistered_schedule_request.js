// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Unregistered Schedule Request', {
	onload(frm) {
		frappe.call({
			method: "hrpro.hrpro.doctype.attendance_approval.attendance_approval.get_departments",
			args: {
				user: frappe.session.user
			},
			callback: function (r) {
				frm.set_df_property("dept", "options", r.message)
			}
		});
	},
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			frm.set_value("start_date", frappe.datetime.month_start())
			frm.set_value("end_date", frappe.datetime.month_end())
		}
		if (frm.doc.start_date && frm.doc.end_date && frm.doc.contractor && frm.doc.dept && frm.doc.plant) {
		frm.trigger('get_history')
		}
	},
	contractor(frm) {
		if (frm.doc.start_date && frm.doc.end_date && frm.doc.plant && frm.doc.dept && frm.doc.contractor) {
			frm.trigger('get_history')
		}
		if (frm.doc.contractor) {
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Contractor',
					filters: {
						name: frm.doc.contractor
					},
				},
				callback(r) {
					var nw_list = []
					$.each(r.message.nature_of_work_table,function(i,v){
						nw_list.push(v.nature_of_work)
					})
				frm.set_df_property("nature_of_work", "options", nw_list)
				}
			})
		}
	},
	plant(frm) {
		if (frm.doc.start_date && frm.doc.end_date && frm.doc.contractor && frm.doc.dept && frm.doc.plant) {
			frm.trigger('get_history')
		}
	},
	dept(frm) {
		frm.set_value("department", frm.doc.dept)
		if (frm.doc.start_date && frm.doc.end_date && frm.doc.contractor && frm.doc.plant && frm.doc.dept) {
			frm.trigger('get_history')
		}
	},
	get_history(frm) {
		frappe.call({
			method: "hrpro.hrpro.doctype.unregistered_schedule_request.unregistered_schedule_request.get_history",
			args: {
				"contractor": frm.doc.contractor,
				"plant": frm.doc.plant,
				"start_date": frm.doc.start_date,
				"end_date": frm.doc.end_date,
				"department": frm.doc.dept
			},
			callback(r) {
				if((r.message).length > 0){
				var table = ` <h2>Utilized RC Summary </h2><table class='table table-bordered'>
		<tr>
		<th>Request ID</th>
		<th>Contractor</th>
		<th>Plant</th>
		<th>Count</th>
		<th>Status</th>
		</tr>
		`
		var content = ""
				$.each(r.message,function(i,v){
					content = `<tr>
					<td>${v.name}</td>
					<td>${v.contractor}</td>
					<td>${v.plant}</td>
					<td>${v.count}</td>
					<td>${v.workflow_state}
					</tr>`
					table = table + content
				})
			frm.fields_dict.rc_html.$wrapper.empty().append(table)
			}
			else{
				frm.fields_dict.rc_html.$wrapper.empty()
			}
		}
		})
	},
});
