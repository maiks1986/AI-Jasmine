from typing import List
from phi.tools import Toolkit
from phi.utils.log import logger
from dotenv import dotenv_values

import ollama, urllib.request, json 

class OllamaToolkit(Toolkit):
    def __init__(self):
        env = dotenv_values(".env")
        super().__init__(name="ollama_toolkit")
        self.register(self.list_local_models)
        self.register(self.list_online_models)
        self.register(self.pull)
        self.register(self.show)
        self.register(self.ask)
    
    def list_local_models(self):
        """List Ollama models that are available locally.
        Args:
            None
        Returns:
            str: Ollama models that are available locally.
        """
        list = json.dumps(ollama.list())
        return list

    def list_online_models(self):
        """List Ollama models that are available online.
        """
        req = urllib.request.Request(
            url='http://ollama-models.zwz.workers.dev', 
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        with urllib.request.urlopen(req) as f:
            r_string = f.read().decode('utf-8')
            data = json.loads(r_string)
            models = []
            for model in data["models"]:
                for tag in model["tags"]:
                    models.append({"model": model["name"]+":"+tag,
                                "description": model["description"]}) 
        return models

    def show(self, name):
        """Show information about a model including details, modelfile, template, parameters, license, and system prompt.

        Args
            name(string): name of the model to show
        """
        return ollama.show(name.lower())
    
    def pull(self, name):
        """Download a model from the ollama library. 

        Args
            name(string): name of the model to pull. Example mistral:7b like they are found in list_online_models tool
        """
        return ollama.pull(name.lower())
    
    def ask(self, name, question, format = '', options = None, stream = False, keep_alive = None ):
        """Generate the next message in a chat with a provided model. This is a streaming endpoint, so there will be a series of responses. Streaming can be disabled using "stream": false. The final response object will include statistics and additional data from the request.

        Args
            name(string): (required) the Ollama model name from list_local_models()
            format(string): (optional) the format to return a response in. Currently the only accepted value is json
            options(string): (optional) additional model parameters listed in the documentation for the Modelfile such as temperature
            stream(boolean): (optional) if false the response will be returned as a single response object, rather than a stream of objects
            keep_alive: (optional) controls how long the model will stay loaded into memory following the request (default: 5m)
            question(json): (required) the messages of the chat, this can be used to keep a chat memory
                The message object has the following fields:
                    role(string): the role of the message, either system, user or assistant
                    content(string): the content of the message
                    images(string) :(optional) a list of images to include in the message (for multimodal models such as llava)

                Example for question
                    {
                        "role": "user",
                        "content": "why is the sky blue?"
                    },
                    {
                        "role": "assistant",
                        "content": "due to rayleigh scattering."
                    },
                    {
                        "role": "user",
                        "content": "how is that different than mie scattering?"
                    }
            """
        ollama.chat(model=name.lower(), messages=question, format=format, options=options, stream=stream, keep_alive=keep_alive)