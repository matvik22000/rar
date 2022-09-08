import json
import custom_logger

NAME = "firebase"


# requires eschool
class FirebaseCredentials:
    def __init__(self, credentials: dict):
        self.key: str = credentials["key"]


filename = f'{__file__.replace("__init__.py", "")}credentials.json'
with open(filename, 'r') as f:
    obj = json.load(f)
    credentials = FirebaseCredentials(obj)

log= custom_logger.get_my_logger(NAME)
