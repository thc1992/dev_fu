# encoding=utf-8
from src.base.Access_token import *
import allure


class Test_login(object):
    @allure.description("验证登录")
    @allure.suite('登录')
    @allure.title("正常登录")  # 测试用例的标题
    @allure.testcase('/api/rdp-auth/oauth/token')
    def test_login(self):
        result = get_token('18810007982', 'derfu365COM1')
        if "access_token" in result.json():
            json_str = result.json()['access_token']
            assert json_str != ''
        else:
            mess = result.json()['message']
            print(mess)

    @allure.description("验证登录")
    @allure.suite('登录')
    @allure.title("异常登录")  # 测试用例的标题
    @allure.testcase('/api/rdp-auth/oauth/token')
    def test_err_login(self):
        result = get_token('17355538290', 'derfu365COM')
        code = result.json()['code']
        mess = result.json()['message']
        if code == 400:
            assert mess == '用户名或密码错误'
