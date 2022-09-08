import sys

sys.path.append("../")
sys.path.append("../db")
sys.path.append("../eschool")
sys.path.append("../exceptions")
sys.path.append("../firebase")
sys.path.append("../mailing")
sys.path.append("../server")


from mailing.mail import mail
import threading


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


set_interval(mail, 600)
# mail()
