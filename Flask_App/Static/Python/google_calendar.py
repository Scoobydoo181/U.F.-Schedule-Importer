import datetime
import os.path
import pickle
import re
from ics import Calendar, Event

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def upload_gcal(file_):
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    flow = InstalledAppFlow.from_client_secrets_file('Static/Python/credentials.json', SCOPES)
    creds = flow.run_local_server()
    service = build('calendar', 'v3', credentials=creds)
    
    #Open calendar file with schedule file
    c = Calendar(file_.readlines())

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

if __name__ == '__main__':
    f = open('UFSchedule.ics')
    upload_gcal(f)
    f.close()