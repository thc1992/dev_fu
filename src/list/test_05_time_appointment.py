# encoding=utf-8
import json
import pytest

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
from src.base.time_tools import *

token = Read_yaml().yaml_show('access_token', 'token.yaml')
url_use = Read_yaml().yaml_show('host') + "/fsm-platform/taskOrder/appointTime"
result12 = ('FSMROS02', 'FSMWOS03', 'FSMROS02', 'WAIT_SIGN_IN', 'FSMIOS01', 'FSMTOS02')
tim = Time_tools().get_time()


class Test_time_appointment:
    @allure.description("预约时间")
    @allure.suite('工程师预约时间')
    @allure.title("工程师预约时间")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/appointTime')
    @pytest.mark.one
    def test_appointment(self):

        self.nomal_report = Read_yaml().yaml_show('nomal_report')

        if self.nomal_report:
            self.appointment = Read_sql_Data.Conte(task_order_show % Read_yaml().yaml_show('workOrderId', 'token.yaml'))
        else:
            self.appointment = Read_sql_Data.Conte(time_app)
        headers = {
            "r-auth": token,
            "Content-Type": "application/json",
            "r-idempotent": r_idempotent(token, "workOrder"),
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA=="
        }
        datas = {
            "appointmentDate": str(time.strftime("%Y-%m-%d")),
            "appointmentTime": str(tim) + ':00-' + str(tim + 2) + ':00',
            "taskOrderIds":
                [str(self.appointment[0][0])]

        }
        res = requests.post(url=url_use, json=datas, headers=headers)
        log_show(res, datas)

        assert res.json()['code'] == 200
        name = "(%s)" % str(self.appointment[0][0])
        sql_check = time_app_check % name

        list_sql_check = Read_sql_Data.Conte(sql_check)
        assert list_sql_check[0] == result12

    @allure.description("预约时间")
    @allure.suite('批量预约时间')
    @allure.title("批量预约时间")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/appointTime')
    @pytest.mark.two
    def test_more_appointment(self):
        self.appointment = Read_sql_Data.Conte(time_app)
        assert len(self.appointment) > 1
        more_appointment = str(self.appointment[0][0]), str(self.appointment[1][0])
        headers = {
            "r-auth": token,
            "Content-Type": "application/json",
            "r-idempotent": r_idempotent(token, "workOrder"),
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA=="

        }
        datas = {
            "appointmentDate": str(time.strftime("%Y-%m-%d")),
            "appointmentTime": str(tim) + ':00-' + str(tim + 2) + ':00',
            "taskOrderIds":
                [
                    *more_appointment
                ]
        }
        res = requests.post(url=url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200

        sql_check = time_app_check % str(more_appointment)
        # print(sql_check)
        list_sql_check = Read_sql_Data.Conte(sql_check)
        for i in range(0, len(list_sql_check)):
            assert list_sql_check[i] == result12
