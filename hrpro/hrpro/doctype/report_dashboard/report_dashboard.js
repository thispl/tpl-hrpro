// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Dashboard', {
	// refresh: function(frm) {
	// 	frm.disable_save()
	// },
	download: function (frm) {
		if (frm.doc.report == 'Form-26') {
			var path = "hrpro.hrpro.doctype.report_dashboard.form_26.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&employment_type=%(employment_type)s&contractor=%(contractor)s&plant=%(plant)s'
		}
		if (frm.doc.report == 'Form-27') {
			var path = "hrpro.hrpro.doctype.report_dashboard.form_27.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&employment_type=%(employment_type)s&contractor=%(contractor)s&plant=%(plant)s'
		}
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				// date: frm.doc.date,
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				contractor : frm.doc.contractor || "",
				employment_type:frm.doc.employment_type,
				plant:frm.doc.plant,
				// shift : frm.doc.shift
			});
		}
	},
});
