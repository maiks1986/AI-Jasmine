from phi.assistant import Assistant

from phi.llm.ollama import Ollama

from Tools.basics import BasicsToolkit
from Tools.ollama import OllamaToolkit
from Tools.google import GoogleToolkit
from Tools.Google.calendar import GoogleCalendarToolkit
from Tools.Google.contacts import GoogleContactsToolkit
from Tools.Google.mail import GoogleMailToolkit

class Team:
    def __init__(self):
        self.debug = True
        self.team = []
        self.team.append(self.SpeechElevenLabs())
        self.team.append(self.ConsoleOutput())
        self.team.append(self.OllamaInput())

    def getTeam(self):
        return self.team
    
    def getOllama(self, model = "llama3", host = "127.0.0.1:11434"):
        self.ollama = Ollama(
                model=model,
                host=host,
                )
        return self.ollama
    
    def SpeechElevenLabs(self):
        bt = BasicsToolkit()
        self.speech_eleven_labs = Assistant(
            llm=self.getOllama(),
            name='Voice Output',
            role='Gives voice output',
            tool_call_limit=1,
            show_tool_calls=self.debug,
            tools=[bt.sapiSpeak],
            
            instructions=["if you reply start with your name! Only use your tool.", "REMEMBER: To use a tool, you must respond only in JSON format.", "To use a tool, just respond with the JSON matching the schema. Nothing else. Do not add any additional notes or explanations" ],
            )
        return self.speech_eleven_labs
    
    def ConsoleOutput(self):
        bt = BasicsToolkit()
        self.console_output = Assistant(
            llm=self.getOllama(),
            name='Chat Output',
            role='Gives chat output',
            tool_call_limit=1,
            show_tool_calls=self.debug,
            tools=[bt.chat]
            )
        return self.console_output
    
    def OllamaInput(self):
        self.ollama_input = Assistant(
            llm=self.getOllama(),
            name='Ollama Input',
            role='Gets output from Ollama Models',
            show_tool_calls=self.debug,
            tools=[OllamaToolkit()]
            )
        return self.ollama_input
    
    def GoogleCalendarInput(self):
        self.google_calendar_input = Assistant(
            llm=self.getOllama(),
            name='Google Calendar Input',
            role='Gets output from Google Calendar Models',
            show_tool_calls=self.debug,
            tools=[GoogleCalendarToolkit()]
            )
        return self.ollama_input
    
    def GoogleContactsInput(self):
        self.google_calendar_input = Assistant(
            llm=self.getOllama(),
            name='Google Calendar Input',
            role='Gets output from Google Calendar Models',
            show_tool_calls=self.debug,
            tools=[GoogleContactsToolkit()]
            )
        return self.ollama_input
    
    def GoogleMailInput(self):
        self.google_calendar_input = Assistant(
            llm=self.getOllama(),
            name='Google Calendar Input',
            role='Gets output from Google Calendar Models',
            show_tool_calls=self.debug,
            tools=[GoogleMailToolkit()]
            )
        return self.ollama_input
