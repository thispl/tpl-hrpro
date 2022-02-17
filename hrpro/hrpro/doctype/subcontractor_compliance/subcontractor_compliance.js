// Copyright (c) 2020, frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subcontractor Compliance', {
	// refresh: function(frm) {

	// },
	validate(frm){
		var list = [frm.doc.esic,frm.doc.pf,frm.doc.age,frm.doc.salary_credit]
		if(list.includes(0)){
			frm.set_value('status','Unpaid')
		}
		else{
			frm.set_value('status','Paid')
		}
	}
});
