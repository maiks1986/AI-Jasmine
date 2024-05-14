from dotenv import dotenv_values
class Log():
    def __init__(self):
        env = dotenv_values(".env")
        self.dl = env['DEBUG_LEVEL']

    def Info(self, message):
        if self.dl == 'INFO':
            print(message)
    
    def Warning(self, message):
        if self.dl == 'WARNING' or self.dl == 'INFO':
            print(message)
    
    def Error(self, message):
        if self.dl == 'ERROR' or self.dl == 'WARNING' or self.dl == 'INFO':
            print(message)