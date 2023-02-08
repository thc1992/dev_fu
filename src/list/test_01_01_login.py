# encoding=utf-8
import pytest

from src.base.request_Control import *
import allure

from src.read_yaml.read_yaml import Read_yaml

user_name = Read_yaml().yaml_show('login')['user_name']
pwd = Read_yaml().yaml_show('passwd', 'token.yaml')
host = Read_yaml().yaml_show('host')
baseUrl = host + '/rdp-auth/oauth/token'

class Test_login(object):
    @allure.description("验证登录")
    @allure.suite('登录')
    @allure.title("正常登录")  # 测试用例的标题
    @allure.testcase('/rdp-auth/oauth/token')
    @pytest.mark.one
    def test_regular_login(self):
        self.result = get_token(user_name,pwd, baseUrl)
        assert "access_token" in self.result.json()

        json_str = {'access_token': self.result.json()['access_token'],
                    'passwd': pwd
                    }
        Read_yaml().write_yaml(json_str)

    @allure.description("验证登录")
    @allure.suite('登录')
    @allure.title("异常登录")  # 测试用例的标题
    @allure.testcase('/api/rdp-auth/oauth/token')
    @pytest.mark.three
    def test_err_login(self):
        result = get_token(user_name, 'derfu365CO', baseUrl)
        code = result.json()['code']
        mess = result.json()['message']
        assert code == 400
