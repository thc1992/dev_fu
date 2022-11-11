# encoding=utf-8
import json

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
from src.base.time_tools import *
import pytest


class Test_signIn_Check:
    @allure.description("签到")
    @allure.suite('工程师签到')
    @allure.title("工程师签到")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/signIn')
    @pytest.mark.one
    def test_signIn(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/taskOrder/signInCheck"
        self.url_sign = Read_yaml().yaml_show('host') + "/fsm-platform/taskOrder/signIn"
        self.sign_sta = ('Y', 'FSMROS02', 'FSMWOS03', 'FSMWOS03', 'FSMROS02', 'IN_SERVICE', 'FSMIOS01', 'FSMTOS02')
        self.tim = Time_tools().get_time()
        self.nomal_report = Read_yaml().yaml_show('nomal_report')
        if self.nomal_report:
            self.appointment = Read_sql_Data.Conte(task_order_show % Read_yaml().yaml_show('workOrderId', 'token.yaml'))
        else:
            self.appointment = Read_sql_Data.Conte(sign)

        name = long_lat % self.appointment[0][1]
        sign_stau = sign_staus % self.appointment[0][1]
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA=="
        }
        data = {
            "requestOrderId": self.appointment[0][1],
            "taskOrderIds":
                [
                    self.appointment[0][0]
                ]
        }

        res1 = requests.post(url=self.url_use, json=data, headers=headers)
        assert res1.json()['code'] == 200

        datas = {"requestOrderId": self.appointment[0][1],
                 "taskOrderIds": [self.appointment[0][0]],
                 "latitude": Read_sql_Data.Conte(name)[0][1],
                 "longitude": Read_sql_Data.Conte(name)[0][0]
                 }

        res = requests.post(url=self.url_sign, json=datas, headers=headers)
        assert res.json()['code'] == 200
        log_show(res, datas)
        assert self.sign_sta == Read_sql_Data.Conte(sign_stau)[0]
