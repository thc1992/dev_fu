# encoding=utf-8

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest


class Test_cancel_quote:
    @allure.description("取消报价审核")
    @allure.suite('取消报价')
    @allure.title("取消报价")  # 测试用例的标题
    @allure.testcase('/fsm-platform/fee/actual/quote/cancel')
    @pytest.mark.two
    def test_cancel_quote(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/fee/actual/quote/cancel"
        result = ('N', 'CANCEL', 'HAS_QUOTE', 0)
        appointment = Read_sql_Data.Conte(cancle_quote)
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
        }
        datas = {
            "quoteId": appointment[0][0]
        }
        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(cancle_quote_check % appointment[0][0])
        assert result == appointment2[0]
