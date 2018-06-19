#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line sample for the Calendar API.
Command-line application that retrieves the list of the user's calendars."""
from __future__ import print_function
import copy
import datetime
import httplib2
import json
import os
import sys

from oauth2client import client
from googleapiclient import sample_tools
from apiclient import discovery
from oauth2client import tools
from oauth2client.file import Storage

import argparse
# flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
flags = None


EVENT_TEMPLATE = {'creator': {'displayName': 'Brendan Duke',
                              'email': 'brendanw.duke@gmail.com',
                              'self': True},
                  'kind': 'calendar#event',
                  'organizer': {'displayName': 'Brendan Duke',
                                'email': 'brendanw.duke@gmail.com',
                                'self': True},
                  'reminders': {'overrides': [{'method': 'popup', 'minutes': 15}],
                                'useDefault': False},
                  'sequence': 0,
                  'start': {'dateTime': '2018-01-21T20:30:00-05:00'},
                  'end': {'dateTime': '2018-01-21T21:15:00-05:00'},
                  'status': 'confirmed',
                  'summary': 'Reimagined octo tribble'}


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'automatic-calendar'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def create_events(start, end, summary, should_show_upcoming):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = copy.deepcopy(EVENT_TEMPLATE)
    event['start']['dateTime'] = '{}-04:00'.format(start)
    event['end']['dateTime'] = '{}-04:00'.format(end)

    event['summary'] = summary

    event_http = service.events().insert(calendarId='brendanw.duke@gmail.com',
                                         body=event).execute()
    print('Event created: {}'.format(event_http.get('htmlLink')))

    if not should_show_upcoming:
        return

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--day', type=str, help='Day of schedule.')
    parser.add_argument('--schedule', type=str, help='Schedule filename')

    args = parser.parse_args()

    with open(args.schedule, 'r') as f:
        schedule = json.load(f)

    for i, event in enumerate(schedule):
        start = args.day + 'T' + event['start'] + ':00'
        end = args.day + 'T' + event['end'] + ':00'
        should_show_upcoming = i == (len(schedule) - 1)
        create_events(start,
                      end,
                      event['summary'],
                      should_show_upcoming=should_show_upcoming)
