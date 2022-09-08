import requests


class HttpRequestException(Exception):
    def __init__(self, response: requests.Response):
        msg = f'code: {response.status_code}; text: {response.text}'
        super().__init__(msg)


class EschoolAuthorisationException(Exception):
    def __init__(self):
        super().__init__("Wrong username or password")


class IncorrectCookieException(HttpRequestException):
    def __init__(self, r: requests.Response):
        super().__init__(r)


class UserNotAuthorised(Exception):
    def __init__(self) -> None:
        super().__init__("Please, call user.auth() method before")


class WrongUserInfoException(Exception):
    def __init__(self) -> None:
        super().__init__("user_id or prs_id are empty. Please, call use.state() method before")


class NoMarksException(Exception):
    def __init__(self) -> None:
        super().__init__("This user haven`t got any marks. Maybe he`s teacher or parent")
