# encoding=utf-8

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest


class Test_transfer_order:

    @allure.description("转单")
    @allure.suite('转单申请')
    @allure.title("转单申请")  # 测试用例的标题
    @allure.testcase('/api/fsm-platform/operation/handle')
    @pytest.mark.two
    def test_transfer_order(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/handle"
        result = ('FSMWOS02', 0, 1, 'FSMROS03','DISPATCH_ORDER')
        appointment = Read_sql_Data.Conte(transfer_order)
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N1cHBsaWVyOmZzbV9zdXBwbGllcl9zZWNyZXQ=",
        }
        datas = {
            "operationType": "TRANSFER_ORDER_APPLY",
            "remark": "忙不过来，申请转单",
            "workOrderId": appointment[0][0]
        }
        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(transfer_result % appointment[0][0])
        assert result == appointment2[0]



