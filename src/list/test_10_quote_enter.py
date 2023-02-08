# encoding=utf-8

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest


class Test_quote_enter:
    @allure.description("报价审核")
    @allure.suite('审核通过')
    @allure.title("审核通过")  # 测试用例的标题
    @allure.testcase('/fsm-platform/fee/actual/quote/approval')
    @pytest.mark.one
    def test_quote_enter(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/fee/actual/quote/approval"
        result = ('PASS', '通过报价审核', 'HAS_QUOTE', 1)

        self.nomal_report = Read_yaml().yaml_show('nomal_report')
        if self.nomal_report:
            quote_offer = Read_sql_Data.Conte(quote_process % Read_yaml().yaml_show('requestOrderId', 'token.yaml'))
        else:
            quote_offer = Read_sql_Data.Conte(quote_offer_enter)

        print(quote_offer[0])
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
            "r-idempotent": r_idempotent(self.token, "quoteApproval")

        }
        datas = {
            "id": quote_offer[0][0],
            "requestOrderId": quote_offer[0][1],
            "approvalState": "PASS",
            "approvalRemark": "通过报价审核",
        }
        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        check = Read_sql_Data.Conte(quote_check % quote_offer[0][0])
        assert result == check[0]

    @allure.description("报价审核")
    @allure.suite('审核拒绝')
    @allure.title("审核拒绝")  # 测试用例的标题
    @allure.testcase('/fsm-platform/fee/actual/quote/approval')
    @pytest.mark.two
    def test_quote_enter2(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/fee/actual/quote/approval"
        result = ('REJECT', '拒绝报价审核', 'HAS_QUOTE', 0)
        quote_offer = Read_sql_Data.Conte(quote_offer_enter)
        print(quote_offer[0])
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
            "r-idempotent": r_idempotent(self.token, "quoteApproval")

        }
        datas = {
            "id": quote_offer[0][0],
            "requestOrderId": quote_offer[0][1],
            "approvalState": "REJECT",
            "approvalRemark": "拒绝报价审核",
        }
        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        check = Read_sql_Data.Conte(quote_check % quote_offer[0][0])
        assert result == check[0]
