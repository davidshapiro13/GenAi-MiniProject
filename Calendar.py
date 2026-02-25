#Calendar interface with Google API
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class Calendar():

    #Initialize the calendar (code provided by Google)
    def __init__(self):
        self.oldest_day = '2015-05-28T09:00:00-07:00' 
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        self.service = build("calendar", "v3", credentials=creds)

    #Create a new event
    # JSON is information for event
    def create_event(self, json):
        event = json
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        return event.get("htmlLink")

    #Create many events at once
    def mass_create_events(self, json):
        urls = []
        for item in json:
            new_url = self.create_event(item)
            urls.append(new_url)

    #Update an event in the calendar that already exists
    def update_event(self, json):
        updated_event = self.service.events().patch (
            calendarId = 'primary',
            eventId=json['event_id'],
            body = json['body'],
            sendUpdates='all'
        ).execute()
        return json['event_id']


    #List all events
    def get_events(self):
        events_results = self.service.events().list(
            calendarId="primary",
            timeMin='2015-05-28T09:00:00-07:00' ,
            maxResults=200,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_results.get("items", [])
        return events

    #Delete an event
    def delete_event(self, json):
        self.service.events().delete(
            calendarId = 'primary',
            eventId = json['event_id']
        ).execute()
        return "Successfully deleted"

'''
Used AI to figure out how to delete an event and update an event. 

Prompt: I'm using "googleapiclient.discovery" but am unable to find documentation on how to delete a calendar event. How do I do that?

And how do I update Calendar items?
'''