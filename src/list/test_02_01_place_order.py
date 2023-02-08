# encoding=utf-8
from src.Search.Sql_search import *
from src.base.request_Control import *
from src.base.Read_sql_Data import *
import allure
import json
import pytest

from src.base.time_tools import *


class Test_place_order:
    @allure.description("验证下单操作")
    @allure.suite('下维修单')
    @allure.title("下维修单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/requestOrder/add')
    @pytest.mark.one
    def test_order(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.user_name=Read_yaml().yaml_show('login')['user_name']
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/requestOrder/add"
        path = open(os.path.dirname(os.path.abspath(__file__)) + '/../common/city.jpg', 'rb')
        print(path)
        self.image_id = get_image(path, self.token)
        path.close()
        self.place_order = Read_sql_Data.Conte(place_order)
        self.prace_name = "空调维修自动化"
        self.prace_version = Read_sql_Data.Conte(prace_order_version % self.prace_name)
        name = pro_duction % self.prace_name
        self.produ_version = name + pro_duction2
        self.production = Read_sql_Data.Conte(self.produ_version)
        pro_key = json.loads(self.production[0][0])
        prop_value = "select * from rdp_fsm.r_production_prop_value t1 where  t1.prop_id='%(1)s' and t1.prop_value='%(2)s'" % \
                     {'1': pro_key[0]['key'], '2': pro_key[0]['value_label']}
        self.production_value = Read_sql_Data.Conte(prop_value)
        name1 = get_name % self.prace_name
        produ_name = name1 + get_name2
        self.names = Read_sql_Data.Conte(produ_name)

        produ_high = get_high % self.prace_name
        self.high = Read_sql_Data.Conte(produ_high)


        name_phone=Read_sql_Data.Conte(user_info + "'%s'" % str(self.user_name))

        self.tim = Time_tools().get_time()

        print(self.production_value)
        assert self.image_id.json()['code'] == 200
        imag_id = self.image_id.json()['data']['id']
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "r-idempotent": r_idempotent(self.token, "requestOrder")
        }
        data = {
            "requestType": 'FSMST01',  # 订单类型         r_request_order       获取订单类型
            "brandId": self.place_order[0][1],
            "genericFlag": 'false',
            "contactPerson":name_phone[0][1],
            "contactPhone":name_phone[0][3],
            "serviceId": self.prace_version[0][0],  # r_production 通过名称获取id  这里id值是"serviceId":
            "serviceVersion": self.prace_version[0][1],
            "propValues": [

                {
                    "id": str(self.production_value[0][0]),
                    "createUser": str(self.production_value[0][1]),
                    "createUser_label": str(self.names[0][0]),
                    "createTime": str(str(self.production_value[0][2]).split('.')[0]),
                    "updateUser": str(self.production_value[0][3]),
                    "updateUser_label": str(self.names[0][0]),
                    "updateTime": str(str(self.production_value[0][4]).split('.')[0]),
                    "isDelete": self.production_value[0][5],
                    "propValue": str(self.production_value[0][6]),
                    "propId": str(self.production_value[0][7]),
                    "propKeyType": "PROPKT02",
                    "propName": "",
                    "propValueId": str(self.production_value[0][0])
                },
                {
                    "id": str(self.high[0][0]),
                    "createUser": str(self.high[0][1]),
                    "createUser_label": str(self.names[0][0]),
                    "createTime": str(str(self.high[0][2]).split('.')[0]),
                    "updateUser": str(self.high[0][3]),
                    "updateUser_label": str(self.names[0][0]),
                    "updateTime": str(str(self.high[0][4]).split('.')[0]),
                    "isDelete": self.high[0][5],
                    "valueId": str(self.high[0][6]),
                    "propValue": str(self.high[0][7]),
                    "keyId": str(self.high[0][8]),
                    "configKeyId": str(self.high[0][9]),
                    "propKeyType": "PROPKT01",
                    "propId": str(self.high[0][8]),
                    "propValueId": str(self.high[0][6])
                }

            ],

            "urgencyDegree": "FSMUD01",  # 紧急成度   01 紧急   02 一般
            "expectedDate": str(time.strftime("%Y-%m-%d")),
            "expectedTime": str(self.tim) + ':00-' + str(self.tim + 2) + ':00',
            "remark": "我们一起打豆豆",
            "appointmentDate": [
                str(time.strftime("%Y-%m-%d")),
                str(self.tim) + ':00-' + str(self.tim + 2) + ':00'
            ],
            "productName": self.prace_name,  # r_production通过名称获取id这里id值是"serviceId":
            "storeId": self.place_order[0][0],  # user --> r_store_rel_us "storeId":
            "imgOrVideos": [
                imag_id  # 图片接口返回的id值
            ]
        }

        res = request_all(self.url_use, data, headers=headers)
        # log_show(res, data, showlog=1)
        assert res.json()['code'] == 200
        # print(res.json())
        relut = place_check % res.json()['data']['id']
        production = Read_sql_Data.Conte(relut)
        result12 = (
            int(res.json()['data']['id']), int(res.json()['data']['brandId']), int(res.json()['data']['tenantId']),
            'FSMROS01', 'WAIT_OUTLETS_CONFIRM',
            'FSMIOS01', 'FSMROS01')
        # 查询表中是否有新建的订单
        # # 验证返回数据和数据库数据是否一致
        assert result12 == production[0]
        # 存表的id值
        old_data = Read_yaml().read_yaml_all('token.yaml')  # 读取文件数据
        old_data['requestOrderId'] = str(res.json()['data']['id'])
        Read_yaml().update_yaml(old_data, 'token.yaml')
        return str(res.json()['data']['id'])
