# encoding=utf-8
import re

from src.Search.Sql_search import *
from src.base.request_Control import *
from src.base.Read_sql_Data import *
import allure
import pytest


class Test_operation_confirm():
    def sets_up(self):
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/confirm"
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.headers = {
            "r-auth": self.token,
            "Content-Type": "application/json"
        }
        self.pass_code = ('CONFIRMR01', 'CONFIRMR02', 'CONFIRMR03')
        self.data_dict = {
            'CONFIRMR01': '正常完成', 'CONFIRMR02': '维修成本过高，未进行服务', 'CONFIRMR03': '问题自行恢复正常，未进行服务','CONFIRMR04': '没有维修好，问题依然存在', 'CONFIRMR05': '工程师无法处理，需要重新安排', 'CONFIRMR06': '工程师未到店'}
        self.data_comfirm_dict = {confirm_requestOrderId01: '正常完成', confirm_requestOrderId02: '到店未服务',confirm_requestOrderId03: '电话指导完成', confirm_requestOrderId04: '误发起完成',confirm_requestOrderId05: '协商完成'}

    # 确认完成检查方法
    def confirm_sql_check(self, requestOrderId, remark, confirm_code):
        sql_check = sql_check_confirm  % str(requestOrderId)
        # print(sql_check)
        list_sql_check = Read_sql_Data.Conte(sql_check)
        # 登陆用户作为确认店员
        userId = Read_yaml().yaml_show('login')['user_name']
        user_id = Read_sql_Data.Conte(sql_user_id % str(userId))
        # 确认完成
        if confirm_code in self.pass_code:
            check_condition = Read_sql_Data.Conte(sql_check_condition + "(%s)" % str(requestOrderId))
            if len(check_condition) > 0:
                if check_condition[0][0] == 'ACTUAL_QUOTE':
                    check_condition = 'ORDER_COMPLETE'
                else:
                    check_condition = 'ACTUAL_QUOTE'

            else:
                check_condition = 'ORDER_COMPLETE'

            assert list_sql_check == [('FSMROS04', 'FSMWOS04', 'FSMTOS03', 'FSMROS04', 'FSMWOS04', 'FSMIOS03',
                                       'FSMOCF01', check_condition, 'FSMOCF01', remark, user_id[0][0], confirm_code)]
            # print(check_condition)
        # 确认未完成
        else:
            assert list_sql_check == [('FSMROS02', 'FSMWOS05', 'FSMTOS03', 'FSMROS02', 'FSMWOS05', 'FSMIOS01',
                                       'FSMOCF02', 'DISPUTE_ORDER', 'FSMOCF02', remark, user_id[0][0], confirm_code)]

    @allure.description("正常完成")
    @allure.suite('正常完成')
    @allure.title("正常完成")  # 测试用例的标题
    @allure.testcase('fsm-platform/operation/confirm')
    @pytest.mark.one
    def test_operation_confirm(self):
        self.sets_up()
        items = self.data_dict.items()
        self.nomal_report = Read_yaml().yaml_show('nomal_report')
        if self.nomal_report:
            appointment = task_order_show % Read_yaml().yaml_show('workOrderId', 'token.yaml')
            self.data_comfirm_dict = {appointment: '正常完成'}

        comfirm_items = self.data_comfirm_dict.items()
        for confirm_code, remark in items:
            # print(remark)
            # print(confirm_code)
            for confirm_requestOrderId, type in comfirm_items:
                requestOrderId = Read_sql_Data.Conte(confirm_requestOrderId)
                # print(requestOrderId)

                try:
                    if self.nomal_report:
                        request_order_id = requestOrderId[0][1]
                    else:
                        request_order_id = requestOrderId[0][0]

                    if confirm_code in self.pass_code:
                        # 确认完成
                        data = {
                            "remark": remark,
                            "requestOrderId": request_order_id,
                            "confirmCode": confirm_code
                        }
                        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
                        log_show(res, data)
                        assert res.status_code == 200
                        self.confirm_sql_check(request_order_id, remark, confirm_code)
                        if self.nomal_report:
                            return
                    else:
                        # 确认未完成
                        requestOrderId = Read_sql_Data.Conte(confirm_requestOrderId)
                        data = {
                            "remark": remark,
                            "requestOrderId": requestOrderId[0][0],
                            "confirmCode": confirm_code
                        }
                        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
                        log_show(res, data)
                        assert res.status_code == 200
                        self.confirm_sql_check(requestOrderId[0][0], remark, confirm_code)
                    print(type + remark + "-用例执行成功")

                except IndexError:
                    print(type + remark + "-用例未执行")

    @allure.description("多场景下，订单确认完成和确认未完成")
    @allure.suite('多场景下，订单确认完成和确认未完成')
    @allure.title("多场景下，订单确认完成和确认未完成")  # 测试用例的标题
    @allure.testcase('fsm-platform/operation/confirm')
    @pytest.mark.two
    def test_operation_confirm_all(self):
        self.sets_up()
        items = self.data_dict.items()
        comfirm_items = self.data_comfirm_dict.items()
        for confirm_code, remark in items:
            # print(remark)
            # print(confirm_code)
            for confirm_requestOrderId, type in comfirm_items:
                requestOrderId = Read_sql_Data.Conte(confirm_requestOrderId)
                # print(requestOrderId)
                try:
                    request_order_id = requestOrderId[0][0]
                    if confirm_code in self.pass_code:
                        # 确认完成
                        data = {
                            "remark": remark,
                            "requestOrderId": request_order_id,
                            "confirmCode": confirm_code
                        }
                        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
                        log_show(res, data)
                        assert res.status_code == 200
                        self.confirm_sql_check(request_order_id, remark, confirm_code)
                    else:
                        # 确认未完成
                        requestOrderId = Read_sql_Data.Conte(confirm_requestOrderId)
                        data = {
                            "remark": remark,
                            "requestOrderId": requestOrderId[0][0],
                            "confirmCode": confirm_code
                        }
                        res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
                        log_show(res, data)
                        assert res.status_code == 200
                        self.confirm_sql_check(requestOrderId[0][0], remark, confirm_code)
                    print(type + remark + "-用例执行成功")

                except IndexError:
                    print(type + remark + "-用例未执行")
