import json
from typing import List
from threading import currentThread
import psycopg2

from eschool.eschool_server import EschoolServer
from eschool.mark import Mark
from exceptions.database_exceptions import *
from firebase.firebase_user import FirebaseUser
from . import credentials, log


def requires_connection(func):
    def wrapper(self, *args, **kwargs):
        if self.conn is None or self.cur is None:
            raise ConnectionIsNull
        return func(self, *args, **kwargs)

    return wrapper


class Database:
    def __init__(self, eschool_server: EschoolServer):
        self.cur = None
        self.conn = None
        self.eschool_server = eschool_server

    def connect(self) -> None:
        conn = psycopg2.connect(
            database=credentials.database,
            user=credentials.user,
            password=credentials.password,
            host=credentials.host,
            port=credentials.port
        )
        self.conn = conn
        self.cur = conn.cursor()

    def commit(self) -> None:
        self.conn.commit()
        self.conn.close()

    def rollback(self) -> None:
        self.conn.rollback()
        self.conn.close()

    def insert_stat(self, msg: str, event: str, firebase_id: str) -> None:
        self.connect()
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO stat (firebase_id, event, msg, time) VALUES(%s, %s, %s, CURRENT_DATE)""", (
            firebase_id, event, msg
        ))
        self.commit()

    @requires_connection
    def add_user(self, user: FirebaseUser):
        firebase_id: str = user.get_firebase_id()
        username: str = user.get_username()
        password: str = user.get_password()
        user_info: dict = user.get_user_info()
        cookies: dict = user.get_cookies()
        school, clazz = user.get_school_clazz()
        self.cur.execute(
            """INSERT INTO users(firebase_id, username, pword, userinfo, cookie, clazz, lastentry, school, is_pw_actual)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE, %s, true)""",
            (
                firebase_id, username, password, json.dumps(user_info),
                json.dumps(cookies), clazz, school,
            ))

    @requires_connection
    def del_user(self, firebase_id: str, prs_id: str, username: str):
        # TODO add deleting
        log.warning(f'user {username} {prs_id} {firebase_id} deleted {currentThread().name}')
        self.cur.execute("DELETE FROM users WHERE firebase_id = %s", (
            firebase_id,
        ))
        self.cur.execute("DELETE FROM marks WHERE userid = %s", (
            firebase_id,
        ))
        self.cur.execute("DELETE FROM lessons WHERE userid = %s", (
            firebase_id,
        ))

    @requires_connection
    def insert_mark(self, user_mark: Mark, firebase_id: str) -> None:
        self.cur.execute(
            """INSERT INTO marks (markid, markdate, markvalid, mktwt, subject, teachfio, isupdated, userid, unitid, startdate,
                   lessonid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                user_mark.markId, user_mark.markDate, user_mark.markVal, user_mark.mktWt,
                user_mark.subject, user_mark.teachFio, user_mark.isUpdated, firebase_id, user_mark.unitId,
                user_mark.startDate, user_mark.lessonId
            ))

    def get_users_count(self) -> int:
        self.connect()
        self.cur.execute("""select count(*) from users""")
        ans = int(self.cur.fetchall()[0][0])
        self.conn.close()
        return ans

    @requires_connection
    def set_mark_updated(self, mark: Mark, firebase_id: str) -> None:
        self.cur.execute("""UPDATE marks SET isupdated = 0 WHERE userid = %s and markid = %s""", (
            firebase_id, mark.markId,
        ))

    @requires_connection
    def is_in_db(self, firebase_id: str) -> bool:
        self.cur.execute("""select count(*) from users where firebase_id = %s""", (
            firebase_id,
        ))
        return int(self.cur.fetchall()[0][0]) != 0

    @requires_connection
    def get_users(self, offset: int, limit: int, extended_logger) -> List[FirebaseUser]:
        self.cur.execute("""select * from users where is_pw_actual = true offset %s limit %s""", (
            str(offset), str(limit)
        ))
        users: List[FirebaseUser] = []
        rows = self.cur.fetchall()

        skipped = 0
        count = 0
        for row in rows:
            count += 1

            firebase_id = row[0]
            username = row[1]
            password = row[2]
            user_info = json.loads(row[3])
            cookie = json.loads(row[4])
            is_pw_relevant = row[9]

            if is_pw_relevant:
                # extended_logger.debug(f'{username} is added to array {currentThread().name}')
                user: FirebaseUser = FirebaseUser(username,
                                                  password,
                                                  self.eschool_server,
                                                  firebase_id,
                                                  route=cookie["route"],
                                                  jsessionid=cookie["JSESSIONID"],
                                                  prs_id=user_info["prsId"],
                                                  user_id=user_info["userId"]
                                                  )

                users.append(user)
            else:
                skipped += 1
                extended_logger.exception(f'skipped {username} because of is_pw_actual is false {currentThread().name}')

        log.info(f'got {count} of {limit} {currentThread().name}')
        return users

    @requires_connection
    def update_user(self, user: FirebaseUser, ver: str):
        school, clazz = user.get_school_clazz()

        self.cur.execute(
            """UPDATE users
                SET username  = %s,
                    pword     = %s,
                    userinfo  = %s,
                    cookie    = %s,
                    clazz     = %s,
                    ver       = %s,
                    lastentry = CURRENT_DATE,
                    school    = %s,
                    is_pw_actual = true
                WHERE firebase_id = %s""",
            (
                user.get_username(),
                user.get_password(),
                json.dumps(user.get_user_info()),
                json.dumps(user.get_cookies()),
                clazz,
                ver,
                school,
                # where
                user.get_firebase_id()
            ))

    @requires_connection
    def update_pw_relevance(self, is_pw_relevant: bool, username: str):
        self.cur.execute("""update users set is_pw_actual = %s where username = %s""", (
            str(is_pw_relevant), username,
        ))
        log.info(f'set is_pw_actual {is_pw_relevant} for {username}')

    def get_ver(self) -> str:
        self.connect()
        self.cur.execute("""SELECT * FROM ver""")
        rows = self.cur.fetchall()
        self.conn.close()
        return rows[0][0]
