
from __future__ import print_function
import httplib2
import os
import sys
import datetime
import json
import re

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from pprint import pprint
import CreateCredentials

DATE_REGEX = '(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})'

def get_credentials():
    credentials = CreateCredentials.get_credentials()
    return credentials

def update_calendar(events_to_add=[], events_to_delete=[]):
    """Adds new events and deletes removed events
    """
    if not events_to_add and not events_to_delete:
        print('Everything already up to date')
        return 0
    if not events_to_add:
        print('No events to add')
    if not events_to_delete:
        print('No events to delete')
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    args = sys.argv

    # Get calendar events, populate eventIdTable
    eventIdTable = dict()
    page_token = None

    # Create event id dictionary for deletion lookup
    while True:
        # get list of events from calendar
        events = service.events().list(calendarId='primary', pageToken=page_token, singleEvents=True).execute()
        for event in events['items']:
            short_date = re.search(DATE_REGEX, event['start']['dateTime'])
            key = event['summary'].strip(' ') + str(short_date.group(0))
            eventIdTable[key] = event['id']
        page_token = events.get('nextPageToken')
        if not page_token:
            break

    # Add New Events
    for event in events_to_add:
        key = event['summary'].strip(' ') + event['start']['dateTime']
        # if key not in eventIdTable:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: {} : {}'.format(event['summary'].strip(' '), event['start']['dateTime']))

    # Delete Removed Events
    for event in events_to_delete:
        key = event['summary'].strip(' ') + event['start']['dateTime']
        service.events().delete(calendarId='primary', eventId=eventIdTable[key]).execute()
        print('Event deleted: {} : {}'.format(event['summary'].strip(' '), event['start']['dateTime']))

    return 0
