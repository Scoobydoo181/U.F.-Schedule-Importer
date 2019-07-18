import datetime
import icalendar
import re

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build

def credentials_to_dict(credentials):
  return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

def upload_gcal(file_text, creds):
    """Takes a file and an authorized credentials object
        and adds the events from the file 
        to the user's google calendar"""

    service = build('calendar', 'v3', credentials=creds)
    #Create calendar  with schedule file
    text = str(file_text, 'UTF-8').replace('\r\n', '\n')
    c = icalendar.Calendar.from_ical(text)

    r_rule_list = re.findall(r'RRULE:.*', text)
    #Loop through each event and add it to the calendar
    for i, course in enumerate(c.subcomponents[1:]):
        r_rule = r_rule_list[i+2]

        # Adjust for timezone
        course['dtstart'].dt -= datetime.timedelta(days=1)
        course['dtend'].dt -= datetime.timedelta(days=1)

        #Data to create event with GCal API
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
        #Send data
        response = service.events().insert(calendarId='primary', body=data).execute()
