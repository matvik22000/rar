from threading import currentThread
from eschool.eschool_server import EschoolServer
from eschool.eschool_user import EschoolUser
from eschool.mark import Mark
from exceptions.firebase_exceptions import FirebaseNotInitedException
from .push import push
from . import log


class FirebaseUser(EschoolUser):
    def __init__(self, username: str, password: str, server: EschoolServer, firebase_id: str, route="", jsessionid="",
                 prs_id="", user_id=""):
        super().__init__(username, password, server, route, jsessionid, prs_id, user_id)
        self.firebase_id = firebase_id

    def push(self, data: dict):
        if self.firebase_id == "":
            raise FirebaseNotInitedException()
        push(self.firebase_id, data)

    def get_firebase_id(self) -> str:
        return self.firebase_id

    def send_msg(self, msg: dict):
        try:
            message = msg["msg"][:500]
        except KeyError:
            message = ""
        try:
            subject = msg["subject"]
        except KeyError:
            subject = ""
        try:
            files = msg["attachInfo"]
        except KeyError:
            files = []

        count = int(self.eschool_server.get_members_count(self.cookies, msg["threadId"]))
        data = {"type": "msg",
                "text": message,
                "senderId": msg["senderId"],
                "senderFio": msg["senderFio"],
                "threadId": msg["threadId"],
                "date": msg["sendDate"],
                "subject": subject,
                "attachInfo": files,
                "addrCnt": count
                }

        self.read_msg(msg["msgId"])
        # log.info(f'read msg {msg["msgId"]} {currentThread()}')
        log.info(f'pushing to msg {self.username} {currentThread().name}')
        self.push(data)

    def send_mark(self, mark: Mark) -> None:
        body = {"type": "mark", "val": mark.markVal, "coef": mark.mktWt, "unitId": mark.unitId,
                "event": "new"}
        log.info(f'pushing to mark {self.username} {currentThread().name}')
        self.push(body)

    def __repr__(self):
        return self.username
