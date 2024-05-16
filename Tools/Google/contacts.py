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
        except HttpError as err:
            print(err)

    def searchContacts(self, name, pageSize = 10, readMask = "names"):
        """Provides a list of contacts in the authenticated user's grouped contacts that matches the search query. The query matches on a contact's `names`, `nickNames`, `emailAddresses`, `phoneNumbers`, and `organizations` fields that are from the CONTACT source. **IMPORTANT**: Before searching, clients should send a warmup request with an empty query to update the cache. See https://developers.google.com/people/v1/contacts#search_the_users_contacts
        
        Args
            name (string): (required) The plain-text query for the request. The query is used to match prefix phrases of the fields on a person. For example, a person with name "foo name" matches queries such as "f", "fo", "foo", "foo n", "nam", etc., but not "oo n".
            pageSize (integer) (optional) The number of results to return. Defaults to 10 if field is not set, or set to 0. Values greater than 30 will be capped to 30.
            readMask (string): (required) A field mask to restrict which fields on each person are returned. Multiple fields can be specified by separating them with commas. Valid values are: * addresses * ageRanges * biographies * birthdays * calendarUrls * clientData * coverPhotos * emailAddresses * events * externalIds * genders * imClients * interests * locales * locations * memberships * metadata * miscKeywords * names * nicknames * occupations * organizations * phoneNumbers * photos * relations * sipAddresses * skills * urls * userDefined
        """
        try:
            service = build("people", "v1", credentials=self.creds)

            request = (
            service.people()
            .searchContacts(
                pageSize=pageSize, 
                query=name, 
                readMask=readMask
                )
            ).execute()

            return request
            #print(json.dumps(request, indent=1))
        except HttpError as err:
            print(err)

    def updateContact(self, resourceName, body=None):
        """Update contact data for an existing contact person. Any non-contact data will not be modified. Any non-contact data in the person to update will be ignored. All fields specified in the `update_mask` will be replaced. The server returns a 400 error if `person.metadata.sources` is not specified for the contact to be updated or if there is no contact source. The server returns a 400 error with reason `"failedPrecondition"` if `person.metadata.sources.etag` is different than the contact's etag, which indicates the contact has changed since its data was read. Clients should get the latest person and merge their updates into the latest person. The server returns a 400 error if `memberships` are being updated and there are no contact group memberships specified on the person. The server returns a 400 error if more than one field is specified on a field that is a singleton for contact sources: * biographies * birthdays * genders * names Mutate requests for the same user should be sent sequentially to avoid increased latency and failures.

        Args:
            resourceName: string, The resource name for the person, assigned by the server. An ASCII string in the form of `people/{person_id}`. (required)
            body: object, The request body."""

    def createContact(self,body):
        """Create a new contact and return the person resource for that contact.

        Args
            body: object, The request body"""
        service = build("people", "v1", credentials=self.getCreds(self.SCOPES))
        service.people().createContact(parent='people/me', body=body).execute()
