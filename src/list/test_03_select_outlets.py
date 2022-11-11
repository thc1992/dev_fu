# encoding=utf-8
from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
import pytest
from src.read_yaml.read_yaml import Read_yaml


class Test_select_outlets:
    @allure.description("选择服务商")
    @allure.suite('服务商选择')
    @allure.title("服务商选择")  # 测试用例的标题
    @allure.testcase('/fsm-platform/workOrder/confirmOutlets')
    @pytest.mark.one
    def test_select_lets(self):
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/workOrder/confirmOutlets"
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.nomal_report = Read_yaml().yaml_show('nomal_report')
        if self.nomal_report:
            print(2222222222222222222222222222222222222)
            request_order_id = Read_yaml().yaml_show('requestOrderId', 'token.yaml')
        else:
            self.orderid = Read_sql_Data.Conte(no_chose_order)
            request_order_id = str(self.orderid[0][0])
        self.order = Read_sql_Data.Conte(order_choose)

        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "r-idempotent": r_idempotent(self.token, "workOrder"),
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA=="

        }

        datas = {"requestOrderId": request_order_id,
                 "outletsId": str(self.order[0][0]),
                 "supplierId": str(self.order[0][1]),
                 "skuId": str(self.order[0][2]),
                 "hours":'1.0',
                 "hourPrice": '50.00',
                 "totalPrice": '150.00',
                 "serviceName": self.order[0][3],
                 "salesDetails": [
                     {

                         "hourPrice": "50.00",
                         "hours": "1.0",
                         "totalPrice": "50.00",

                         "feeType": "ARTIFICIAL_FEE"
                     },
                     {

                         "priceType": "SUPPLIER_PRICE",
                         "keyId": "1574669071178870785",
                         "keyId_label": "高空作业",
                         "valueId": "1574669071208230913",
                         "totalPrice": "100.00",
                         "feeType": "ADDITIONAL_FEE"
                     }
                 ],
                 "isPlatformContract": False
                 }

        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        print(res.json())

        result12 = ("FSMROS01", "FSMWOS02", "DISPATCH_ORDER", "FSMIOS01", "FSMROS01", "FSMWOS02")

        ce = Read_sql_Data.Conte(order_check % res.json()['data']['id'])
        # # 验证返回数据和数据库数据是否一致
        assert result12 == ce[0]

        # 存表的id值
        old_data = Read_yaml().read_yaml_all('token.yaml')  # 读取文件数据
        old_data['workOrderId'] = str(res.json()['data']['id'])
        Read_yaml().update_yaml(old_data, 'token.yaml')
