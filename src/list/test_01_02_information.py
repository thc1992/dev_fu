# encoding=utf-8
import pytest

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml

class Test_information(object):
    @allure.description("修改个人信息")
    @allure.suite('个人信息')
    @allure.title("个人信息")  # 测试用例的标题
    @allure.testcase('/rdp-system/user/submit')
    @pytest.mark.three
    def test_info(self):
        self.user_name = Read_yaml().yaml_show('login')['user_name']
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/rdp-system/user/submit"
        self.user_meg = Read_sql_Data.Conte(user_info + "'%s'" % str(self.user_name))

        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
        }
        datas = {
            "id": self.user_meg[0][0],
            "account": self.user_name,
            "realName": "小唐",
            "email": "123@qq.com",
            "phone": self.user_name
        }
        res = request_all(self.url_use, datas, headers)

        parm = (
            int(res.json()['data']['id']), "%s" % res.json()['data']['realName'], "%s" % res.json()['data']['email'])
        # print(parm)
        user_info1 = Read_sql_Data.Conte(user_info + "'%s'" % str(self.user_name))
        # print(user_info[0])
        assert parm == user_info1[0]
