# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Gcal Sync",
			"color": "grey",
			"icon": "fa fa-calendar",
			"type": "module",
			"label": _("Gcal Sync")
		}
	]
