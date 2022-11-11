# encoding=utf-8

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
import datetime
import pytest
from src.read_yaml.read_yaml import Read_yaml


class Test_delayed_fil:
    @allure.description("延迟申请")
    @allure.suite('延迟申请')
    @allure.title("延迟申请")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/delay')
    @pytest.mark.two
    def test_delayed(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/taskOrder/delay"
        result = (
            'FSMWOS03', 'FSMWOSCS04', 'FSMROS03', 'FSMROS03002', 'FSMWOS03', 'FSMROS03', 'FSMIOS01', 'N', 'FSMTT01')
        appointment = Read_sql_Data.Conte(delayed_fil)
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
        }
        datas = {
            "delayRemark": "忙过不来，来不及过去",
            "delayTime": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            "taskOrderIds": [appointment[0][0]]
        }
        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(delay_fil_state % appointment[0][1])
        assert result == appointment2[0]
