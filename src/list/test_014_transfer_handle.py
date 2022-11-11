# encoding=utf-8

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest


class Test_transfer_handle:
    @allure.description("转单审核")
    @allure.suite('转单通过')
    @allure.title("转单通过")  # 测试用例的标题
    @allure.testcase('/api/fsm-platform/operation/handle')
    @pytest.mark.two
    def test_transfer_handle(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/api/fsm-platform/operation/handle"
        result = ('FSMWOS02', 0, 1, 'FSMROS03', 'WAIT_OUTLETS_CONFIRM')
        appointment = Read_sql_Data.Conte(transfer_handle)

        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N1cHBsaWVyOmZzbV9zdXBwbGllcl9zZWNyZXQ=",
        }
        datas = {
            "approvalState": "PASS",
            "operationType": "TRANSFER_ORDER_APPROVAL",
            "processedTaskId": appointment[0][1],
            "remark": "通过转单申请",
            "transferOrderApplyId": appointment[0][2],
            "workOrderId": appointment[0][0],
        }
        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(transfer_result % appointment[0][0])
        assert result == appointment2[0]

    @allure.description("转单审核")
    @allure.suite('转单拒绝')
    @allure.title("转单拒绝")  # 测试用例的标题
    @allure.testcase('/api/fsm-platform/operation/handle')
    @pytest.mark.two
    def test_transfer_handle2(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/handle"
        result = ('FSMWOS02', 0, 1, 'FSMROS03', 'DISPATCH_ORDER')
        appointment = Read_sql_Data.Conte(transfer_handle)

        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N1cHBsaWVyOmZzbV9zdXBwbGllcl9zZWNyZXQ=",
        }
        datas = {
            "approvalState": "REJECT",
            "operationType": "TRANSFER_ORDER_APPROVAL",
            "processedTaskId": appointment[0][1],
            "remark": "拒绝转单申请",
            "transferOrderApplyId": appointment[0][2],
            "workOrderId": appointment[0][0],
        }
        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(transfer_result % appointment[0][0])
        assert result == appointment2[0]
