# encoding=utf-8
import os
import time

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest
import json


class Test_order_evaluate:
    def change_type(byte):
        if isinstance(byte, bytes):
            return str(byte, encoding="utf-8")
        return json.JSONEncoder.default(byte)

    def get_evaluate(self):
        appointment = Read_sql_Data.Conte(check_evaluate)
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        # 获取评价单数据
        self.detail = Read_yaml().yaml_show('host') + "/fsm-platform/evaluation/detail"
        headers = {
            "r-auth": self.token,
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
        }
        datas = {
            "requestOrderId": appointment[0][0]
        }
        res = requests.get(url=self.detail, headers=headers, params=datas)
        # log_show(res, datas)
        assert res.json()['code'] == 200
        with open("test.json", 'w', encoding='utf-8') as load_f:
            load_f.write(str(res.json()['data']))
            load_f.close()
        with open("test.json", 'r', encoding='utf-8') as load_fs:
            name = load_fs.read()
            load_dict = json.dumps(name, ensure_ascii=False)
            json_data = eval(json.loads(load_dict))
            json_data[0]['remark'] = "维修的很理想"
            for i in range(len(json_data[0]['items'])):
                json_data[0]['items'][i]['score'] = 100
            print(len(json_data[0]['taskEvaluations']))
            if len(json_data[0]['taskEvaluations']) == 1:
                json_data[0]['taskEvaluations'][0]['remark'] = "维修人员很负责"
                for i in range(len(json_data[0]['taskEvaluations'][0]['items'])):
                    json_data[0]['taskEvaluations'][0]['items'][i]['score'] = 100
                load_fs.close()
        with open("test.json", 'w', encoding='utf-8') as load_f:
            json.dump(json_data, load_f, ensure_ascii=False)
            load_f.close()
        with open("test.json", 'r', encoding='utf-8') as load_fs:
            name = load_fs.read()
            load_dict = json.dumps(name, ensure_ascii=False)
            return eval(load_dict), appointment[0][0]
            load_fs.close()
        # return res.json()['data'], '644868054068494336'

    @allure.description("工单评价")
    @allure.suite('评价')
    @allure.title("评价")  # 测试用例的标题
    @allure.testcase('/fsm-platform/evaluation/submit')
    @pytest.mark.two
    def test_order_evaluate(self):
        evaluate = self.get_evaluate()
        assert len(json.loads(evaluate[0])) == Read_sql_Data.Conte(evalue_num % evaluate[1])[0][0]
        assert len(json.loads(evaluate[0])[0]['taskEvaluations']) == Read_sql_Data.Conte(order_num % evaluate[1])[0][0]
        self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/evaluation/submit"
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json",
            "Authorization": "Basic ZnNtX3N0b3JlX21vYmlsZTpmc21fc3RvcmVfbW9iaWxlX3NlY3JldA==",
        }
        datas = {
            "requestOrderId": evaluate[1],
            "list": json.loads(evaluate[0]),
        }
        res = requests.post(url=self.url_use, json=datas, headers=headers)
        log_show(res, datas)
        assert res.json()['code'] == 200
        num = Read_sql_Data.Conte(check_evslute % evaluate[1])
        assert num[0][0] > 0
        os.remove('test.json')
