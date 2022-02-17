# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "hrpro"
app_title = "hrPRO"
app_publisher = "TeamPRO"
app_description = "hrPRO"
app_icon = "octicon octicon-people"
app_color = "blue"
app_email = "abdulla.pi@groupteampro.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hrpro/css/hrpro.css"
# app_include_js = "/assets/hrpro/js/hrpro.js"

# include js, css files in header of web template
# web_include_css = "/assets/hrpro/css/hrpro.css"
# web_include_js = "/assets/hrpro/js/hrpro.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "hrpro.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hrpro.install.before_install"
# after_install = "hrpro.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hrpro.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Biometric User": {
		"on_submit": "hrpro.custom.create_employee"
		# "on_cancel": "method",
		#, "on_trash": "method"
	},
    "User": {
		"on_update": "hrpro.custom.block_other_modules"
	}
}

# Scheduled Tasks
# ---------------


scheduler_events = {
    "cron": {
        # "0 10 15 * *": [
        #     "hrpro.email_alerts.pf_notification",
        #     "hrpro.email_alerts.esi_notification"
        # ],
        # "*/1 * * * *": [
        #     "hrpro.email_alerts.pf_notification"
        # ],
        # "0 10 12 11 *": [
        #     "hrpro.email_alerts.esi_half_year"
        # ],
        # "0 10 12 5 *": [
        #     "hrpro.email_alerts.esi_half_year_return"
        # ],
        # "0 10 31 3 *": [
        #     "hrpro.email_alerts.pt_notification",
        # ],
        # "0 10 20 * *": [
        #     "hrpro.email_alerts.gst_notification",
        # ],
        # "0 10 7 * *": [
        #     "hrpro.email_alerts.tds_notification",
        # ],
        # "0 10 30 4 *": [
        #     "hrpro.email_alerts.tds_march_alone",
        # ],
        # "0 10 31 7 *": [
        #     "hrpro.email_alerts.it_filling",
        # ],
        "30 6 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_c_out"
        ],
        "0 7 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_c_out"
        ],
        "30 7 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_c_out"
        ],
        "0 8 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_c_out"
        ],
        "30 8 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_c_out"
        ],
        "0 9 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_c_out"
        ],
        "15 9 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_c_out",
        ],
        "30 14 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out",
            "hrpro.custom.mark_c_out"
        ],
        "0 15 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out"
        ],
        "15 15 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out",
        ],
        "00 16 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out",
        ],
        "30 16 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out",
        ],
        "00 17 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out",
            "hrpro.custom.new_contract_employee"
        ],
        "00 18 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out",
            "hrpro.custom.no_out_report"
        ],
        "30 18 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out"
        ],
        "0 19 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out"
        ],
        "30 19 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out"
        ],
        "0 22 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out"
        ],
        "0 23 * * *": [
            "hrpro.custom.mark_in",
            "hrpro.custom.mark_ab_out",
            "hrpro.custom.no_out_report"
        ],
        "0 0 20 * *": [
        "hrpro.hrpro.doctype.contractor.contractor.rc_expiry_alert",
        ]
    },
# 	"all": [
# 		"hrpro.tasks.all"
# 	],
	"daily": [
		"hrpro.hrpro.doctype.alert_mechanism.alert_mechanism.alert_list",
        "hrpro.custom.employment_age",
        "hrpro.custom.block_employee",
        "hrpro.hrpro.doctype.contractor.contractor.wc_expiry_alert",
        "hrpro.hrpro.doctype.contractor.contractor.expired_wc",
        "hrpro.hrpro.doctype.contractor.contractor.no_rc_wc_alert"
	],
# 	"hourly": [
# 		"hrpro.tasks.hourly"
# 	],
# 	"weekly": [
# 		"hrpro.tasks.weekly"
# 	]
# 	"monthly": [
# 		"hrpro.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "hrpro.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hrpro.event.get_events"
# }
override_doctype_class = {
	"Payroll Entry": "hrpro.overrides.CustomPayrollEntry",
    # "Salary Slip": "hrpro.overrides.CustomSalarySlip"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "hrpro.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = ["Custom Field","Desk Page","Custom Script","Print Format"]
