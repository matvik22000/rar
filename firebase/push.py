import json
import requests
from datetime import datetime

from exceptions.firebase_exceptions import *
from firebase import credentials
from exceptions.http_exceptions import HttpRequestException
from . import log


def push(address: str, data: dict) -> None:
    # 'notification': {'title': 'test', 'body': data}

    headers = {"Authorization": "key=" + credentials.key, "Content-Type": "application/json"}
    data = {
        "to": address,
        "data": data
    }
    r = requests.post("https://fcm.googleapis.com/fcm/send", data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        # {"multicast_id":2282221511986004670,"success":0,"failure":1,"canonical_ids":0,"results":[{"error":"InvalidRegistration"}]}
        response = json.loads(r.text)
        if response["failure"] == 1:
            if response["results"][0]["error"] == "NotRegistered":
                raise NotRegisteredException()
            elif response["results"][0]["error"] == "InvalidRegistration":
                raise InvalidRegistrationException()
            else:
                raise PushException(response["results"])

        log.info(f'{currentThread().name} pushed {data} successfully')
    else:
        raise HttpRequestException(r)


