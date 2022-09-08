from . import log
from threading import currentThread


class PushException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
        log.critical(f'push failed {msg} {currentThread()}')


class NotRegisteredException(PushException):
    def __init__(self) -> None:
        super().__init__("NotRegistered; maybe this user is 'dead'")


class InvalidRegistrationException(PushException):
    def __init__(self) -> None:
        super().__init__("InvalidRegistration; maybe this user is 'dead'")


class FirebaseNotInitedException(Exception):
    def __init__(self) -> None:
        super().__init__("Firebase was not inited for this user")
