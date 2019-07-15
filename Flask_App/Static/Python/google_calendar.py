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
    
    service = build('calendar', 'v3', credentials=creds)
    #Open calendar file with schedule file
    text = str(file_.read(), 'UTF-8').replace('\r\n', '\n')
    c = icalendar.Calendar.from_ical(text)

    r_rule_list = re.findall(r'RRULE:.*', text)
    #Loop through each event and add it to the calendar
    for i, course in enumerate(c.subcomponents[1:]):
        r_rule = r_rule_list[i+2]#.replace('Z', '')

        # Adjust for timezone
        course['dtstart'].dt -= datetime.timedelta(days=1)
        course['dtend'].dt -= datetime.timedelta(days=1)

        data = {
            'summary': str(course["summary"]),
            'location': str(course['location']),
            'description': str(course['description']).replace('\n', ' ').rstrip(),
            'start': {
                'dateTime' : str(course['dtstart'].dt).replace(' ','T').replace('-05:', '-04:'),
                'timeZone' : 'America/New_York'
            },
            'end': { 
                'dateTime' : str(course['dtend'].dt).replace(' ','T').replace('-05:', '-04:'),
                'timeZone' : 'America/New_York'
            },
            'recurrence': [r_rule],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 5}
                ]
            }
        }
        #send data
        response = service.events().insert(calendarId='primary', body=data).execute()

if __name__ == '__main__':
    f = open(r'UF_Schedule_Importer\Flask_App\Static\Python\UFSchedule.ics')
    upload_gcal(f)
    f.close()