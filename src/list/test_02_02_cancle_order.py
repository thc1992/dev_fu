# encoding=utf-8
from src.Search.Sql_search import *
from src.base.request_Control import *
from src.base.Read_sql_Data import *
import allure
import pytest


class Test_cancle_order:
    @allure.description("取消订单")
    @allure.suite('取消订单')
    @allure.title("取消订单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/requestOrder/cancel')
    @pytest.mark.two
    def test_cancle_order(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/requestOrder/cancel"
        result = ("FSMIOS03", "FSMROS05", "FSMROS04001", "FSMTOSOT06", "FSMROS05", "FSMROS04001")
        self.place_order = Read_sql_Data.Conte(cancle_informat)

        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlOmZzbV9zdG9yZV9zZWNyZXQ="
        }
        datas = {

            "cancelReason": "信息填写错误,需要重新发布",
            "requestOrderIds": [self.place_order[0][0]]

        }
        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(cancle_state % self.place_order[0][0])
        assert result == appointment2[0]
