# encoding=utf-8
from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest

class Test_platform_operation:
    def sets_up(self):
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/order"
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.headers = {
            "r-auth": self.token,
            "Content-Type": "application/json"
        }
        self.text = '平台处理异常单'
        self.operation_order = Read_sql_Data.Conte(platform_rework)
    @allure.description("返工至网点")
    @allure.suite('返工至网点')
    @allure.title("返工至网点")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/order')
    @pytest.mark.two
    def test_rework(self):
        self.sets_up()
        data = {
            "workOrderId": self.operation_order[0][1],
            "requestOrderId": self.operation_order[0][0],
            "operationType": "REWORK",
            "remark": self.text
        }
        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
        assert res.status_code == 200
        log_show(res, data)
        sql_check_rework = Read_sql_Data.Conte(check_platform_rework % self.operation_order[0][1])
        assert sql_check_rework == [('FSMROS01','FSMWOS02','ABNOPT01',self.text,'FSMWOS02','FSMROS01','DISPATCH_ORDER','FSMIOS01')]

    @allure.description("平台协商完成")
    @allure.suite('平台协商完成')
    @allure.title("平台协商完成")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/order')
    @pytest.mark.two
    def test_negotiate_complete(self):
        self.sets_up()
        data = {
            "workOrderId": self.operation_order[0][1],
            "requestOrderId": self.operation_order[0][0],
            "operationType": "NEGOTIATE_COMPLETE",
            "remark": self.text
        }
        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
        assert res.status_code == 200
        log_show(res, data)
        sql_check_rework = Read_sql_Data.Conte(check_platform_rework % self.operation_order[0][1])
        check_condition = Read_sql_Data.Conte(sql_check_condition + "(%s)" % str(self.operation_order[0][0]))
        if len(check_condition) > 0:
            if check_condition[0][0] == 'ACTUAL_QUOTE':
                check_condition = 'ORDER_COMPLETE'
            else:
                check_condition = 'ACTUAL_QUOTE'
        else:
            check_condition = 'ORDER_COMPLETE'
        print(check_condition)
        assert sql_check_rework == [
            ('FSMROS04','FSMWOS04','ABNOPT02','异常单处理','FSMWOS05','FSMROS04',check_condition,'FSMIOS03')]