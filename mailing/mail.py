from .mailer import Mailer
from eschool.eschool_server import EschoolServer
from db.database import Database
from . import config, log


def mail():
    print("starting")

    eschool: EschoolServer = EschoolServer()
    db: Database = Database(eschool)
    served_users = 0
    users_count = db.get_users_count()
    limit: int = config.users_on_thread

    print(f'starting mailing iteration for {users_count} with limit {limit}')
    log.warn(f'starting iteration for {users_count} with limit {limit}')

    while served_users < users_count:
        mailer = Mailer(limit, served_users, eschool)
        mailer.start()
        served_users += limit
