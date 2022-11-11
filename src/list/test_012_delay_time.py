# encoding=utf-8

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest


class Test_delay_time:
    @allure.description("延迟审核")
    @allure.suite('延迟拒绝')
    @allure.title("延迟拒绝")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/delayApproval')
    @pytest.mark.two
    def test_delay(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/delayApproval"
        result = ('FSMWOS03', 'FSMWOSCS04', 'FSMROS02', 'REJECT', 'FSMWOS03', 'FSMROS02', 'FSMIOS01')
        appointment = Read_sql_Data.Conte(delay)
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
            "r-idempotent": r_idempotent(self.token, "delayApproval")

        }
        datas = {"operationType": "REJECT",
                 "remark": "我拒绝你的延迟申请",
                 "requestOrderId": appointment[0][0],
                 "processedTaskId": appointment[0][1]
                 }
        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(delay_state % appointment[0][0])
        assert result == appointment2[0]

    @allure.description("延迟审核")
    @allure.suite('延迟通过')
    @allure.title("延迟通过")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/delayApproval')
    def test_delay2(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/delayApproval"
        result = ('FSMWOS03', 'FSMWOSCS04', 'FSMROS02', 'PASS', 'FSMWOS03', 'FSMROS02', 'FSMIOS01')
        appointment = Read_sql_Data.Conte(delay)
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
            "r-idempotent": r_idempotent(self.token, "delayApproval")

        }
        datas = {"operationType": "PASS",
                 "remark": "我通过你的延迟申请",
                 "requestOrderId": appointment[0][0],
                 "processedTaskId": appointment[0][1]
                 }
        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(delay_state % appointment[0][0])
        assert result == appointment2[0]
