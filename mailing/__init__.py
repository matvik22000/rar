import json
import custom_logger

NAME = "mailing"


# requires eschool, db, firebase
class MailConfig:
    def __init__(self, config: dict):
        self.users_on_thread: int = int(config["users_on_thread"])


filename = f'{__file__.replace("__init__.py", "")}config.json'
with open(filename, 'r') as f:
    obj = json.load(f)
    config = MailConfig(obj)

log = custom_logger.get_my_logger(NAME)
