frappe.ui.form.on('RC Schedule Request', {
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
		if (frm.doc.start_date && frm.doc.end_date && frm.doc.plant && frm.doc.dept && frm.doc.contractor) {
			frm.trigger('check_availability')
		}
		if (frm.doc.start_date && frm.doc.end_date && frm.doc.plant && frm.doc.dept && frm.doc.contractor) {
			frm.trigger('get_rc_schedule_history')
		}
	},
	after_workflow_action: (frm) => {
		frm.call('send_mail', {
			status: frm.doc.workflow_state
		})
	},
	get_rc_schedule_history(frm) {
		if (frappe.user.has_role("HOD")) {
			frm.call('get_hod_rc')
				.then(r => {
					if (r.message) {
						var table = `<h2>RC Request History</h2> <table class='table table-bordered'>
			<tr>
			<th>Request ID</th>
			<th>Contractor</th>
			<th>Plant</th>
			<th>Department</th>
			<th>Count</th>
			<th>Status</th>
			</tr>
			`
						var content = ""
						$.each(r.message, function (i, v) {
							content = `<tr>
						<td>${v.name}</td>
						<td>${v.contractor}</td>
						<td>${v.plant}</td>
						<td>${v.department}</td>
						<td>${v.manpower_count}</td>
						<td>${v.workflow_state}
						</tr>`
							table = table + content
						})
						frm.fields_dict.rc_html.$wrapper.empty().append(table)
					}
					else {
						frm.fields_dict.rc_html.$wrapper.empty()
					}
				})
		}
		else if (frappe.user.has_role("General Manager")) {
			frm.call('get_gm_rc')
				.then(r => {
					if (r.message) {
						var table = `<h2>RC Request History</h2> <table class='table table-bordered'>
			<tr>
			<th>Request ID</th>
			<th>Contractor</th>
			<th>Plant</th>
			<th>Department</th>
			<th>Count</th>
			<th>Status</th>
			</tr>
			`
						var content = ""
						$.each(r.message, function (i, v) {
							content = `<tr>
						<td>${v.name}</td>
						<td>${v.contractor}</td>
						<td>${v.plant}</td>
						<td>${v.department}</td>
						<td>${v.manpower_count}</td>
						<td>${v.workflow_state}
						</tr>`
							table = table + content
						})
						frm.fields_dict.rc_html.$wrapper.empty().append(table)
					}
					else {
						frm.fields_dict.rc_html.$wrapper.empty()
					}
				})
		}
		else if (frappe.user.has_role("VP")) {
			frm.call('get_vp_rc')
				.then(r => {
					if (r.message) {
						var table = `<h2>RC Request History</h2> <table class='table table-bordered'>
			<tr>
			<th>Request ID</th>
			<th>Contractor</th>
			<th>Plant</th>
			<th>Department</th>
			<th>Count</th>
			<th>Status</th>
			</tr>
			`
						var content = ""
						$.each(r.message, function (i, v) {
							content = `<tr>
						<td>${v.name}</td>
						<td>${v.contractor}</td>
						<td>${v.plant}</td>
						<td>${v.department}</td>
						<td>${v.manpower_count}</td>
						<td>${v.workflow_state}
						</tr>`
							table = table + content
						})
						frm.fields_dict.rc_html.$wrapper.empty().append(table)
					}
					else {
						frm.fields_dict.rc_html.$wrapper.empty()
					}
				})
		}
	},
	// start_date: function (frm) {
	// 	if (frm.doc.start_date) {
	// 		frappe.call({
	// 			method: 'erpnext.payroll.doctype.payroll_entry.payroll_entry.get_end_date',
	// 			args: {
	// 				frequency: "Monthly",
	// 				start_date: frm.doc.start_date
	// 			},
	// 			callback: function (r) {
	// 				if (r.message) {
	// 					frm.set_value('end_date', r.message.end_date);
	// 					if (frm.doc.contractor && frm.doc.plant) {
	// 						frm.trigger('check_availability')
	// 					}
	// 				}
	// 			}
	// 		});
	// 	}
	// },
	contractor(frm) {
		if (frm.doc.start_date && frm.doc.end_date && frm.doc.plant && frm.doc.dept && frm.doc.contractor) {
			frm.trigger('check_availability')
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
			frm.trigger('check_availability')
		}
	},
	dept(frm) {
		frm.set_value("department", frm.doc.dept)
		if (frm.doc.start_date && frm.doc.end_date && frm.doc.contractor && frm.doc.plant && frm.doc.dept) {
			frm.trigger('check_availability')
		}
	},
	check_availability(frm) {
		frm.call('check_availability')
			.then(r => {
				frm.fields_dict.av_html.$wrapper.empty().append(` <h2>RC Availability Details</h2><table class='table table-bordered'>
		<tr>
		<th>RC Registered Count</th>
		<td>${r.message[0]}</td>
		<th>WC Registered Count</th>
		<td>${r.message[2]}</td>
		</tr>
		<tr>
		<th>RC Available Count</th>
		<td>${r.message[1]}</td>
		<th>WC Available Count</th>
		<td>${r.message[3]}</td>
		</tr>
		
		</table>
		`)
			})
	}
});