# encoding=utf-8
from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest




class Test_handle:
    @allure.description("派单")
    @allure.suite('派单')
    @allure.title("派单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/handle')
    @pytest.mark.one
    def test_handle(self):

        url_use = Read_yaml().yaml_show('host') + "/fsm-platform/operation/handle"
        token = Read_yaml().yaml_show('access_token', 'token.yaml')
        headers = {
            "r-auth": token,
            "Content-Type": "application/json",
            "r-idempotent": r_idempotent(token, "orderOperate")
        }

        self.nomal_report = Read_yaml().yaml_show('nomal_report')

        if self.nomal_report:
            self.list_sql_search = Read_sql_Data.Conte(name_work % Read_yaml().yaml_show('workOrderId', 'token.yaml'))
        else:
            self.list_sql_search = Read_sql_Data.Conte(distribute)

        work_order_id = self.list_sql_search[0][0]
        self.user_id = self.list_sql_search[0][1]

        data = {
            "operationType": "DISPATCH",
            "remark": "派单",
            "engineerId": self.user_id,
            "workOrderIds": [
                work_order_id
            ]
        }
        res = requests.request(method="post", url=url_use, headers=headers, json=data)
        # print(res.text)
        assert res.status_code == 200
        log_show(res, data)
        sql_check = sql_check_handle + "(%s)" % str(work_order_id)
        # print(sql_check)
        list_sql_check = Read_sql_Data.Conte(sql_check)
        assert list_sql_check == [(
            'FSMROS02', 'FSMWOS03', 'FSMWOS03', 'FSMROS02', 'APPOINT_TIME', 'FSMIOS01', 'FSMTOS01', self.user_id)]



    # @allure.description("派单")
    # @allure.suite('批量派单')
    # @allure.title("批量派单")  # 测试用例的标题
    # @allure.testcase('/fsm-platform/operation/handle')
    # @pytest.mark.two
    # def test_batch_handle(self):
    #     self.list_sql_search = Read_sql_Data.Conte(distribute)
    #     assert len(self.list_sql_search) > 1
    #     self.user_id = self.list_sql_search[0][1]
    #     work_order_id = self.list_sql_search[0][0], self.list_sql_search[1][0]
    #     print(work_order_id)
    #     self.check_sql = (
    #         'FSMROS02', 'FSMWOS03', 'FSMWOS03', 'FSMROS02', 'APPOINT_TIME', 'FSMIOS01', 'FSMTOS01', self.user_id)
    #     data = {
    #         "operationType": "DISPATCH",
    #         "remark": "批量派单",
    #         "engineerId": self.user_id,
    #         "workOrderIds": [
    #             *work_order_id
    #         ]
    #     }
    #
    #     res = requests.request(method="post", url=url_use, headers=headers, json=data)
    #     print(res.text)
    #     assert res.status_code == 200
    #     log_show(res, data)
    #     sql_check = sql_check_handle + "%s" % str(work_order_id)
    #     print(sql_check)
    #     # 改成list，返回【】，接口校验不通过；改成元组，一条数据（a,）,校验不通过，分开处理
    #     list_sql_check = Read_sql_Data.Conte(sql_check)
    #     for i in range(0, len(list_sql_check)):
    #         assert list_sql_check[i] == self.check_sql
            # print(list_sql_check[i])
