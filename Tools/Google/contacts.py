from Tools.google import GoogleToolkit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleContactsToolkit(GoogleToolkit):

    def __init__(self):
        self.registerModule(self)

        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ["https://www.googleapis.com/auth/contacts"]


    def list(self, numberResults = 1000, personFields="names,birthdays,addresses,emailAddresses,relations",**kwargs):
        """This tool lists contacts from the Google People API thet belong to the user

        Args
            numberResults (int): The maximum number of result. Default 1000
            personFields (string): (FieldMask format) Required. A field mask to restrict which fields on each person are returned. Multiple fields can be specified by separating them with commas. Valid values are:
                addresses
                ageRanges
                biographies
                birthdays
                calendarUrls
                clientData
                coverPhotos
                emailAddresses
                events
                externalIds
                genders
                imClients
                interests
                locales
                locations
                memberships
                metadata
                miscKeywords
                names
                nicknames
                occupations
                organizations
                phoneNumbers
                photos
                relations
                sipAddresses
                skills
                urls
                userDefined
                """
        try:
            service = build("people", "v1", credentials=self.getCreds(self.SCOPES))

            # Call the People API
            print("List "+str(numberResults)+" connection names")
            results = (
                service.people()
                .connections()
                .list(
                    resourceName="people/me",
                    pageSize=numberResults,
                    personFields=personFields,
                )
                .execute()
            )
            connections = results.get("connections", [])

            return connections
            '''
            for person in connections:
            print(json.dumps(person, indent=1))
            '''
            '''
            names = person.get("names", [])
            if names:
                name = names[0].get("displayName")
                print(name)
            '''
        except HttpError as err:
            print(err)
