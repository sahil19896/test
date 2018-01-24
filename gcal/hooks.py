# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "gcal"
app_title = "gcal"
app_publisher = "sahil"
app_description = "Sync Google Calender"
app_icon = "fa fa-calendar"
app_color = "blue"
app_email = "sahil19896@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/gcal/css/gcal.css"
# app_include_js = "/assets/gcal/js/gcal.js"

# include js, css files in header of web template
# web_include_css = "/assets/gcal/css/gcal.css"
# web_include_js = "/assets/gcal/js/gcal.js"

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
# get_website_user_home_page = "gcal.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "gcal.install.before_install"
# after_install = "gcal.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "gcal.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
	"Event": {
		"on_update": "gcal.gcal_methods.update_gcal_event",
		"on_trash": "gcal.gcal_methods.delete_gcal_event"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
 	"all": [
 		"gcal.tasks.all"
 	],
 	"daily": [
 		"gcal.tasks.daily"
 	],
 	"hourly": [
 		"gcal.tasks.hourly"
 	],
 	"weekly": [
 		"gcal.tasks.weekly"
 	],
 	"monthly": [
 		"gcal.tasks.monthly"
 	]
 }

fixtures = ['Custom Field']

# Testing
# -------

# before_tests = "gcal.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "gcal.event.get_events"
# }

