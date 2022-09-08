import json
import logging


def get_my_logger(name):
    with open('../config.json', 'r') as f:
        config = json.load(f)

    # setup log
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f'{config["logger"]}', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s - %(filename)s:%(lineno)s]: %(message)s')
    file_handler.setFormatter(formatter)

    log.addHandler(file_handler)

    return log
