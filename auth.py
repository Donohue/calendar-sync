#!/usr/bin/env python
import os

from oauth2client.client import OAuth2WebServerFlow

flow = OAuth2WebServerFlow(
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=os.environ['REDIRECT_URI'],
    approval_prompt='force'
)
auth_uri = flow.step1_get_authorize_url()
print 'Go here: ' + auth_uri
code = raw_input('Enter the code: ')
credentials = flow.step2_exchange(code)
print credentials.to_json()
