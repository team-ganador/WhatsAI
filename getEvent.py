from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import paths
proxy = 'http://172.31.2.4:8080'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
path = paths.HINT_PATH
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def upComingEvents(total, start_date):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path + 'token.pickle'):
        with open(path + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path + 'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(path + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='en.indian#holiday@group.v.calendar.google.com', timeMin=start_date,
                                        maxResults=total, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    print (now)
    if not events:
        print('No upcoming events found.')
    event_list = ""
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list = event_list + (start + ' ' + event['summary'] + ' ')
    return event_list

# response = upComingEvents(10, '2019-03-20T01:00:00+05:30')
# print(response)