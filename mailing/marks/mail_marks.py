from threading import currentThread

from db.database import Database
from typing import *

from eschool.mark import Mark
from exceptions.http_exceptions import EschoolAuthorisationException, NoMarksException
from firebase.firebase_user import FirebaseUser
from exceptions.firebase_exceptions import *
from . import log


def mail_marks(offset: int, limit: int, db: Database):
    db.connect()
    users: List[FirebaseUser] = db.get_users(offset, limit, log)
    count = 0
    served = 0
    skipped = 0
    skipped_parents = 0
    for user in users:
        # log.debug(f'serving {user} {currentThread().name}')
        count += 1
        try:
            marks: List[Mark] = user.get_marks()
        except NoMarksException:
            log.debug(f'skipped {user.username} parent/teacher {currentThread().name}')
            skipped_parents += 1
            continue
        except EschoolAuthorisationException:
            db.update_pw_relevance(False, user.username)
            skipped += 1
            log.info(f'skipped {user} {currentThread().name} because of EschoolAuthorisationException')
            continue
        for mark in marks:
            if mark.isUpdated == "1":
                try:
                    user.send_mark(mark)
                except InvalidRegistrationException:
                    db.del_user(user.get_firebase_id(), user.prs_id, user.username)
                except NotRegisteredException:
                    db.del_user(user.get_firebase_id(), user.prs_id, user.username)

        served += 1
    log.info(
        f'served {served}; skipped {skipped}; skipped parents {skipped_parents} from {count} {currentThread().name}')
    db.commit()
