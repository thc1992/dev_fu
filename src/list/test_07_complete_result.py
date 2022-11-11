# encoding=utf-8
from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
import pytest

from src.base.time_tools import *
from src.read_yaml.read_yaml import Read_yaml


class Test_complete_result:
    def sets_up(self):
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.path = open(os.path.dirname(os.path.abspath(__file__)) + '/../common/city.jpg', 'rb')
        self.path2 = open(os.path.dirname(os.path.abspath(__file__)) + '/../common/after.jpg', 'rb')
        self.taskOrder = Read_yaml().yaml_show('host') + "/fsm-platform/orderDetail/taskOrder?id="
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/taskOrder/complete"

        image_id = get_image(self.path, self.token)
        assert image_id.json()['code'] == 200
        self.afterService = image_id.json()['data']['id']
        image_id2 = get_image(self.path2, self.token)
        assert image_id2.json()['code'] == 200
        self.beforeService = image_id2.json()['data']['id']
        self.headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA=="
        }

    @allure.description("完成工单")
    @allure.suite('正常完成')
    @allure.title("正常完成")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/complete')
    @pytest.mark.one
    def test_complete(self):
        self.sets_up()

        relust = ('FSMWOS03', 'FSMROS03', 'FSMWOS03', 'FSMTOS03', 'FSMIOS01', 'FSMROS03', 'WAIT_CONFIRM',
                  'FSMTOSOT01', 'FSMTOS03', 'FSMTOSOT01')

        self.nomal_report = Read_yaml().yaml_show('nomal_report')
        if self.nomal_report:
            appointment = Read_sql_Data.Conte(task_order_show % Read_yaml().yaml_show('workOrderId', 'token.yaml'))
        else:
            appointment = Read_sql_Data.Conte(restule)

        appointment2 = Read_sql_Data.Conte(group_ip % appointment[0][1])

        data = {
            "key": appointment[0][0]
        }
        res = requests.get(url=self.taskOrder + str(appointment[0][0]), json=data, headers=self.headers)
        assert res.json()['code'] == 200
        # log_show(res, data)
        # print(res.json()['data'])

        datas = {
            "afterService": [self.afterService],
            "beforeService": [self.beforeService],
            "id": appointment[0][0],
            "operationInfo": res.json()['data']['typeDisplay'],
            "operationType": "FSMTOSOT01",
            "propValues": [
                {
                    "createTime": res.json()['data']['createTime'],
                    "createUser": res.json()['data']['createUser'],
                    "createUser_label": res.json()['data']['createUser_label'],
                    "groupId": str(appointment2[0][6]),
                    "id": str(appointment2[0][0]),
                    "isDelete": res.json()['data']['isDelete'],
                    "propId": str(appointment2[0][2]),
                    "propKeyType": str(appointment2[0][5]),
                    "propName": appointment2[0][7],
                    "propValue": appointment2[0][8],
                    "propValueId": str(appointment2[0][4]),
                    "requestOrderId": appointment2[0][1],
                    "updateTime": res.json()['data']['updateTime'],
                    "updateUser": res.json()['data']['updateUser'],
                    "updateUser_label": res.json()['data']['updateUser_label']
                },
                {
                    "createTime": res.json()['data']['createTime'],
                    "createUser": res.json()['data']['createUser'],
                    "createUser_label": res.json()['data']['createUser_label'],
                    "groupId": str(appointment2[1][6]),
                    "id": str(appointment2[1][0]),
                    "isDelete": appointment2[1][3],
                    "propId": str(appointment2[1][2]),
                    "propKeyType": appointment2[1][5],
                    "propName": appointment2[1][7],
                    "propValue": appointment2[1][8],
                    "propValueId": str(appointment2[1][4]),
                    "requestOrderId": str(appointment2[1][1]),
                    "updateTime": res.json()['data']['updateTime'],
                    "updateUser": res.json()['data']['updateUser'],
                    "updateUser_label": res.json()['data']['updateUser_label']
                }
            ],
            "remark": "我们一起打豆豆，然后就测试完成了",
            "serviceId": res.json()['data']['serviceId'],
            "serviceVersion": res.json()['data']['serviceVersion']

        }
        res = requests.post(url=self.url_use, json=datas, headers=self.headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        normal = Read_sql_Data.Conte(result_normal % appointment[0][0])
        assert relust == normal[0]

    @allure.description("完成工单")
    @allure.suite('预约二次完成')
    @allure.title("预约二次完成")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/complete')
    @pytest.mark.two
    def test_complete2(self):
        self.sets_up()

        relust = ('FSMWOS03', 'FSMROS02', 'FSMWOS03', 'FSMTOS02', 'FSMIOS01', 'FSMROS02', 'WAIT_SIGN_IN',
                  None, 'FSMTOS02', None)
        relust2 = ('FSMWOS03', 'FSMROS02', 'FSMWOS03', 'FSMTOS02', 'FSMIOS01', 'FSMROS02', 'WAIT_SIGN_IN',
                   None, 'FSMTOS03', 'FSMTOSOT02')

        appointment = Read_sql_Data.Conte(restule)
        appointment2 = Read_sql_Data.Conte(group_ip % appointment[0][1])

        data = {
            "key": appointment[0][0]
        }
        res = requests.get(url=self.taskOrder + str(appointment[0][0]), json=data, headers=self.headers)
        assert res.json()['code'] == 200
        # log_show(res, data)
        # print(res.json()['data'])
        self.tim = Time_tools().get_time()

        datas = {
            "afterService": [self.afterService],
            "appointment": [str(time.strftime("%Y-%m-%d")), str(self.tim) + ':00-' + str(self.tim + 2) + ':00'],
            "appointmentDate": str(time.strftime("%Y-%m-%d")),
            "appointmentTime": str(self.tim) + ':00-' + str(self.tim + 2) + ':00',
            "beforeService": [self.beforeService],
            "id": appointment[0][0],
            "operationInfo": res.json()['data']['typeDisplay'],
            "operationType": "FSMTOSOT02",
            "propValues": [
                {
                    "createTime": res.json()['data']['createTime'],
                    "createUser": res.json()['data']['createUser'],
                    "createUser_label": res.json()['data']['createUser_label'],
                    "groupId": str(appointment2[0][6]),
                    "id": str(appointment2[0][0]),
                    "isDelete": res.json()['data']['isDelete'],
                    "propId": str(appointment2[0][2]),
                    "propKeyType": str(appointment2[0][5]),
                    "propName": appointment2[0][7],
                    "propValue": appointment2[0][8],
                    "propValueId": str(appointment2[0][4]),
                    "requestOrderId": appointment2[0][1],
                    "updateTime": res.json()['data']['updateTime'],
                    "updateUser": res.json()['data']['updateUser'],
                    "updateUser_label": res.json()['data']['updateUser_label']
                },
                {

                    "createTime": res.json()['data']['createTime'],
                    "createUser": res.json()['data']['createUser'],
                    "createUser_label": res.json()['data']['createUser_label'],
                    "groupId": str(appointment2[1][6]),
                    "id": str(appointment2[1][0]),
                    "isDelete": appointment2[1][3],
                    "propId": str(appointment2[1][2]),
                    "propKeyType": appointment2[1][5],
                    "propName": appointment2[1][7],
                    "propValue": appointment2[1][8],
                    "propValueId": str(appointment2[1][4]),
                    "requestOrderId": str(appointment2[1][1]),
                    "updateTime": res.json()['data']['updateTime'],
                    "updateUser": res.json()['data']['updateUser'],
                    "updateUser_label": res.json()['data']['updateUser_label']
                }
            ],
            "remark": "协商达成",
            "serviceId": res.json()['data']['serviceId'],
            "serviceVersion": res.json()['data']['serviceVersion']

        }
        res = requests.post(url=self.url_use, json=datas, headers=self.headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        normal = Read_sql_Data.Conte(return_check % appointment[0][0])
        # print(normal[0])
        assert relust == normal[0] and relust2 == normal[1]

    @allure.description("完成工单")
    @allure.suite('转上级主管')
    @allure.title("转上级主管")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/complete')
    @pytest.mark.two
    def test_complete3(self):
        self.sets_up()
        relust = ('FSMWOS02', 'FSMROS01', 'FSMWOS02', None, 'FSMIOS01', 'FSMROS01', 'DISPATCH_ORDER',
                  None, 'FSMTOS03', 'FSMTOSOT03')

        appointment = Read_sql_Data.Conte(restule)
        appointment2 = Read_sql_Data.Conte(group_ip % appointment[0][1])

        data = {
            "key": appointment[0][0]
        }
        res = requests.get(url=self.taskOrder + str(appointment[0][0]), json=data, headers=self.headers)
        assert res.json()['code'] == 200
        # log_show(res, data)
        # print(res.json()['data'])
        self.tim = Time_tools().get_time()

        datas = {
            "afterService": [self.afterService],
            "beforeService": [self.beforeService],
            "id": appointment[0][0],
            "operationInfo": res.json()['data']['typeDisplay'],
            "operationType": "FSMTOSOT03",
            "propValues": [
                {
                    "createTime": res.json()['data']['createTime'],
                    "createUser": res.json()['data']['createUser'],
                    "createUser_label": res.json()['data']['createUser_label'],
                    "groupId": str(appointment2[0][6]),
                    "id": str(appointment2[0][0]),
                    "isDelete": res.json()['data']['isDelete'],
                    "propId": str(appointment2[0][2]),
                    "propKeyType": str(appointment2[0][5]),
                    "propName": appointment2[0][7],
                    "propValue": appointment2[0][8],
                    "propValueId": str(appointment2[0][4]),
                    "requestOrderId": appointment2[0][1],
                    "updateTime": res.json()['data']['updateTime'],
                    "updateUser": res.json()['data']['updateUser'],
                    "updateUser_label": res.json()['data']['updateUser_label']
                },
                {

                    "createTime": res.json()['data']['createTime'],
                    "createUser": res.json()['data']['createUser'],
                    "createUser_label": res.json()['data']['createUser_label'],
                    "groupId": str(appointment2[1][6]),
                    "id": str(appointment2[1][0]),
                    "isDelete": appointment2[1][3],
                    "propId": str(appointment2[1][2]),
                    "propKeyType": appointment2[1][5],
                    "propName": appointment2[1][7],
                    "propValue": appointment2[1][8],
                    "propValueId": str(appointment2[1][4]),
                    "requestOrderId": str(appointment2[1][1]),
                    "updateTime": res.json()['data']['updateTime'],
                    "updateUser": res.json()['data']['updateUser'],
                    "updateUser_label": res.json()['data']['updateUser_label']
                }
            ],
            "remark": "协商达成",
            "serviceId": res.json()['data']['serviceId'],
            "serviceVersion": res.json()['data']['serviceVersion']

        }
        res = requests.post(url=self.url_use, json=datas, headers=self.headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        normal = Read_sql_Data.Conte(turn_super % appointment[0][0])
        # print(normal[0])
        assert relust == normal[0]

    @allure.description("完成工单")
    @allure.suite('到店未服务')
    @allure.title("到店未服务")  # 测试用例的标题
    @allure.testcase('/fsm-platform/taskOrder/complete')
    @pytest.mark.two
    def test_complete4(self):
        self.sets_up()
        relust = ('FSMWOS03', 'FSMROS03', 'FSMWOS03', 'FSMTOS03', 'FSMIOS01', 'FSMROS03', 'WAIT_CONFIRM',
                  'FSMTOSOT05', 'FSMTOS03', 'FSMTOSOT05')

        appointment = Read_sql_Data.Conte(restule)
        appointment2 = Read_sql_Data.Conte(group_ip % appointment[0][1])
        data = {
            "key": appointment[0][0]
        }
        res = requests.get(url=self.taskOrder + str(appointment[0][0]), json=data, headers=self.headers)
        assert res.json()['code'] == 200
        # log_show(res, data)
        # print(res.json()['data'])

        datas = {
            "afterService": [self.afterService],
            "beforeService": [self.beforeService],
            "id": appointment[0][0],
            "operationInfo": res.json()['data']['typeDisplay'],
            "operationType": "FSMTOSOT05",
            "propValues": [
                {
                    "createTime": res.json()['data']['createTime'],
                    "createUser": res.json()['data']['createUser'],
                    "createUser_label": res.json()['data']['createUser_label'],
                    "groupId": str(appointment2[0][6]),
                    "id": str(appointment2[0][0]),
                    "isDelete": res.json()['data']['isDelete'],
                    "propId": str(appointment2[0][2]),
                    "propKeyType": str(appointment2[0][5]),
                    "propName": appointment2[0][7],
                    "propValue": appointment2[0][8],
                    "propValueId": str(appointment2[0][4]),
                    "requestOrderId": appointment2[0][1],
                    "updateTime": res.json()['data']['updateTime'],
                    "updateUser": res.json()['data']['updateUser'],
                    "updateUser_label": res.json()['data']['updateUser_label']
                },
                {

                    "createTime": res.json()['data']['createTime'],
                    "createUser": res.json()['data']['createUser'],
                    "createUser_label": res.json()['data']['createUser_label'],
                    "groupId": str(appointment2[1][6]),
                    "id": str(appointment2[1][0]),
                    "isDelete": appointment2[1][3],
                    "propId": str(appointment2[1][2]),
                    "propKeyType": appointment2[1][5],
                    "propName": appointment2[1][7],
                    "propValue": appointment2[1][8],
                    "propValueId": str(appointment2[1][4]),
                    "requestOrderId": str(appointment2[1][1]),
                    "updateTime": res.json()['data']['updateTime'],
                    "updateUser": res.json()['data']['updateUser'],
                    "updateUser_label": res.json()['data']['updateUser_label']
                }
            ],
            "remark": "到店未对设备经行维修",
            "serviceId": res.json()['data']['serviceId'],
            "serviceVersion": res.json()['data']['serviceVersion']

        }
        res = requests.post(url=self.url_use, json=datas, headers=self.headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        normal = Read_sql_Data.Conte(result_normal % appointment[0][0])
        assert relust == normal[0]
