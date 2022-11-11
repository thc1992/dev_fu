# encoding=utf-8
from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
import pytest
from src.read_yaml.read_yaml import Read_yaml


class Test_change_pwd:
    @allure.description("修改登录密码")
    @allure.suite('修改密码')
    @allure.title("修改密码")  # 测试用例的标题
    @allure.testcase('/rdp-system/user/submit')
    @pytest.mark.three
    def test_passwd(self):
        self.new_pwd = 'derfu365COM1'
        self.user_name = Read_yaml().yaml_show('login')['user_name']
        self.host = Read_yaml().yaml_show('host')
        self.baseUrl = self.host + '/rdp-auth/oauth/token'
        self.passwd = Read_yaml().yaml_show('passwd', 'token.yaml')

        self.url_use = Read_yaml().yaml_show('host') + "/rdp-system/user/update-password"
        self.user_meg = Read_sql_Data.Conte(user_info + "'%s'" % str(self.user_name))

        result = get_token(self.user_name, self.passwd, self.baseUrl, showlog=2)

        headers = {
            "r-auth": result.json()['access_token'],
            "Content-Type": "application/json",
        }
        datas = {"account": "", "oldPassword": self.passwd, "newPassword": self.new_pwd,
                 "newPasswordConfirm": self.new_pwd}

        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        result2 = get_token(self.user_name, self.new_pwd, self.baseUrl, showlog=1)
        print(result2.json())
        assert "access_token" in result2.json()

        # 修改读取的数据（k存在就修改对应值，k不存在就新增一组键值对）
        old_data = Read_yaml().read_yaml_all('token.yaml')  # 读取文件数据
        old_data['passwd'] = self.new_pwd
        Read_yaml().update_yaml(old_data, 'token.yaml')
