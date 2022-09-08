import json
import custom_logger

# requires eschool, firebase
NAME = "db"


class DatabaseCredentials:
    def __init__(self, credentials: dict):
        self.host = credentials["host"]
        self.database = credentials["database"]
        self.user = credentials["user"]
        self.port = credentials["port"]
        self.password = credentials["password"]


filename = f'{__file__.replace("__init__.py", "")}credentials.json'
with open(filename, 'r') as f:
    obj = json.load(f)
    credentials = DatabaseCredentials(obj)

log = custom_logger.get_my_logger(NAME)
