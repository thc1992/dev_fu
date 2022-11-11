# encoding=utf-8
from src.Search.Sql_search import *
from src.base.request_Control import *
from src.base.Read_sql_Data import *
import allure
import json
import pytest


class Test_update_order:
    @allure.description("修改订单")
    @allure.suite('修改')
    @allure.title("修改")  # 测试用例的标题
    @allure.testcase('/fsm-platform/requestOrder/update')
    @pytest.mark.two
    def test_update_orders(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/requestOrder/update"
        self.prace_name = "空调维修自动化"
        remark = "测试修改订单"
        self.update_order = Read_sql_Data.Conte(update_order)  # 未选择服务商的订单
        user_lable = Read_sql_Data.Conte(
            "select real_name,phone from rdp_system.r_user  where id='%s'" % self.update_order[0][1])
        name = pro_duction % self.prace_name
        self.produ_version = name + pro_duction2
        self.production = Read_sql_Data.Conte(self.produ_version)
        pro_key = json.loads(self.production[0][0])
        prop_value = "select * from rdp_fsm.r_production_prop_value t1 where  t1.prop_id='%(1)s' and t1.prop_value='%(2)s'" % \
                     {'1': pro_key[0]['key'], '2': pro_key[0]['value_label']}

        image = "select file_id  from rdp_system.r_biz_file  where  biz_id='%s'" % self.update_order[0][0]
        images = Read_sql_Data.Conte(image)
        if len(images[0]) > 1:
            for i in images:
                imagevide = images[0][i]
        else:
            imagevide = [images[0][0]]

        print(imagevide)
        self.production_value = Read_sql_Data.Conte(prop_value)  # 空调人员

        name1 = get_name % self.prace_name
        produ_name = name1 + get_name2
        self.names = Read_sql_Data.Conte(produ_name)  # 高空作业创建人

        produ_high = get_high % self.prace_name
        self.high = Read_sql_Data.Conte(produ_high)  # 高空作业参数

        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
        }
        datas = {
            "id": self.update_order[0][0],
            "createUser": self.update_order[0][1],
            "createUser_label": user_lable[0][0],
            "createTime": str(self.update_order[0][2]),
            "updateUser": self.update_order[0][3],
            "updateUser_label": user_lable[0][0],
            "updateTime": str(self.update_order[0][4]),
            "isDelete": self.update_order[0][5],
            "tenantId": self.update_order[0][6],
            "brandId": self.update_order[0][7],
            "storeId": self.update_order[0][8],
            "requestType": self.update_order[0][9],
            "orderStatus": self.update_order[0][10],
            "orderCode": self.update_order[0][11],
            "submitDealStatus": self.update_order[0][12],
            "hasEvaluate": self.update_order[0][13],
            "typeDisplay": self.prace_name,

            "expectedStartTime": str(str(self.update_order[0][14]).split(' ')[0] + ' ' +
                                     str(self.update_order[0][14]).split(' ')[1][:5]),
            "expectedEndTime": str(str(self.update_order[0][15]).split(' ')[0] + ' ' +
                                   str(self.update_order[0][15]).split(' ')[1][:5]),
            "urgencyDegree": self.update_order[0][16],
            "remark": remark,
            "serviceId": self.update_order[0][17],
            "serviceVersion": self.update_order[0][18],
            "imgOrVideos": [
                str(imagevide[0])
            ],
            "propValues": [
                {
                    "id": self.production_value[0][0],
                    "createUser": self.production_value[0][1],
                    "createUser_label": self.names[0][0],
                    "createTime": str(self.production_value[0][2]).split('.')[0],
                    "updateUser": self.production_value[0][3],
                    "updateUser_label": self.names[0][0],
                    "updateTime": str(self.production_value[0][4]).split('.')[0],
                    "isDelete": self.production_value[0][5],
                    "propValue": self.production_value[0][6],
                    "propId": self.production_value[0][7],
                    "propKeyType": "PROPKT02",
                    "propName": "",
                    "propValueId": self.production_value[0][0]
                },
                {
                    "id": self.high[0][0],
                    "createUser": self.high[0][1],
                    "createUser_label": self.names[0][0],
                    "createTime": str(self.high[0][2]).split('.')[0],
                    "updateUser": self.high[0][3],
                    "updateUser_label": self.names[0][0],
                    "updateTime": str(self.high[0][4]).split('.')[0],
                    "isDelete": self.high[0][5],
                    "valueId": self.high[0][6],
                    "propValue": self.high[0][7],
                    "keyId": self.high[0][8],
                    "price": self.high[0][10],
                    "configKeyId": self.high[0][9],
                    "propKeyType": "PROPKT01",
                    "propName": "",
                    "propId": self.high[0][8],
                    "propValueId": self.high[0][6]
                }
            ],
            "expectedDate": str(str(self.update_order[0][14]).split(' ')[0]),
            "expectedTime": str(str(self.update_order[0][14]).split(' ')[1][:5] + '-' +
                                str(self.update_order[0][15]).split(' ')[1][:5]),
            "expectedDisplay": str(str(self.update_order[0][14]).split(' ')[0] + ' ' +
                                   str(self.update_order[0][14]).split(' ')[1][:5] + '-' +
                                   str(self.update_order[0][15]).split(' ')[1][:5]),
            "orderUserPhone": user_lable[0][1],
            "genericFlag": False,
            "productName": self.prace_name,
            "appointmentDate": [
                str(str(self.update_order[0][14]).split(' ')[0]),
                str(str(self.update_order[0][14]).split(' ')[1][:5] + '-' + str(self.update_order[0][15]).split(' ')[1][
                                                                            :5])
            ]
        }
        result = ('FSMROS01', 'FSMIOS01', 'FSMROS01', 'WAIT_OUTLETS_CONFIRM', remark)

        res = requests.put(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas, showlog=1)
        assert res.json()['code'] == 200
        check = Read_sql_Data.Conte(update_check % self.update_order[0][0])
        assert result == check[0]
