from datetime import datetime
from json import loads

from requests import get, post, put, delete

URL = "http://127.0.0.1:8001"
URL_LIMITS = f"{URL}/limits"
URL_TRANSFER = f"{URL}/transfers"


def del_id(data):
    for d in data:
        if "id" in d:
            del d["id"]
    return data


def test_post():
    data = [
        {
            "country": "RUS",
            "cur": "EUR",
            "amount": 1000
        },
    ]

    assert loads(delete(URL_LIMITS, json=data).text)["status"] == 200
    start_value = del_id(loads(get(URL_LIMITS).text))
    assert loads(post(URL_LIMITS, json=data).text)["status"] == 200

    start_value.extend(data)
    assert sorted(del_id(start_value), key=lambda x: str(x)) == \
           sorted(del_id(loads(get(URL_LIMITS).text)), key=lambda x: str(x))


def test_put():
    data_post = [
        {
            "country": "RUS",
            "cur": "EUR",
            "amount": 1000
        },
    ]
    data_put = [
        {
            "country": "RUS",
            "cur": "EUR",
            "amount": 2000
        },
    ]

    assert loads(delete(URL_LIMITS, json=data_post).text)["status"] == 200
    start_value = del_id(loads(get(URL_LIMITS).text))
    assert loads(post(URL_LIMITS, json=data_post).text)["status"] == 200
    assert loads(put(URL_LIMITS, json=data_put).text)["status"] == 200
    start_value.extend(data_put)
    assert sorted(del_id(start_value), key=lambda x: str(x)) == \
           sorted(del_id(loads(get(URL_LIMITS).text)), key=lambda x: str(x))


def test_delete():
    data = [
        {
            "country": "RUS",
            "cur": "EUR",
            "amount": 3000
        },
    ]

    assert loads(delete(URL_LIMITS, json=data).text)["status"] == 200
    start_value = del_id(loads(get(URL_LIMITS).text))
    assert loads(post(URL_LIMITS, json=data).text)["status"] == 200
    assert loads(delete(URL_LIMITS, json=data).text)["status"] == 200
    assert del_id(start_value) == del_id(loads(get(URL_LIMITS).text))


def test_transfer():
    data_limit = [
        {
            "country": "RUS",
            "cur": "EUR",
            "amount": 10000
        },
    ]

    assert loads(delete(URL_LIMITS, json=data_limit).text)["status"] == 200
    assert loads(post(URL_LIMITS, json=data_limit).text)["status"] == 200

    data_transfer = [
        {
            "date": datetime.now().strftime('%d/%m/%y %H:%M:%S'),
            "country": "RUS",
            "cur": "EUR",
            "amount": 5000
        },
    ]

    assert loads(post(URL_TRANSFER, json=data_transfer).text)["status"] == 200
    assert loads(post(URL_TRANSFER, json=data_transfer).text)["status"] == 200
    assert loads(post(URL_TRANSFER, json=data_transfer).text)["status"] == 707
