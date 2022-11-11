# encoding=utf-8

import requests
import os

from src.file_case.allure_tools import log_show
from src.read_yaml.read_yaml import Read_yaml


def get_token(username, passwd, baseUIR, showlog=1):
    header = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Authorization': 'Basic ZnNtX3N0b3JlOmZzbV9zdG9yZV9zZWNyZXQ=',
    }
    datas = {
        'password': passwd,
        'username': username,
        'grant_type': 'password',
        'scope': 'all'
    }
    res = requests.post(baseUIR, data=datas, headers=header)
    log_show(res, datas, showlog)
    return res


def r_idempotent(token, order):
    """

    :param token: 每次请求都要传递
    :param order: 去重验证每个接口的值不同
    :return: 返回
    """
    url = Read_yaml().yaml_show('host') + "/fsm-platform/requestOrder/generate"
    headers = {
        "r-auth": token,
        "Content-Type": "application/json"
    }
    data = {
        "key": order
    }
    res = requests.get(url=url, headers=headers, params=data)
    log_show(res, data)
    return res.json()['data']


def get_image(path, token):
    """
    "上传图片接口"
    path:图片路径
    token:请求r-auth值
    """
    url = Read_yaml().yaml_show('host') + "/rdp-system/file/endpoint/put-file"
    headers = {
        "r-auth": token,
    }
    datas = {
        'file': ('city.jpg', path, 'image/jpg')
    }
    res = requests.post(url, files=datas, headers=headers)
    return res


def request_all(url_use, datas, headers, showlog=1):
    res = requests.post(url=url_use, json=datas, headers=headers)
    log_show(res, datas, showlog)
    return res

# token = Read_yaml().yaml_show('access_token', 'token.yaml')
# print(r_idempotent(token, "requestOrder"))
# token = Read_yaml().yaml_show('access_token', 'token.yaml')
# r_idempotent(token, "delayApproval")