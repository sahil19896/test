from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe import _, msgprint, throw
from datetime import datetime, timedelta, date
from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client.client import Credentials
from oauth2client.file import Storage

def sync_all():
	# get the list of user with
	users = get_users_by_sync_optios('Hourly')
	sych_users_calender(users)

def sync_hourly():
	# get the list of user having sync option as "hourly"
	users = get_users_by_sync_optios('Hourly')
	sych_users_calender(users)

def sync_daily():
	# get the list of user having sync option as "Daily"
	users = get_users_by_sync_optios('Daily')
	sych_users_calender(users)

def sync_weekly():
	# get the list of user having sync option as "Weekly"
	users = get_users_by_sync_optios('Weekly')
	sych_users_calender(users)

def sync_monthly():
	# get the list of user having sync option as "Monthly"
	users = get_users_by_sync_optios('Monthly')
	sych_users_calender(users)

def get_users_by_sync_optios(mode):
	return frappe.db.sql("select gmail_id from `tabSync Configuration` where is_sync=1 and sync_options='%s'"%(mode),as_list=True)

def sych_users_calender(users):
	for user in users:
		# get user credentials from keyring storage
		store = Storage("sahil19896@gmail.com")
		credentials = store.get()
		if not credentials or credentials.invalid:
			# invalid credentials
			print "invalid credentials", user[0]
		else:
			sync_google_calendar(credentials)

def sync_google_calendar(credentials):
	# get service object
	# get all the events
	eventsResult = get_gcal_events(credentials)
	events = eventsResult.get('items', [])
	#frappe.throw(_("{0}").format(events))
	if not events:
		frappe.msgprint("No Events to Sync")
	else:
		frappe.db.sql("""UPDATE `tabSync Configuration` SET time_zone='%s' WHERE name='%s'"""%(eventsResult.get("timeZone"), frappe.session.user))
		for event in events:
			# check if event alreay synced if exist update else create new event
			if(event.get('summary')):
				e_name = is_event_already_exist(event)
				update_event(e_name, event) if e_name else save_event(event)

def get_gcal_events(credentials):
	now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	service = build('calendar', 'v3', http=credentials.authorize(Http()))
	eventsResult = service.events().list(
		calendarId='primary', timeMin=now).execute()
	events = eventsResult.get('items', [])
	#frappe.throw(_("{0}").format(events[0]))
	return eventsResult

def save_event(event):
	e = frappe.new_doc("Event")
	e = set_values(e, event)
	e.save()
	frappe.db.commit()

def update_event(name, event):
	e = frappe.get_doc("Event", name)

	if e.modified != get_formatted_updated_date(event['updated']):
		e = set_values(e, event)
		e.save()
		frappe.db.commit()

def set_values(doc, event):
	#frappe.errprint(event)
	doc.subject = event.get('summary')

	start_date = event['start'].get('dateTime', event['start'].get('date'))
	end_date = event['end'].get('dateTime', event['start'].get('date'))

	doc.starts_on = get_formatted_date(start_date)
	doc.ends_on = get_formatted_date(end_date)

	doc.all_day = 1 if doc.starts_on == doc.ends_on else 0

	if not event.get('visibility'):
		doc.event_type = "Private"
	else:
		doc.event_type =  "Private" if event['visibility'] == "private" else "Public"

	doc.description = event.get("description")
	doc.is_gcal_event = 1
	doc.event_owner = event.get("organizer").get("email")
	doc.gcal_id = event.get("id")
	add_attendees(doc, event)
	#frappe.throw(_("{0}").format(doc))
	return doc

def add_attendees(doc, event):
	if event.get("attendees"):
		for attendee in event.get("attendees"):
			doc.append("attendees",{
				"email":  attendee.get("email")
			})

def get_repeat_till_date(date, count=None, repeat_on=None):
	if count:
		if repeat_on == "Every Day":
			# add days
			date = date + timedelta(days=int(count))
		elif repeat_on == "Every Week":
			# add weeks
			date = date + timedelta(weeks=int(count))
		elif repeat_on == "Every Month":
			# add months
			date = add_months(date, int(count))
		elif repeat_on == "Every Year":
			# add years
			date = add_months(date, int(count) * 12)
		else:
			# set default value
			date = add_months(date, int(count))

	return date.strftime("%Y-%m-%d")

def add_months(date, count):
	import calendar

	month = date.month - 1 + count
	year = date.year + month / 12
	month = month % 12 + 1
	day = min(date.day,calendar.monthrange(year,month)[1])
	return datetime(year,month,day)

def get_formatted_date(str_date):
	# remove timezone from str_date
	str_date = str_date.split("+")[0]
	date = None

	date_list = str_date.split("T")
	if len(date_list) == 1:
		str_date = date_list[0] + "T00:00:00"

	date = datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
	return date

def is_event_already_exist(event):
	name = frappe.db.get_value("Event",{"gcal_id":event.get("id")},"name")
	return name

def get_formatted_updated_date(str_date):
	""" converting 2015-08-21T13:11:39.335Z string date to datetime """
	return datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.%fZ")
