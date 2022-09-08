from typing import *
from threading import currentThread

from exceptions.http_exceptions import *
from .eschool_server import EschoolServer
from .mark import Mark
from . import log


def request(func):
    def wrapper(self, *args, **kwargs):
        if self.jsessionid == "" or self.route == "":
            raise UserNotAuthorised()
        if self.user_id == "" or self.prs_id == "":
            raise WrongUserInfoException()
        # double request is using because cookies from database may be past due
        # auth() method is tying to authorise user via his username and password
        # if request fails second time, password is wrong
        try:
            try:
                return func(self, *args, **kwargs)
            except IncorrectCookieException:
                self.auth()
                return func(self, *args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            log.critical(f'connection error {currentThread().name} {e}')

    return wrapper


class EschoolUser:
    def __init__(self, username: str, password: str, server: EschoolServer, route: str, jsessionid: str, prs_id: str,
                 user_id: str):
        self.username = username
        self.password = password
        self.eschool_server: EschoolServer = server
        self.route, self.jsessionid = route, jsessionid
        self.cookies = {"route": self.route, "JSESSIONID": self.jsessionid}
        self.prs_id: str = prs_id
        self.user_id: str = user_id

    def auth(self) -> None:
        self.route, self.jsessionid = self.eschool_server.login(self.username, self.password)
        self.cookies = {"route": self.route, "JSESSIONID": self.jsessionid}

    def state(self) -> None:
        if self.jsessionid == "" or self.route == "":
            raise UserNotAuthorised()
        state = self.eschool_server.get_state(self.cookies)
        self.prs_id = state["user"]["prsId"]
        self.user_id = state["user"]["userId"]

    @request
    def get_marks(self) -> List[Mark]:
        marks = self.eschool_server.get_marks(self.user_id, self.cookies)
        return marks

    @request
    def get_new_msgs(self) -> List[dict]:
        msgs = self.eschool_server.get_new_msgs(self.cookies, self.prs_id)
        return msgs

    @request
    def read_msg(self, msg_id: str) -> None:
        self.eschool_server.read_msg(msg_id, self.cookies)

    @request
    def get_school_clazz(self) -> Tuple[str, str]:
        return self.eschool_server.get_school_clazz(self.prs_id, self.cookies)

    def get_user_info(self) -> dict:
        if self.user_id == "" or self.prs_id == "":
            raise WrongUserInfoException

        return {"userId": self.user_id, "prsId": self.prs_id}

    def get_username(self) -> str:
        return self.username

    def get_password(self) -> str:
        return self.password

    def get_cookies(self) -> Dict[str, str]:
        if self.jsessionid == "" or self.route == "":
            raise UserNotAuthorised()

        return self.cookies
