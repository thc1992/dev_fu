# encoding=utf-8
import random
from decimal import Decimal

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest
from src.list.test_quote_save import Test_quote_save

class Test_quote_submit_suptobrand:
    @allure.description("查看详情")
    @allure.suite('报价')
    @allure.title("报价")  # 测试用例的标题
    @allure.testcase('/fsm-platform/fee/actual/workOrder/submit')
    @pytest.mark.one
    def test_quote_submit_suptobrand(self):
        quoteId_data = Read_sql_Data.Conte(quoteId_suptobrand)[0][0]
        quote_submit = Read_sql_Data.Conte(result_quoteId_suptobrand % str(quoteId_data))
        quote_id = quote_submit[0][0]
        quotesave=Test_quote_save()
        quotesave.quote_save(quote_id)
        # print(quote_submit)
        url_use = Read_yaml().yaml_show('host') + "/fsm-platform/fee/actual/workOrder/submit"
        token = Read_yaml().yaml_show('access_token', 'token.yaml')
        headers = {
            "r-auth": token,
            "Content-Type": "application/json"
        }
        data = {
            "id": quote_submit[0][8],
            "quoteId": quote_id
        }
        print(url_use)
        res = requests.request(method="post", url=url_use, headers=headers, json=data)
        assert res.status_code == 200
        log_show(res, data)
        list_sql_check = Read_sql_Data.Conte(check_quote_submit + str(quote_id))
        assert list_sql_check == [('APPLY', 'HAS_QUOTE', 1)]
