from typing import List
from phi.tools import Toolkit
from phi.utils.log import logger
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from dotenv import dotenv_values
from playsound import playsound

import asyncio
import edge_tts
import sys
import edge_tts
import win32com.client 


class BasicsToolkit(Toolkit):
    def __init__(self,
                 _api_key = dotenv_values(".env")["ELEVENLABS_KEY"], 
                 voice = "Charlotte",
                 model = "eleven_multilingual_v2"
                 ):
        env = dotenv_values(".env")
        super().__init__(name="basics")
        self.register(self.sapiSpeak)
        #self.register(self.edgeSpeak)
        #self.register(self.elevenLabsSpeak)
        self.register(self.chat)
        self.register(self.exit)
        self.client = ElevenLabs(api_key=_api_key)
        self.voice = voice
        self.model = model

    def sapiSpeak(self, message, voice=1):
        """Speaks to user using edge TTS. Try to alway use this one time when responding. End response after this tool.

        Args:
            message (string): The full string of the message you want to send.
            voice (string) Options:
                0 = David
                1 = Zira (Default) Use this one!"""
        speaker = win32com.client.Dispatch("SAPI.SpVoice") 
        speaker.Voice = speaker.GetVoices().Item(voice)
        speaker.Speak(message) 


    def edgeSpeak(self, message, voice = "en-GB-SoniaNeural"):
        """Speaks to user using edge TTS. Try to alway use this one time when responding. End response after this tool.

        Args:
            message (string): The full string of the message you want to send.
            voice (string) Options:
                en-GB-LibbyNeural
                en-GB-MaisieNeural
                en-GB-SoniaNeural
                en-US-AnaNeural
                en-US-AriaNeural
                en-US-AvaMultilingualNeural
                en-US-AvaNeural
                en-US-EmmaMultilingualNeural
                en-US-EmmaNeural
                en-US-JennyNeural
                en-US-MichelleNeural
        """
        
        #asyncio.run(self.play(message, voice))
        return

    async def play(self, TEXT, VOICE = "en-GB-SoniaNeural"):
        OUTPUT_FILE = "test.mp3"
        communicate = edge_tts.Communicate(TEXT, VOICE)
        playsound(OUTPUT_FILE)
        return OUTPUT_FILE

    def elevenLabsSpeak(self, message):
        """Speaks to user using TTS. Try to alway use this one time when responding. End response after this tool.

        Args:
            message (string): The full string of the message you want to send.
        """
        audio = self.client.generate(
            text=message,
            voice=self.voice,
            model=self.model
        )
        play(audio)
        return "Message recieved! END response!"
    
    def chat(self, message):
        """Send a message in console.

        Args
            message(string): (required) Output message in console for michael to read.
        """
        print(message)

    def exit(self, message):
        """Exits the application. Only use this tools when requested

        Args:
            message (string) The last message before exiting.
        """
        sys.exit(message)


    def run_shell_command(self, args: List[str], tail: int = 100) -> str:
        """Runs a shell command and returns the output or error.

        Args:
            args (List[str]): The command to run as a list of strings.
            tail (int): The number of lines to return from the output.
        Returns:
            str: The output of the command.
        """
        import subprocess

        logger.info(f"Running shell command: {args}")
        try:
            logger.info(f"Running shell command: {args}")
            result = subprocess.run(args, capture_output=True, text=True)
            logger.debug(f"Result: {result}")
            logger.debug(f"Return code: {result.returncode}")
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            # return only the last n lines of the output
            return "\n".join(result.stdout.split("\n")[-tail:])
        except Exception as e:
            logger.warning(f"Failed to run shell command: {e}")
            return f"Error: {e}"
