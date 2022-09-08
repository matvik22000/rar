from eschool.eschool_server import EschoolServer
from db.database import Database
from firebase.firebase_user import FirebaseUser
from exceptions.http_exceptions import *


def login(firebase_id: str, username: str, password: str, ver: str, db: Database, eschool: EschoolServer):
    db.connect()
    user: FirebaseUser = FirebaseUser(username, password, eschool, firebase_id)
    try:
        user.auth()
        db.update_pw_relevance(True, user.username)
    except EschoolAuthorisationException:
        db.update_pw_relevance(False, user.username)

    user.state()
    if not db.is_in_db(firebase_id):
        db.add_user(user)
    else:
        db.update_user(user, ver)
    db.commit()

