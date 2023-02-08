# encoding=utf-8
from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
import pytest
from src.read_yaml.read_yaml import Read_yaml


class Test_select_outlets:
    def getrequest(self, booles):

        self.nomal_report = Read_yaml().yaml_show('nomal_report')
        if self.nomal_report:
            if booles == "1":
                orderid = Read_sql_Data.Conte(no_chose_order)
                self.request_order_id = str(orderid[0][0])
            else:
                self.request_order_id = Read_yaml().yaml_show('requestOrderId', 'token.yaml')
        return self.request_order_id

    def stepup(self, booles):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        url_use = Read_yaml().yaml_show('host') + "/fsm-platform/requestOrder/matchOutlets"
        self.urlname = Read_yaml().yaml_show('host') + "/fsm-platform/requestOrder/queryOutletsConfirmInfo"
        self.request = self.getrequest(booles)
        self.store_id = Read_sql_Data.Conte(
            "select store_id from rdp_fsm.r_request_order  WHERE  id='%s'" % self.request)
        self.headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA=="
        }
        datas = {
            "id": self.request,
            "storeId": self.store_id[0][0]
        }
        res = requests.post(url=url_use, json=datas, headers=self.headers)
        log_show(res, datas)
        assert res.json()['code'] == 200 and res.json()['data']['outletsList'] != None

        for i in res.json()['data']['outletsList']:
            if i['isPlatformContract'] == True:
                if i['outletsName'] == "浦口体验店":
                    self.outlites = i
            else:
                if i['outletsName'] == "浦口体验店":
                    self.outlites2 = i

    @allure.description("选择服务商")
    @allure.suite('选择平台服务商')
    @allure.title("选择平台服务商")  # 测试用例的标题
    @allure.testcase('/fsm-platform/workOrder/confirmOutlets')
    @pytest.mark.two
    def test_select_lets(self):
        self.stepup("1")
        datas2 = {
            "outletsId": self.outlites['outletsId'],
            "requestOrderId": self.request,
            "supplierId": self.outlites['supplierId'],
            "contractId": self.outlites['contractId'],
            "skuId": self.outlites['skuId'],
            "supplierProductionId": self.outlites['supplierProductionId'],
            "storeId": self.store_id[0][0]
        }
        res2 = requests.post(url=self.urlname, json=datas2, headers=self.headers)
        log_show(res2, datas2)
        assert res2.json()['code'] == 200 and res2.json()['data'] != None

        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/workOrder/confirmOutlets"
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "r-idempotent": r_idempotent(self.token, "workOrder"),
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA=="

        }
        res = requests.post(url=self.url_use, json=res2.json()['data'], headers=headers)
        log_show(res, res2.json()['data'])
        assert res.json()['code'] == 200
        result12 = ("FSMROS01", "FSMWOS02", "DISPATCH_ORDER", "FSMIOS01", "FSMROS01", "FSMWOS02")
        ce = Read_sql_Data.Conte(order_check % res.json()['data']['id'])
        # # 验证返回数据和数据库数据是否一致
        assert result12 == ce[0]
        # 存表的id值
        old_data = Read_yaml().read_yaml_all('token.yaml')  # 读取文件数据
        old_data['workOrderId'] = str(res.json()['data']['id'])
        Read_yaml().update_yaml(old_data, 'token.yaml')

    @allure.description("选择服务商")
    @allure.suite('选择合约服务商')
    @allure.title("选择合约服务商")  # 测试用例的标题
    @allure.testcase('/fsm-platform/workOrder/confirmOutlets')
    @pytest.mark.one
    def test_select_lets2(self):
        self.stepup("0")
        datas2 = {
            "outletsId": self.outlites2['outletsId'],
            "requestOrderId": self.request,
            "supplierId": self.outlites2['supplierId'],
            "contractId": self.outlites2['contractId'],
            "skuId": self.outlites2['skuId'],
            "supplierProductionId": self.outlites2['supplierProductionId'],
            "storeId": self.store_id[0][0]
        }
        res2 = requests.post(url=self.urlname, json=datas2, headers=self.headers)
        log_show(res2, datas2)
        assert res2.json()['code'] == 200 and res2.json()['data'] != None

        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/workOrder/confirmOutlets"
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "r-idempotent": r_idempotent(self.token, "workOrder"),
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA=="

        }
        res = requests.post(url=self.url_use, json=res2.json()['data'], headers=headers)
        log_show(res, res2.json()['data'])
        assert res.json()['code'] == 200
        # print(res.json())
        result12 = ("FSMROS01", "FSMWOS02", "DISPATCH_ORDER", "FSMIOS01", "FSMROS01", "FSMWOS02")
        ce = Read_sql_Data.Conte(order_check % res.json()['data']['id'])
        # # 验证返回数据和数据库数据是否一致
        assert result12 == ce[0]
        # 存表的id值
        old_data = Read_yaml().read_yaml_all('token.yaml')  # 读取文件数据
        old_data['workOrderId'] = str(res.json()['data']['id'])
        Read_yaml().update_yaml(old_data, 'token.yaml')
