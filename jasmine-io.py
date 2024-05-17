from Models.ioModel import IoModel
from phi.assistant import Assistant
class JasmineIO():
    def question(self, question, assistant = Assistant()):
        assistant.output_model=IoModel
        output = assistant.run(message=question,
                          stream=False,
                          )
        self.doNext(output)
        
    def doNext(self, output):
        output = IoModel()
        if output.useTool:
            output.useTool.tool(**output.useTool.arguments)
        if output.message:
            print(output.message)