import datetime
import os.path
import pickle
import re
# from ics import Calendar, Event

import icalendar

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def upload_gcal(file_):
    
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    flow = InstalledAppFlow.from_client_secrets_file('UF_Schedule_Importer/Flask_App/Static/Python/credentials.json', SCOPES)
    creds = flow.run_local_server()
    service = build('calendar', 'v3', credentials=creds)

    creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
    if os.path.exists(r'C:\Users\scoob\OneDrive\Documents\Programming Projects\Python\UF_Schedule_Importer\Flask_App\Static\Python\token.pickle'):
        with open(r'C:\Users\scoob\OneDrive\Documents\Programming Projects\Python\UF_Schedule_Importer\Flask_App\Static\Python\token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(r'C:\Users\scoob\OneDrive\Documents\Programming Projects\Python\UF_Schedule_Importer\Flask_App\Static\Python\credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(r'C:\Users\scoob\OneDrive\Documents\Programming Projects\Python\UF_Schedule_Importer\Flask_App\Static\Python\token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    #Open calendar file with schedule file
    c = icalendar.Calendar.from_ical(file_.read())

    #Loop through each event and add it to the calendar
    for i, course in enumerate(c.subcomponents[1:]):
        r_rule = re.search(r'RRULE:.*', str(file_.read())).group(i).rstrip()

        #Adjust for timezone
        # course.begin -= datetime.timedelta(days=1, hours=-4)
        # course.end -= datetime.timedelta(days=1, hours=-4)

        data = {
            'summary': course["summary"],
            'location': course['location'],
            'description': course['description'],
            'start': {
                'dateTime' : str(course['dtstart']),
                'timeZone' : 'America/New_York'
            },
            'end': { 
                'dateTime' : str(course['dtend']),
                'timeZone' : 'America/New_York'
            },
            'recurrence': r_rule,
            'reminders': str(course['alarm'])
        }
        print(data)
        #send data
        response = service.events().insert(calendarId='primary', body=data).execute()
        return response

if __name__ == '__main__':
    f = open(r'UF_Schedule_Importer\Flask_App\Static\Python\UFSchedule.ics')
    upload_gcal(f)
    f.close()