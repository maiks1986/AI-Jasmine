import datetime

from Tools.google import GoogleToolkit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
class GoogleCalendarToolkit(GoogleToolkit):

    def __init__(self):
        self.registerModule(self)

        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ["https://www.googleapis.com/auth/contacts"]

    def getCalandarEvents(self, NumResults = 10):
        try:
            service = self.build("calendar", "v3", credentials=self.getCreds(self.SCOPES))

            # Call the Calendar API
            now = datetime.datetime.UTC.isoformat() + "Z"  # 'Z' indicates UTC time
            print("Getting the upcoming 10 events")
            events_result = (
                service.events().list(
                        calendarId="primary",
                        timeMin=now,
                        maxResults=NumResults,
                        singleEvents=True,
                        orderBy="startTime",
                    ).execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

                # Prints the start and name of the next 10 events
            return events
            '''for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                ids.append(event["id"])
                print(event["id"], start, event["summary"])'''

        except HttpError as error:
            print(f"An error occurred: {error}")
            '''for id in ids:
                event = service.events().get(calendarId='primary', eventId=id).execute()
                print(json.dumps(event, indent=1))
                return event'''
        

