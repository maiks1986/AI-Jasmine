import os.path

from dotenv import dotenv_values

from phi.tools import Toolkit

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleToolkit(Toolkit):

    def __init__(self):
        env = dotenv_values(".env")

        self.modules = []
        self.client_id = env['GOOGLE_CLIENT_ID']
        self.client_secret = env['GOOGLE_CLIENT_SECRET']
        self.project_id = env['GOOGLE_PROJECT_ID']
        
    def registerModule(self, tool):
        self.modules.append(tool)

    def getModules(self):
        return self.modules
    
    def getClientId(self):
        return self.client_id
    
    def getClientSecret(self):
        return self.client_secret
    
    def getProjectId(self):
        return self.project_id
    
    def getCreds(self, SCOPES):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
