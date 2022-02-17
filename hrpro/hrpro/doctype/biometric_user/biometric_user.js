// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Biometric User', {
	refresh: function(frm) {
		// frappe.call({
		// 	method:"hrpro.custom.create_employee",
		// 	args:{
		// 		doc:frm.doc.name}
		// })
	},
	validate(frm){
		if(frm.doc.employment_type == "Subcontract"){
		if(!frm.doc.contractor){
			frappe.throw("Please fill Contractor Name")
		}
		if(!frm.doc.uan_no){
			frappe.throw("Please fill UAN Number")
		}
		if(!frm.doc.esi_ip_no){
			frappe.throw("Please fill ESI IP Number")
		}
		}
	}
});
