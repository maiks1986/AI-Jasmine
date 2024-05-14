from dotenv import set_key
from pathlib import Path

class EnvWriter:
    def __init__(self):
        self.env_file_path = Path(".env")
    # Create the file if it does not exist.
        self.env_file_path.touch(mode=0o600, exist_ok=True)
    # Save some values to the file.
    def write(self,key, value):
        set_key(dotenv_path=self.env_file_path, key_to_set=str(key).upper(), value_to_set=value)