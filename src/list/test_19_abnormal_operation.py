# encoding=utf-8
from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest


class Test_operation_order:
    def sets_up(self):
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/order"
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.headers = {
            "r-auth": self.token,
            "Content-Type": "application/json"
        }
        self.text = '异常单处理'
        self.operation_order = Read_sql_Data.Conte(operation_order)

    @allure.description("返工")
    @allure.suite('返工')
    @allure.title("返工")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/order')
    @pytest.mark.two
    def test_rework(self):
        self.sets_up()
        self.list_sql_search = Read_sql_Data.Conte(rework_user % self.operation_order[0][1])
        self.user_id = self.list_sql_search[0][1]
        data = {
            "workOrderId": self.operation_order[0][1],
            "requestOrderId": self.operation_order[0][0],
            "operationType": "SUPPLIER_REWORK",
            "engineerId": self.user_id,
            "remark": self.text
        }
        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
        assert res.status_code == 200
        log_show(res, data)
        sql_check_rework = Read_sql_Data.Conte(check_rework % self.operation_order[0][1])
        assert sql_check_rework == [(
            'FSMROS02', 'FSMWOS03', 'ABNOPT04', self.text, 'FSMWOS03', 'FSMROS02', 'APPOINT_TIME', 'FSMIOS01', 'FSMTOS01',self.user_id)]

# TURN_TO_PLATFORM 提交至平台
    @allure.description("提交至平台")
    @allure.suite('提交至平台')
    @allure.title("提交至平台")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/order')
    @pytest.mark.two
    def test_turn_to_platform(self):
        self.sets_up()
        data = {
            "workOrderId": self.operation_order[0][1],
            "requestOrderId": self.operation_order[0][0],
            "operationType": "TURN_TO_PLATFORM",
            "remark": self.text
        }
        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
        assert res.status_code == 200
        log_show(res, data)
        sql_check_turn_to_platform = Read_sql_Data.Conte(check_turn_to_platform % self.operation_order[0][1])
        assert sql_check_turn_to_platform == [(
            'FSMROS02','FSMWOS05','ABNOPT02',self.text,'FSMWOS05','FSMROS02','PLATFORM_ARBITRATION','FSMIOS05')]

# ENGINEER_NEGOTIATE_COMPLETE 协商完成
    @allure.description("服务商协商完成")
    @allure.suite('服务商协商完成')
    @allure.title("服务商协商完成")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/order')
    @pytest.mark.two
    def test_engineer_negotiate_complete(self):
        self.sets_up()
        data = {
            "workOrderId": self.operation_order[0][1],
            "requestOrderId": self.operation_order[0][0],
            "operationType": "ENGINEER_NEGOTIATE_COMPLETE",
            "remark": self.text
        }
        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
        assert res.status_code == 200
        log_show(res, data)
        sql_check_negotiate_complete = Read_sql_Data.Conte(check_negotiate_complete % self.operation_order[0][1])
        assert sql_check_negotiate_complete == [('FSMROS03','FSMWOS03','ABNOPT03',self.text,'FSMWOS03','FSMROS03','WAIT_CONFIRM','FSMIOS01')]