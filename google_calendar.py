import datetime
import os.path
import pickle
import re
from ics import Calendar, Event

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def upload_gcal(file):
    # Access scope
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\scoob\OneDrive\Documents\Programming Projects\Python\UF_Schedule_Importer\credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    #Open calendar file with schedule event
    c = Calendar(file.read()) 

    #Loop through each event and add it to the calendar
    for course in c.events:
        r_rule = re.search(r'RRULE:.*', str(course)).group(0).rstrip()

        #Adjust for timezone
        course.begin -= datetime.timedelta(days=1, hours=-4)
        course.end -= datetime.timedelta(days=1, hours=-4)

        data = {
            'summary': course.name,
            'location': course.location,
            'description': course.description,
            'start': {
                'dateTime' : str(course.begin),
                'timeZone' : 'America/New_York'
            },
            'end': { 
                'dateTime' : str(course.end),
                'timeZone' : 'America/New_York'
            },
            'recurrence': [r_rule],
            'reminders': str(course.alarms)
        }
        
        #send data
        response = service.events().insert(calendarId='primary', body=data).execute()
        return response
