import speech_recognition as sr
import os
import time
from dotenv import dotenv_values
from team import Team

from Tools.basics import BasicsToolkit
from Tools.ollama import OllamaToolkit
#from output_template import OutputTemplate
from phi.assistant import Assistant, AssistantKnowledge
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.text import TextKnowledgeBase
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2

from phi.llm.ollama import Ollama
from log import Log


class Jasmine:
    def __init__(self):
        self.log = Log()
        self.team = Team()
        self.env = dotenv_values(".env")
        self.r = sr.Recognizer()
        self.conversation_started = None
        self.adjust_for_ambient_noise = False
        # Create a storage backend using the Postgres database
        
        storage = PgAssistantStorage(
            # store runs in the ai.assistant_runs table
            table_name="assistant_runs",
            # db_url: Postgres database URL
            db_url=self.env["POSTGRES_URL"],
            schema="jasmine"
        )
        knowledge_base = TextKnowledgeBase(
            path="data/docs",
            # Table name: ai.text_documents
            vector_db=PgVector2(
                collection="text_documents",
                db_url=self.env["POSTGRES_URL"],
            ),
        )
        extra_instructions = [
            "Do not use Markdown in tool_calls.",
            "Do not repeat yourself unless asked.",
            "Do not use Markdown or formatting in tool_calls!",
            #"Only use tools to communicate.",
            "Try giving a short answer if possible.",
            "Once you have used the speak tool end output and wait for new input."
            ]
        self.assistant = Assistant(
            llm=Ollama(
                model = self.env["ASSISTENT_MODEL"],
                host = self.env["OLLAMA_HOST"],
                add_user_message_after_tool_call=True,
                name="Jasmine",
                ),
            description="You are the personal AI assistant of "+self.env['USER_FULL_NAME']+" called Jasmine. You call me "+self.env["USER_SHORT_NAME"]+".",
            add_chat_history_to_messages=False,
            tools=[BasicsToolkit(), OllamaToolkit()], 
            show_tool_calls=True,
            use_tools=True,
            name="Jasmine",
            storage=storage,
            debug_mode=True,
            markdown=False,
            read_chat_history=True,
            read_tool_call_history=True,
            knowledge_base=knowledge_base,
            extra_instructions=extra_instructions,
            #team=self.team.getTeam(),
            tool_call_limit=10,
            save_output_to_file="logs/jasmine.log"
            )

    def run(self):
        self.log.Info("Assistant name: "+self.env["ASSISTANT_NAME"])
        while True:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            user_response = self.recognize_speech_from_mic(self.recognizer, self.microphone)
            if user_response["success"] and user_response["transcription"] != None:
                self.debug(user_response)
                
                if user_response['transcription'].lower().startswith(self.env["ASSISTANT_NAME"].lower()):
                    self.jasmin(user_response['transcription'])
                    self.debug(user_response['transcription'])
                elif self.conversation_started != None and self.conversation_started + 60 >= time.time():
                    self.assistant.print_response(user_response['transcription'], markdown=False, stream=False)
                else:
                    if user_response["error"] != None:
                        self.debug(user_response["error"])
                    else:
                        print("Did not hear "+self.env["ASSISTANT_NAME"]+" but did hear: "+ user_response['transcription'])


 
    def jasmin(self, input):
        self.log.Info("input: "+input)
        if input.lower().startswith("jasmine") or input.lower().startswith("jasmin"):
            self.conversation_started = time.time()
            if input.lower().startswith("jasmine"):
                new_input = input.lower().replace("jasmine ", "")
                self.log.Info("removed jasmine")
            elif input.lower().startswith("jasmin"):
                new_input = input.lower().replace("jasmin ", "")
                self.log.Info("removed jasmin")
            self.log.Info("new input: "+new_input)

            if new_input.lower().strip() == "exit":
                exit()
            else:
                self.assistant.print_response(input, markdown=False, stream=False)


    def recognize_speech_from_mic(self, recognizer, microphone):


        """ code stolen from Real Python
        
        Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                successful
        "error":   `None` if no error occured, otherwise a string containing
                an error message if the API could not be reached or
                speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        if not self.adjust_for_ambient_noise:
            with microphone as source:
                self.log.Info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, 1)
                self.adjust_for_ambient_noise = True
                self.log.Info("Adjusting for ambient noise done!!")
                self.recognizer.dynamic_energy_threshold = True

        with microphone as source:
            audio = recognizer.listen(source, None, 9)
            if not audio:
                self.log.Info("Nothing recieved trying again..")

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_google(audio)
            print(response)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
            self.debug(response)
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"
            self.debug(response)

        return response
    


jasmine = Jasmine()
jasmine.run()