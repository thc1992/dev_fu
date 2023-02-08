# encoding=utf-8
import random
from decimal import Decimal

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest

class Test_settlement_submit():
    @allure.description("查看详情")
    @allure.suite('提交结算')
    @allure.title("提交结算")  # 测试用例的标题
    @allure.testcase('/fsm-platform/fee/settlement/submit')
    @pytest.mark.one
    def test_settlement_submit(self):
        url_use = Read_yaml().yaml_show('host') + "/fsm-platform/fee/settlement/submit"
        token = Read_yaml().yaml_show('access_token', 'token.yaml')
        quoteId = Read_sql_Data.Conte(settlement_submit)[0][0]
        headers = {
            "r-auth": token,
            "Content-Type": "application/json"
        }
        data = {
                "quoteIds": [quoteId]
            }
        res = requests.request(method="post", url=url_use, headers=headers, json=data)
        log_show(res, data)
        assert res.status_code == 200
        quote_submit = Read_sql_Data.Conte(check_settlement % str(quoteId))
        assert quote_submit == [('Y', 'APPLY')]