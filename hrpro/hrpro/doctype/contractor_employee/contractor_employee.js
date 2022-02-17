// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contractor Employee', {
	validate: function(frm) {
		if (frm.doc.pf_number) {
            var regex = /[^0-9A-Za-z]/g;
            if (regex.test(frm.doc.pf_number) === true) {
                frappe.msgprint(__("PF No.: Only letters and numbers are allowed."));
                frappe.validated = false;
            }
            var len = frm.doc.pf_number
            if (len.length < 12 || len.length > 12) {
                frappe.throw("PF Number must be 12 digits")
                frappe.validated = false;
            }
        }
        if (frm.doc.uan) {
            var regex = /[^0-9A-Za-z]/g;
            if (regex.test(frm.doc.uan) === true) {
                frappe.msgprint(__("UAN No.: Only letters and numbers are allowed."));
                frappe.validated = false;
            }
            var len = frm.doc.uan
            if (len.length < 12 || len.length > 12) {
                frappe.throw("UAN Number must be 12 digits")
                frappe.validated = false;
            }
        }

        if (frm.doc.esi_ip_no) {
            var regex = /[^0-9]/g;
            if (regex.test(frm.doc.esi_ip_no) === true) {
                frappe.msgprint(__("ESI IP No.: Only Numbers allowed."));
                frappe.validated = false;
            }
            var len = frm.doc.esi_ip_no
            if (len.length < 10 || len.length > 10) {
                frappe.throw("ESI IP No. must be 10 digits")
                frappe.validated = false;
            }
        }
        if (frm.doc.aadhar_number) {
            var regex = /[^0-9]/g;
            if (regex.test(frm.doc.aadhar_number) === true) {
                frappe.msgprint(__("Aadhar No. Only Numbers allowed."));
                frappe.validated = false;
            }
            var len = frm.doc.aadhar_number
            if (len.length < 12 || len.length > 12) {
                frappe.throw("Aadhar No. must be 12 digits")
                frappe.validated = false;
            }
        }
	}
});
