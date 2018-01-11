from __future__ import print_function
import datetime
import dateutil.parser
import httplib2
import os
import pytz
import time

from apiclient.discovery import build
from oauth2client.client import Credentials, OAuth2WebServerFlow

def lambda_handler(event, context):
    starts = dateutil.parser.parse(event['params']['querystring']['starts'])
    ends = dateutil.parser.parse(event['params']['querystring']['ends'])
    duration = (ends - starts).total_seconds()
    if duration > 0 and duration < 6*60*60:
        create_calendar_event(starts, ends)

def calendar_service():
    flow = OAuth2WebServerFlow(
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        scope='https://www.googleapis.com/auth/calendar.readonly',
        redirect_uri=os.environ['REDIRECT_URI'],
        approval_prompt='force'
    )

    credentials_json = os.environ['CREDENTIALS']
    credentials = Credentials.new_from_json(credentials_json)
    if credentials is None or credentials.invalid:
        credentials = run(flow, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('calendar', 'v3', http=http)

def create_calendar_event(starts, ends):
    service = calendar_service()
    timezone = 'America/New_York'
    body = {
        'summary': 'Busy',
        'description': 'This event was automatically created.',
        'start': {
            'dateTime': starts.isoformat(),
            'timeZone': timezone
        },
        'end': {
            'dateTime': ends.isoformat(),
            'timeZone': timezone
        }
    }
    event = service.events().insert(calendarId='primary', body=body).execute()
    print(event)

if __name__ == '__main__':
    starts = datetime.datetime.now()
    ends = starts.replace(hour=starts.hour+1)
    create_calendar_event(starts, ends)

