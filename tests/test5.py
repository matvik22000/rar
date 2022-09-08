import requests

r = requests.get(url='http://shproj2020.herokuapp.com/login', params={"username": "Matvey_gurov",
                                                            "password": "078e2f311f5a55569a07640db1bb06ef636b410459ba78d89f4cc1eb406c413"})
data = {"classNumber": "208",
        "teacherId": 69908,
        "reason": "123test123",
        "startTime": 1586969353834,
        "endTime": 1586969359834,
        "daysCount": 10,
        "daysOfWeek": [1, 0, 0, 1, 0, 1, 0]}
r2 = requests.post(url='http://shproj2020.herokuapp.com/reserve_period', data=data, cookies=r.cookies)
print(r2.text)
print(r2.status_code)
