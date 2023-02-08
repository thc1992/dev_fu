# encoding=utf-8
import random
from decimal import Decimal

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest


class Test_quote_save():
    def unitPrice(self, cityLevel, supplierid):
        if cityLevel == 'CITYL01':
            quote_price = supplierid[1]
        elif cityLevel == 'CITYL001':
            quote_price = supplierid[2]
        elif cityLevel == 'CITYL02':
            quote_price = supplierid[3]
        elif cityLevel == 'CITYL03':
            quote_price = supplierid[4]
        elif cityLevel == 'CITYL04':
            quote_price = supplierid[5]
        elif cityLevel == 'CITYL05':
            quote_price = supplierid[6]
        else:
            print("未匹配上")
        return quote_price

    # @classmethod
    def quote_save(self,quote_id):
        # SUPPLIER_TO_PLATFORM SUPPLIER_TO_BRAND  PLATFORM_TO_BRAND
        # 1、根据r_fee_quote的sumbit_time是否为空，选择未提交的数据
        # 检查每个任务单的数据是否正确 SUPPLIER_TO_PLATFORM
        sql_fee_data = Read_sql_Data.Conte(quote_save % str(quote_id))
        quote_id = sql_fee_data[0][0]
        task_order_id = sql_fee_data[0][1]
        request_order_id = sql_fee_data[0][3]
        work_order_id = sql_fee_data[0][4]
        supplier_id = sql_fee_data[0][5]
        contract_id = sql_fee_data[0][6]
        production_id = sql_fee_data[0][7]
        print(quote_id)
        print(task_order_id)
        print(supplier_id)
        print(work_order_id)
        # 2、校验基础配置,报价是否含税、日夜间、国定假日
        general = check_quote_general % \
        {'1': quote_id,'2': task_order_id}
        sql_check_quote_general = Read_sql_Data.Conte(general)
        sql_check_general_setting=Read_sql_Data.Conte(check_general_setting % str(task_order_id))
        dayNight = sql_check_general_setting[0][2]
        holidaysFestivals = sql_check_general_setting[0][3]
        urgencyDegree = sql_check_general_setting[0][4]
        profCode = sql_check_general_setting[0][1]
        cityLevel = sql_check_general_setting[0][5]
        city_id = sql_check_general_setting[0][6]
        area_id = sql_check_general_setting[0][6]
        quote_setting = sql_check_general_setting[0][9]
        company_id = sql_check_general_setting[0][8]
        settlement_setting = sql_check_general_setting[0][10]
        setting_id = sql_check_general_setting[0][11]
        print(cityLevel)
        print(dayNight)
        print(holidaysFestivals)
        print(urgencyDegree)
        print(profCode)
        # 校验基础数据
        assert sql_check_quote_general [0][0] == quote_setting
        assert sql_check_quote_general[0][1] == dayNight
        assert sql_check_quote_general[0][2] == holidaysFestivals

        # 查每张表的id
        work_summary_id = sql_check_quote_general[0][12]
        task_summary_id = sql_check_quote_general[0][13]
        sql_check_artificialfee = Read_sql_Data.Conte(general + ' %s' % "and t3.fee_code = 'ARTIFICIAL_FEE'")
        sql_check_measuresfee = Read_sql_Data.Conte(general + ' %s' % "and t3.fee_code = 'MEASURES_FEE'")
        sql_check_transportfee = Read_sql_Data.Conte(general + ' %s' % "and t3.fee_code = 'TRANSPORT_FEE'")
        sql_check_addtionalfee = Read_sql_Data.Conte(general + ' %s' % "and t3.fee_code = 'ADDITIONAL_FEE'")
        artificialfee_id = sql_check_artificialfee[0][14]
        measuresfee_id = sql_check_measuresfee[0][14]
        transportfee_id = sql_check_transportfee[0][14]
        addtional_id = sql_check_addtionalfee[0][14]
        prop_id = sql_check_addtionalfee[0][8]


        # 3.1校验附加费费用, 高空作业费
        additional_unitPrice = sql_check_addtionalfee[0][4]
        additional_num = sql_check_addtionalfee[0][6]
        addfee = [additional_unitPrice, float(additional_num)]
        check_addfee = Read_sql_Data.Conte(
            sql_check_prop_feedetail + str(task_order_id) + ' %s' % "and prop_key_type='PROPKT01'")
        assert addfee == [Decimal(check_addfee[0][2]), float('1')]

        # 3.2校验工时和单价
        # 工时，取hours
        quoteDetail_hours = Read_sql_Data.Conte(
            sql_check_prop_feedetail + str(task_order_id) + ' %s' % "and prop_key_type='PROPKT02'")
        # 单价，根据合约取值
        quoteDetail_value = sql_check_price % \
                            {'1': dayNight, '2': holidaysFestivals,
                             '3': urgencyDegree, '4': profCode,
                             '5': supplier_id,'6': task_order_id}
        check_quoteDetail = Read_sql_Data.Conte(quoteDetail_value)
        # 遍历取值，判断是否有厂商，没有厂商取平台数据,现在有合约厂商都有数据
        for supplierid in check_quoteDetail:
            if str(supplier_id) == supplierid[0]:
                unitPrice = self.unitPrice(cityLevel, supplierid)
                print(unitPrice)

            else:
                unitPrice = self.unitPrice(cityLevel, supplierid)
                print(unitPrice)
        print(unitPrice)
        # 根据基础配置，工时、单价，算出总价
        check_quote = (unitPrice, quoteDetail_hours[0][3], int(quoteDetail_hours[0][3]) * unitPrice)
        prop_unitprice = sql_check_artificialfee[0][4]
        prop_hours = sql_check_artificialfee[0][6]
        prop_price = sql_check_artificialfee[0][7]
        quoteDetailfee = (prop_unitprice,prop_hours,prop_price)

        assert quoteDetailfee == check_quote

        # 报价保存接口中的金额和数量皆取随机值
        # 附加费用数量，1或者0随机数
        additional_num = random.randint(0, 1)
        # 数量自由，0.5的倍数
        unitNum = random.randint(0, 5) * 0.5
        # 两位小数
        unit_price = round(random.uniform(50, 200), 2)
        # 整数
        num = random.randint(1, 10)
        material_total_price = round(unit_price * num, 2)
        art_total_price = round(float(prop_unitprice) * unitNum, 2)
        trans_totalPrice = round(random.uniform(50, 200), 2)
        measures_totalPrice = round(random.uniform(50, 200), 2)
        add_totalPrice = round(float(check_addfee[0][2]) * additional_num, 2)

        url_use = Read_yaml().yaml_show('host') + "/fsm-platform/fee/actual/taskOrder/submit"
        token = Read_yaml().yaml_show('access_token', 'token.yaml')
        headers = {
            "r-auth": token,
            "Content-Type": "application/json"
        }
        data = {
                "id": task_summary_id,
                "createUser": "",
                "createUser_label": "",
                "createTime": "",
                "updateUser": "",
                "updateUser_label": "",
                "updateTime": "",
                "isDelete": 0,
                "taskOrderId": task_order_id,
                "workOrderId": work_order_id,
                "requestOrderId": request_order_id,
                "artificialFee": "88.00",
                "materialFee": "0.00",
                "transportFee": None,
                "measuresFee": None,
                "additionalFee": "100.00",
                "dayNight": dayNight,
                "holidaysFestivals": holidaysFestivals,
                "workSummaryId": work_summary_id,
                "quoteId": quote_id,
                "submitFlag": "false",
                "taskCode": None,
                "urgencyDegree": None,
                "additionalQuoteList": [{
                    "id": addtional_id,
                    "createUser": "",
                    "createUser_label": "",
                    "createTime": "",
                    "updateUser": "",
                    "updateUser_label": "",
                    "updateTime": "",
                    "isDelete": 0,
                    "feeType": None,
                    "feeCode": "ADDITIONAL_FEE",
                    "feeName": "附加费用",
                    "parentId": None,
                    "materialId": None,
                    "materialName": None,
                    "unitPrice": check_addfee[0][2],
                    "unit": "个",
                    "num": additional_num,
                    "totalPrice": add_totalPrice,
                    "remark": None,
                    "taskSummaryId": task_summary_id,
                    "warrantyTime": None,
                    "specifications": None,
                    "assetName": None,
                    "articleNumber": None,
                    "propId": prop_id,
                    "propName": "高空作业",
                    "productionId": None,
                    "productionName": None,
                    "profCode": None,
                    "skillCode": None,
                    "cityId": None,
                    "areaId": None,
                    "dayNight": None,
                    "holidaysFestivals": None,
                    "urgencyDegree": None,
                    "cityLevel": None,
                    "key": ""
                }],
            "productionName": None,
            "generalConfig": {
            "id": setting_id,
            "createUser": "",
            "createUser_label": "",
            "createTime": "",
            "updateUser": "",
            "updateUser_label": "",
            "updateTime": "",
            "isDelete": 0,
            "companyId": company_id,
            "quoteSetting": quote_setting,
            "settlementSetting": settlement_setting,
            "settlementType": None,
            "sendDingAlarm": None
        },
            "contractId": contract_id,
            "quoteDetailList": [{
            "id": artificialfee_id,
            "createUser": "",
            "createUser_label": "",
            "createTime": "",
            "updateUser": "",
            "updateUser_label": "",
            "updateTime": "",
            "isDelete": 0,
            "feeType": None,
            "feeCode": "ARTIFICIAL_FEE",
            "feeName": "工时费",
            "parentId": None,
            "materialId": None,
            "materialName": None,
            "unitPrice": float(prop_unitprice),
            "unit": None,
            "num": unitNum,
            "totalPrice": art_total_price,
            "remark": None,
            "taskSummaryId": task_summary_id,
            "warrantyTime": None,
            "specifications": None,
            "assetName": None,
            "articleNumber": None,
            "propId": None,
            "propName": None,
            "productionId": production_id,
            "productionName": "空调维修自动化",
            "profCode": profCode,
            "skillCode": "FSMST01",
            "cityId": city_id,
            "areaId": area_id,
            "dayNight": dayNight,
            "holidaysFestivals": holidaysFestivals,
            "urgencyDegree": urgencyDegree,
            "cityLevel": cityLevel,
            "key": ""
        }],
            "materialDetailList": [{
            "assetName": "测试",
            "unitPrice": unit_price,
            "unit": "FSMSCU08",
            "num": num,
            "feeCode": "NON_STANDARD_MATERIAL",
            "feeName": "测试",
            "materialName": "测试",
            "totalPrice": material_total_price,
            "key": ""
        }],
            "otherFeeList": [{
            "id": transportfee_id,
            "createUser": "",
            "createUser_label": "",
            "createTime": "",
            "updateUser": "",
            "updateUser_label": "",
            "updateTime": "",
            "isDelete": 0,
            "feeType": None,
            "feeCode": "TRANSPORT_FEE",
            "feeName": "运输费",
            "parentId": None,
            "materialId": None,
            "materialName": None,
            "unitPrice": None,
            "unit": None,
            "num": None,
            "totalPrice": trans_totalPrice,
            "remark": None,
            "taskSummaryId": task_summary_id,
            "warrantyTime": None,
            "specifications": None,
            "assetName": None,
            "articleNumber": None,
            "propId": None,
            "propName": None,
            "productionId": None,
            "productionName": None,
            "profCode": None,
            "key": ""
        }, {
            "id": measuresfee_id,
            "createUser": "",
            "createUser_label": "",
            "createTime": "",
            "updateUser": "",
            "updateUser_label": "",
            "updateTime": "",
            "isDelete": 0,
            "feeType": None,
            "feeCode": "MEASURES_FEE",
            "feeName": "措施费",
            "parentId": None,
            "materialId": None,
            "materialName": None,
            "unitPrice": None,
            "unit": None,
            "num": None,
            "totalPrice": measures_totalPrice,
            "remark": None,
            "taskSummaryId": task_summary_id,
            "warrantyTime": None,
            "specifications": None,
            "assetName": None,
            "articleNumber": None,
            "propId": None,
            "propName": None,
            "productionId": None,
            "productionName": None,
            "profCode": None,
            "key": ""
            }]
        }
        res = requests.request(method="post", url=url_use, headers=headers, json=data)
        log_show(res, data)
        # 4、保存后，从表里取值；校验总价、附加费用、工时费
        # 校验task_summary费用；
        # 1、获取扣减金额
        discount = Read_sql_Data.Conte(total_discount % quote_id)[0][0]
        # 2、服务费总额和总金额
        service_fee = Read_sql_Data.Conte(total_fee % quote_id)[0][1]
        total_amount = Read_sql_Data.Conte(total_fee % quote_id)[1][1]
        # (1)判断优惠和扣减金额小于等于服务费总额，算出总金额（含税）-报价金额 = 税费
        if discount <= service_fee:
            withtax = Read_sql_Data.Conte(check_worksummary_withtax1 % \
                            {'1': quote_id, '2': quote_id})
        # (2)扣款金额和优惠金额大于服务费且小于总金额
        elif discount > service_fee and discount < total_amount :
            withtax = Read_sql_Data.Conte(check_worksummary_withtax2  % \
                            {'1': quote_id, '2': quote_id})
        # (3)扣款金额和优惠金额大于总金额，总金额、报价金额、税率为0
        elif discount >=  total_amount :
            withtax = Read_sql_Data.Conte(check_worksummary_withtax3  % \
                            {'1': quote_id, '2': quote_id})
        check_table_worksummary = Read_sql_Data.Conte(table_work_summary % quote_id)
        print(quote_id)
        assert check_table_worksummary == [(withtax[4][1], withtax[3][1],withtax[5][1], withtax[6][1],withtax[7][1], withtax[2][1],withtax[1][1], withtax[0][1])]
