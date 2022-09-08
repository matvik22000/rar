from typing import *
from threading import currentThread
from db.database import Database
from exceptions.firebase_exceptions import *
from firebase.firebase_user import FirebaseUser
from exceptions.http_exceptions import *
from . import log


def mail_msgs(offset: int, limit: int, db: Database):
    db.connect()
    users: List[FirebaseUser] = db.get_users(offset, limit, log)
    count = 0
    served = 0
    skipped = 0
    for user in users:
        count += 1
        # log.debug(f'serving {user} {currentThread().name}')
        try:
            msgs: List[Dict] = user.get_new_msgs()
        except EschoolAuthorisationException:
            db.update_pw_relevance(False, user.username)

            log.info(f'skipped {user} {currentThread().name} because of EschoolAuthorisationException')
            skipped += 1
            continue
        for msg in msgs:
            try:
                user.send_msg(msg)
            except NotRegisteredException:
                db.del_user(user.get_firebase_id(), user.prs_id, user.username)
            except InvalidRegistrationException:
                db.del_user(user.get_firebase_id(), user.prs_id, user.username)

        served += 1
    log.info(f'served {served}; skipped {skipped} from {count} {currentThread().name}')
    db.commit()
