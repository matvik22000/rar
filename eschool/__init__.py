import json
import custom_logger

# loading first


NAME = "eschool"


class EschoolConstants:
    def __init__(self, consts: dict):
        self.eiid: int = consts["eiid"]


filename = f'{__file__.replace("__init__.py", "")}constants.json'
with open(filename, 'r') as f:
    obj = json.load(f)
    constants = EschoolConstants(obj)

log = custom_logger.get_my_logger(NAME)
