import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Calendar():

    def __init__(self):
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
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        self.service = build("calendar", "v3", credentials=creds)

    def create_event(self, json):
        event = json
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(event.get("htmlLink"))


    def update_event(self, json):
        updated_event = self.service.events().patch (
            calendarId = 'primary',
            eventId=json['event_id'],
            body = json['body'],
            sendUpdates='all'
        ).execute()


    def get_events(self, json):
        
        events_results = self.service.events().list(
            calendarId="primary",
            timeMin=json['start_date'],
            maxResults=json['num_results'],
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        events = events_results.get("items", [])
        return events

    def delete_event(self, json):
        self.service.events().delete(
            calendarId = 'primary',
            eventId = json['event_id']
        ).execute()

'''
Used AI to figure out how to delete an event and update an event. 

Prompt: I'm using "googleapiclient.discovery" but am unable to find documentation on how to delete a calendar event. How do I do that?

And how do I update Calendar items?
'''