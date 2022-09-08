import json
from typing import *
from threading import currentThread

import requests

from . import constants, log
from exceptions.http_exceptions import HttpRequestException, EschoolAuthorisationException, IncorrectCookieException, \
    NoMarksException
from .mark import Mark


def check_status(r: requests.Response) -> None:
    if r.status_code == 401:
        raise IncorrectCookieException(r)
    elif r.status_code != 200:
        raise HttpRequestException(r)


# noinspection PyMethodMayBeStatic
class EschoolServer:
    def login(self, username: str, password: str) -> Tuple[str, str]:
        url_login = "https://app.eschool.center/ec-server/login"
        data = {"username": username, "password": password}
        r = requests.post(url_login, data=data)

        if r.status_code == 401:
            raise EschoolAuthorisationException()
        elif r.status_code != 200:
            raise HttpRequestException(r)

        route = str(r.cookies["route"])
        jsessionid = str(r.cookies["JSESSIONID"])
        return route, jsessionid

    def get_state(self, cookies: dict) -> dict:
        url_state = "https://app.eschool.center/ec-server/state?menu=false"

        r = requests.get(url_state, cookies=cookies)
        check_status(r)

        return json.loads(r.text)

    def get_school_clazz(self, prs_id: str, cookies: dict):
        try:
            url_info = "https://app.eschool.center/ec-server/profile/" + str(prs_id) + "?date=1568999900392"
            r = requests.get(url_info, cookies=cookies)
            r = r.json()
            clazz_arr = r["result"]["movements"]["clazz"]
            clazz = clazz_arr[len(clazz_arr) - 1]["className"]
            school = clazz_arr[len(clazz_arr) - 1]["schoolNum"]
        except IndexError:
            clazz = "None"
            school = "None"

        return school, clazz

    def get_marks(self, user_id: str, cookies: dict) -> List[Mark]:
        url = "https://app.eschool.center/ec-server/student/getDiaryPeriod"

        r = requests.get(url + f'/?userId={user_id}&eiId={constants.eiid}', cookies=cookies)
        check_status(r)

        # parents and teachers don`t have this field
        # so I`ll just skip them
        try:
            lessons = json.loads(r.text)["result"]
        except KeyError:
            raise NoMarksException()
        marks = []

        for lesson in lessons:
            try:
                marks.append(Mark(lesson))
            except KeyError:
                pass
        return marks

    def get_new_msgs(self, cookies: dict, prs_id: str) -> List[dict]:
        new_only = "true"
        start_row = "1"
        rows_count = "100"
        url4 = f'https://app.eschool.center/ec-server/chat/count?prsId={prs_id}'

        r3 = requests.get(url4, cookies=cookies)
        check_status(r3)

        try:
            if int(r3.text) > 0:
                url = "https://app.eschool.center/ec-server/chat/threads?newOnly=%s&row=%s&rowsCount=%s" % (new_only,
                                                                                                            start_row,
                                                                                                            rows_count
                                                                                                            )
                r = requests.get(url, cookies=cookies)
                check_status(r)
                r = json.loads(r.text)
                url2 = "https://app.eschool.center/ec-server/chat/messages?getNew=%s&isSearch=%s&rowStart=%s" \
                       "&rowsCount=%s&threadId=%s" % (
                           "true", "false", "1", 1, r[0]["threadId"])

                r = requests.get(url2, cookies=cookies)
                check_status(r)

                ret = []

                for i in range(int(r3.text)):
                    ret.append(json.loads(r.text)[i])

                return ret
            return []
        except IndexError:
            return []

    def get_members_count(self, cookies: Dict, thread_id: str) -> int:
        url = "https://app.eschool.center/ec-server/chat/mem_and_cnt?threadId=%s" % thread_id
        r = requests.get(url, cookies=cookies)
        check_status(r)
        ans = json.loads(r.text)
        count = int(ans["addrCnt"])
        return count

    def read_msg(self, msg_id: str, cookies: dict) -> None:
        url = "https://app.eschool.center/ec-server/chat/readed?msgId=%s" % msg_id
        r = requests.get(url, cookies=cookies)
        check_status(r)
