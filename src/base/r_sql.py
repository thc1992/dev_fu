# encoding=utf-8
import os
import re

import pymysql, json
from datetime import date, datetime
import requests

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import r_idempotent
from src.read_yaml.read_yaml import Read_yaml
import pyautogui

user = 'root'
host = Read_yaml().yaml_show('mysql_db')['host']
passwd = Read_yaml().yaml_show('mysql_db')['password']
port = Read_yaml().yaml_show('mysql_db')['port']
# 打开数据库连接
db = pymysql.connect(host=host, user=user, password=passwd, port=port, charset='utf8mb4')

# 使用cursor（）方法创建一个游标对象cursor
cursor = db.cursor()


# 重新构造json类，遇到日期特殊处理，其余的用内置
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        else:
            return json.JSONEncoder.default(self, obj)


def get_result(sql):
    # 需要执行的sql语句
    # sql = "select  t1.id ,t2.store_id,t3.brand_id,  t4.request_type from rdp_system.r_user   t1 LEFT JOIN rdp_fsm.r_store_rel_user  t2   ON  t1.id=t2.user_id  LEFT JOIN rdp_fsm.r_store_info t3 ON t2.store_id=t3.id  LEFT JOIN  rdp_fsm.r_request_order t4 ON t3.brand_id=t4.brand_id WHERE  phone='18810007982'"
    # sql="select t1.id as work_order_id,t2.user_id from rdp_fsm.r_work_order t1 LEFT JOIN rdp_fsm.r_supplier_rel_user t2 LEFT JOIN rdp_system.r_user t3 on t2.user_id =t3.id on t1.supplier_id=t2.sup_id and t1.outlets_id = t2.outlet_id where t1.order_status='FSMWOS02'  and t2.user_type='engineer' and t2.is_delete=0 and t3.account ='18810007982' ORDER BY t1.create_time DESC"
    cursor.execute(sql)  # 使用execute（）方法执行sql语句
    data = cursor.fetchall()  # fetchall()使用接收全部的返回结果行（fetchone（）方法获取单条数据，
    cols = cursor.description  # 类似desc table_ame返回结果
    res = format_data(cols, data)
    cursor.close()
    db.close()  # 关闭数据库
    # json.dumps(): 对数据进行编码，转成json格式
    data_json = listToJson(res)  # indent默认无=不换行，0=换行；其余indent的值，代表缩进空格式；cls默认 = JSONEncoder
    # print(data_json)
    name = json.loads(data_json)
    # print(name['0'])
    # print(res[0])
    # print(data_json.replace('[','').replace(']',''))
    print(name)
    # print(json.loads(data_json))


# 数据格式化 cols字段名，data结果集
def format_data(cols, data):
    # 字段数组 形式['id', 'name', 'password']
    col = []  # 创建一个空列表以存放列名
    for i in cols:
        col.append(i[0])
    # 返回的数组集合 形式[{'id': 1, 'name': 'admin', 'password': '123456'}]
    res = []
    for iter in data:
        line_data = {}
        for index in range(0, len(col)):
            line_data[col[index]] = iter[index]
        res.append(line_data)
    return res


# list 转成Json格式数据
def listToJson(lst):
    import numpy as np
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, cls=ComplexEncoder, ensure_ascii=False)  # json转为string
    return str_json


# pro = '空调维修'
# name = "select * from rdp_fsm.r_work_order t1 LEFT JOIN rdp_fsm.r_supplier_rel_user t2 LEFT JOIN rdp_system.r_user t3 on t2.user_id =t3.id on t1.supplier_id=t2.sup_id and t1.outlets_id = t2.outlet_id where  t2.user_type='engineer' and t2.is_delete=0 and t3.account ='18810007982' and t1.create_time >'2022-09-10' ORDER BY t1.create_time DESC"
# get_result(name)


# userId = Read_yaml().yaml_show('login')['user_name']
# print(userId)
#
# print(sql_user_id %str(userId))
# user_id = Read_sql_Data.Conte(sql_user_id % str(userId))
#
# print(user_id)



