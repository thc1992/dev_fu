import requests
from src.list.test_login import *
from src.base.URL_link import *
import json
def test_r_idempotent():
    url = URL_link()
    url = url.BASE_URL+"/fsm-platform/requestOrder/generate?key=orderOperate"
    headers = {
        "r-auth": read_token(),
        "Content-Type": "application/json"
    }
    data={
        "key":"orderOperate"
    }
    res = requests.request(method="get", url=url, headers=headers, data=data)
    # print(res)
    if res.status_code == 200:
        r_idempotent = res.json()['data']
        print(res.json()['data'])
        return r_idempotent
    else:
        return None