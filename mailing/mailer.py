from threading import Thread

from db.database import Database
from eschool.eschool_server import EschoolServer
from .marks.mail_marks import mail_marks
from .msgs.mail_msgs import mail_msgs
from . import log


class Mailer(Thread):
    def __init__(self, limit: int, offset: int, eschool: EschoolServer):
        Thread.__init__(self)
        self.db = Database(eschool)
        self.limit: int = limit
        self.offset: int = offset
        self.name: str = f' #{offset}-{offset + limit} '

    def run(self):
        log.info(f'mailing {self.name}')

        mail_msgs(self.offset, self.limit, self.db)
        log.warn(f'msgs mailed; mailing marks {self.name}')

        mail_marks(self.offset, self.limit, self.db)
        log.warn(f'completed {self.name}')
