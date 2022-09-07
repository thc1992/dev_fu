from src.base.URL_link import *
import requests
import os

from src.file_case.allure_tools import allure_step_no, allure_step
from src.read_yaml.log_control import INFO, ERROR
from src.read_yaml.read_yaml import Read_yaml


def get_token(username, passwd):
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
    url = URL_link()
    res = requests.post(url.BASE_URL + url.LOGIN, data=datas, headers=header)

    if Read_yaml().yaml_show('is_run'):
        _log_msg = f"\n==========================================================================\n" \
                   f"请求路径: {res.request.url}\n" \
                   f"请求方式: {res.request.method}\n" \
                   f"请求头:   {res.request.headers}\n" \
                   f"请求内容: {datas}\n" \
                   f"接口响应内容: {res.text}\n" \
                   f"Http状态码: {res.status_code}\n" \
                   "================================================================================="
        if res.status_code == 200:
            """ 在allure中记录请求数据 """
            allure_step_no(f"请求URL: {res.request.url}")
            allure_step_no(f"请求方式: {res.request.method}")
            allure_step("请求头: ", res.request.headers)
            allure_step("请求数据: ", datas)
            allure_step("响应结果: ", res.text)
            INFO.logger.info(_log_msg)
        else:
            """ 在allure中记录请求数据 """
            allure_step_no(f"请求URL: {res.request.url}")
            allure_step_no(f"请求方式: {res.request.method}")
            allure_step("请求头: ", res.request.headers)
            allure_step("请求数据: ", datas)
            allure_step("响应结果: ", res.text)
            ERROR.logger.error(_log_msg)


        if ("access_token" in res.json()):
            json_str = {'access_token': res.json()['access_token']}
            Read_yaml().write_yaml(json_str)

    return res


def read_token():
    token = open(os.path.dirname(os.path.abspath(__file__)) + "/../../acess_token.txt", 'r')
    json_str = token.read().strip()
    if json_str != '':
        return json_str
    else:
        return None

# get_token('18810007982', 'derfu365COM')
# get_token('17355538290', 'derfu365COM')
#
# s = read_token()
# print(s)
