from . import __version__ as app_version

app_name = "skyway"
app_title = "Skyway"
app_publisher = "erpcloud.systems"
app_description = "customizations"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@erpcloud.systems"
app_license = "MIT"



doc_events = {
"Quotation": {
	"before_insert": "skyway.event_triggers.quot_before_insert",
	"after_insert": "skyway.event_triggers.quot_after_insert",
	"onload": "skyway.event_triggers.quot_onload",
	"before_validate": "skyway.event_triggers.quot_before_validate",
	"validate": "skyway.event_triggers.quot_validate",
	"on_submit": "skyway.event_triggers.quot_on_submit",
	"on_cancel": "skyway.event_triggers.quot_on_cancel",
	"on_update_after_submit": "skyway.event_triggers.quot_on_update_after_submit",
	"before_save": "skyway.event_triggers.quot_before_save",
	"before_cancel": "skyway.event_triggers.quot_before_cancel",
	"on_update": "skyway.event_triggers.quot_on_update",
},
	"Sales Invoice": {
	"before_insert": "skyway.event_triggers.siv_before_insert",
	"after_insert": "skyway.event_triggers.siv_after_insert",
	"onload": "skyway.event_triggers.siv_onload",
	"before_validate": "skyway.event_triggers.siv_before_validate",
	"validate": "skyway.event_triggers.siv_validate",
	"on_submit": "skyway.event_triggers.siv_on_submit",
	"on_cancel": "skyway.event_triggers.siv_on_cancel",
	"on_update_after_submit": "skyway.event_triggers.siv_on_update_after_submit",
	"before_save": "skyway.event_triggers.siv_before_save",
	"before_cancel": "skyway.event_triggers.siv_before_cancel",
	"on_update": "skyway.event_triggers.siv_on_update",
},
	"Sales Order": {
		"before_insert": "skyway.event_triggers.so_before_insert",
		"after_insert": "skyway.event_triggers.so_after_insert",
		"onload": "skyway.event_triggers.so_onload",
		"before_validate": "skyway.event_triggers.so_before_validate",
		"validate": "skyway.event_triggers.so_validate",
		"on_submit": "skyway.event_triggers.so_on_submit",
		"on_cancel": "skyway.event_triggers.so_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.so_on_update_after_submit",
		"before_save": "skyway.event_triggers.so_before_save",
		"before_cancel": "skyway.event_triggers.so_before_cancel",
		"on_update": "skyway.event_triggers.so_on_update",

},
	"Material Request": {
		"before_insert": "skyway.event_triggers.mr_before_insert",
		"after_insert": "skyway.event_triggers.mr_after_insert",
		"onload": "skyway.event_triggers.mr_onload",
		"before_validate": "skyway.event_triggers.mr_before_validate",
		"validate": "skyway.event_triggers.mr_validate",
		"on_submit": "skyway.event_triggers.mr_on_submit",
		"on_cancel": "skyway.event_triggers.mr_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.mr_on_update_after_submit",
		"before_save": "skyway.event_triggers.mr_before_save",
		"before_cancel": "skyway.event_triggers.mr_before_cancel",
		"on_update": "skyway.event_triggers.mr_on_update",
},
	"Stock Entry": {
		"before_insert": "skyway.event_triggers.ste_before_insert",
		"after_insert": "skyway.event_triggers.ste_after_insert",
		"onload": "skyway.event_triggers.ste_onload",
		"before_validate": "skyway.event_triggers.ste_before_validate",
		"validate": "skyway.event_triggers.ste_validate",
		"on_submit": "skyway.event_triggers.ste_on_submit",
		"on_cancel": "skyway.event_triggers.ste_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.ste_on_update_after_submit",
		"before_save": "skyway.event_triggers.ste_before_save",
		"before_cancel": "skyway.event_triggers.ste_before_cancel",
		"on_update": "skyway.event_triggers.ste_on_update",
},
	"Delivery Note": {
		"before_insert": "skyway.event_triggers.dn_before_insert",
		"after_insert": "skyway.event_triggers.dn_after_insert",
		"onload": "skyway.event_triggers.dn_onload",
		"before_validate": "skyway.event_triggers.dn_before_validate",
		"validate": "skyway.event_triggers.dn_validate",
		"on_submit": "skyway.event_triggers.dn_on_submit",
		"on_cancel": "skyway.event_triggers.dn_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.dn_on_update_after_submit",
		"before_save": "skyway.event_triggers.dn_before_save",
		"before_cancel": "skyway.event_triggers.dn_before_cancel",
		"on_update": "skyway.event_triggers.dn_on_update",
},
	"Purchase Order": {
		"before_insert": "skyway.event_triggers.po_before_insert",
		"after_insert": "skyway.event_triggers.po_after_insert",
		"onload": "skyway.event_triggers.po_onload",
		"before_validate": "skyway.event_triggers.po_before_validate",
		"validate": "skyway.event_triggers.po_validate",
		"on_submit": "skyway.event_triggers.po_on_submit",
		"on_cancel": "skyway.event_triggers.po_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.po_on_update_after_submit",
		"before_save": "skyway.event_triggers.po_before_save",
		"before_cancel": "skyway.event_triggers.po_before_cancel",
		"on_update": "skyway.event_triggers.po_on_update",
},
	"Purchase Receipt": {
		"before_insert": "skyway.event_triggers.pr_before_insert",
		"after_insert": "skyway.event_triggers.pr_after_insert",
		"onload": "skyway.event_triggers.pr_onload",
		"before_validate": "skyway.event_triggers.pr_before_validate",
		"validate": "skyway.event_triggers.pr_validate",
		"on_submit": "skyway.event_triggers.pr_on_submit",
		"on_cancel": "skyway.event_triggers.pr_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.pr_on_update_after_submit",
		"before_save": "skyway.event_triggers.pr_before_save",
		"before_cancel": "skyway.event_triggers.pr_before_cancel",
		"on_update": "skyway.event_triggers.pr_on_update",
},
	"Purchase Invoice": {
		"before_insert": "skyway.event_triggers.piv_before_insert",
		"after_insert": "skyway.event_triggers.piv_after_insert",
		"onload": "skyway.event_triggers.piv_onload",
		"before_validate": "skyway.event_triggers.piv_before_validate",
		"validate": "skyway.event_triggers.piv_validate",
		"on_submit": "skyway.event_triggers.piv_on_submit",
		"on_cancel": "skyway.event_triggers.piv_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.piv_on_update_after_submit",
		"before_save": "skyway.event_triggers.piv_before_save",
		"before_cancel": "skyway.event_triggers.piv_before_cancel",
		"on_update": "skyway.event_triggers.piv_on_update",
},
	"Payment Entry": {
		"before_insert": "skyway.event_triggers.pe_before_insert",
		"after_insert": "skyway.event_triggers.pe_after_insert",
		"onload": "skyway.event_triggers.pe_onload",
		"before_validate": "skyway.event_triggers.pe_before_validate",
		"validate": "skyway.event_triggers.pe_validate",
		"on_submit": "skyway.event_triggers.pe_on_submit",
		"on_cancel": "skyway.event_triggers.pe_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.pe_on_update_after_submit",
		"before_save": "skyway.event_triggers.pe_before_save",
		"before_cancel": "skyway.event_triggers.pe_before_cancel",
		"on_update": "skyway.event_triggers.pe_on_update",
},
	"Blanket Order": {
		"before_insert": "skyway.event_triggers.blank_before_insert",
		"after_insert": "skyway.event_triggers.blank_after_insert",
		"onload": "skyway.event_triggers.blank_onload",
		"before_validate": "skyway.event_triggers.blank_before_validate",
		"validate": "skyway.event_triggers.blank_validate",
		"on_submit": "skyway.event_triggers.blank_on_submit",
		"on_cancel": "skyway.event_triggers.blank_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.blank_on_update_after_submit",
		"before_save": "skyway.event_triggers.blank_before_save",
		"before_cancel": "skyway.event_triggers.blank_before_cancel",
		"on_update": "skyway.event_triggers.blank_on_update",
},
	"Expense Claim": {
		"before_insert": "skyway.event_triggers.excl_before_insert",
		"after_insert": "skyway.event_triggers.excl_after_insert",
		"onload": "skyway.event_triggers.excl_onload",
		"before_validate": "skyway.event_triggers.excl_before_validate",
		"validate": "skyway.event_triggers.excl_validate",
		"on_submit": "skyway.event_triggers.excl_on_submit",
		"on_cancel": "skyway.event_triggers.excl_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.excl_on_update_after_submit",
		"before_save": "skyway.event_triggers.excl_before_save",
		"before_cancel": "skyway.event_triggers.excl_before_cancel",
		"on_update": "skyway.event_triggers.excl_on_update",
},
"Employee Advance": {
		"before_insert": "skyway.event_triggers.emad_before_insert",
		"after_insert": "skyway.event_triggers.emad_after_insert",
		"onload": "skyway.event_triggers.emad_onload",
		"before_validate": "skyway.event_triggers.emad_before_validate",
		"validate": "skyway.event_triggers.emad_validate",
		"on_submit": "skyway.event_triggers.emad_on_submit",
		"on_cancel": "skyway.event_triggers.emad_on_cancel",
		"on_update_after_submit": "skyway.event_triggers.emad_on_update_after_submit",
		"before_save": "skyway.event_triggers.emad_before_save",
		"before_cancel": "skyway.event_triggers.emad_before_cancel",
		"on_update": "skyway.event_triggers.emad_on_update",
},
}


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/skyway/css/skyway.css"
# app_include_js = "/assets/skyway/js/skyway.js"

# include js, css files in header of web template
# web_include_css = "/assets/skyway/css/skyway.css"
# web_include_js = "/assets/skyway/js/skyway.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "skyway/public/scss/website"

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

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "skyway.install.before_install"
# after_install = "skyway.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "skyway.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"skyway.tasks.all"
# 	],
# 	"daily": [
# 		"skyway.tasks.daily"
# 	],
# 	"hourly": [
# 		"skyway.tasks.hourly"
# 	],
# 	"weekly": [
# 		"skyway.tasks.weekly"
# 	]
# 	"monthly": [
# 		"skyway.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "skyway.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "skyway.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "skyway.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"skyway.auth.validate"
# ]

