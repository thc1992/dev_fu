# encoding=utf-8
from src.Search.Sql_search import *
from src.base.request_Control import *
from src.base.Read_sql_Data import *
import allure
import pytest


class Test_cancle_order:
    def sets_up(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/requestOrder/cancel"
        self.text = "信息填写错误,需要重新发布"

    @allure.description("未生成工单时，取消订单")
    @allure.suite('取消订单')
    @allure.title("取消订单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/requestOrder/cancel')
    @pytest.mark.two
    def test_cancle_order01(self):
        self.sets_up()
        result = ("FSMROS05","FSMROS04001",None,None,None,None,"FSMWOS04","FSMTOS03","FSMIOS03","FSMROS05","FSMROS04001",self.text,"ORDER_CANCEL_COMPLETE")
        # 未生成工单
        self.place_order = Read_sql_Data.Conte(cancle_informat + "AND t2.id IS NULL")
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlOmZzbV9zdG9yZV9zZWNyZXQ="
        }
        datas = {

            "cancelReason": self.text,
            "requestOrderIds": [self.place_order[0][0]]

        }
        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(cancle_state % self.place_order[0][0])
        assert result == appointment2[0]

    @allure.description("未生成任务单时，取消订单")
    @allure.suite('取消订单')
    @allure.title("取消订单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/requestOrder/cancel')
    @pytest.mark.two
    def test_cancle_order02(self):
        self.sets_up()
        result = (
        "FSMROS05", "FSMROS04001", "FSMWOS04", "FSMTOSOT06", None, None,"FSMWOS04", "FSMTOS03", "FSMIOS03", "FSMROS05",
        "FSMROS04001", self.text, "ORDER_CANCEL_COMPLETE")
        # 未生成任务单
        self.place_order = Read_sql_Data.Conte(cancle_informat + "AND t2.id IS NOT NULL  	AND t3.id IS NULL  	AND t2.order_status != 'FSMWOS04' ")
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlOmZzbV9zdG9yZV9zZWNyZXQ="
        }
        datas = {

            "cancelReason": self.text,
            "requestOrderIds": [self.place_order[0][0]]

        }
        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(cancle_state % self.place_order[0][0])
        assert result == appointment2[0]

    @allure.description("生成工单和任务单，取消订单")
    @allure.suite('取消订单')
    @allure.title("取消订单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/requestOrder/cancel')
    @pytest.mark.two
    def test_cancle_order03(self):
        self.sets_up()
        result = (
            "FSMROS05", "FSMROS04001", "FSMWOS04", "FSMTOSOT06", "FSMTOS03", "FSMTOSOT06","FSMWOS04", "FSMTOS03", "FSMIOS03",
            "FSMROS05",
            "FSMROS04001", self.text, "ORDER_CANCEL_COMPLETE")
        # 生成工单和任务单
        self.place_order = Read_sql_Data.Conte(cancle_informat + "AND t2.id IS NOT NULL AND t3.id IS NOT NULL AND t3.task_status ='FSMTOS01'")

        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlOmZzbV9zdG9yZV9zZWNyZXQ="
        }
        datas = {

            "cancelReason": self.text,
            "requestOrderIds": [self.place_order[0][0]]

        }
        res = request_all(self.url_use, datas, headers)
        assert res.json()['code'] == 200
        appointment2 = Read_sql_Data.Conte(cancle_state % self.place_order[0][0])
        assert result == appointment2[0]