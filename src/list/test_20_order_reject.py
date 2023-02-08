# encoding=utf-8

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest
class Test_order_reject:
    @allure.description("工程师拒绝")
    @allure.suite('拒绝工单')
    @allure.title("拒绝工单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/reject')
    @pytest.mark.two
    def test_order_reject(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/taskOrder/reject"
        result = ('FSMTOS03', 'FSMTOS03', 'FSMWOS02')
        appointment = Read_sql_Data.Conte(return_reject)
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
        }
        datas = {
            "rejectReason": "来不急，需要另找人过去",
            "taskOrders": [appointment[0][0]]
        }
        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        list_sql_check = Read_sql_Data.Conte(check_return_reject % appointment[0][0])
        assert list_sql_check[0] == result
