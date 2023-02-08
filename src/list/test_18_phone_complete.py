# encoding=utf-8

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest

class Test_phone_complete:
    @allure.description("电话指导完成")
    @allure.suite('电话指导')
    @allure.title("电话指导")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/handle')
    @pytest.mark.two
    def test_phone_complete(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/handle"
        result = ('FSMWOS03', 'FSMWOSCS01', 'FSMROS03', 'FSMROS03003','WAIT_CONFIRM')
        appointment = Read_sql_Data.Conte(transfer_order)
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
        }
        datas = {
            "operationType": "PHONE_GUIDE_COMPLETE",
            "remark": "电话指导完成",
            "workOrderIds": [appointment[0][0]]
        }
        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(phone_results % appointment[0][0])
        assert result == appointment2[0]
