# encoding=utf-8
import random
from decimal import Decimal

from src.Search.Sql_search import *
from src.base.Read_sql_Data import *
from src.base.request_Control import *
import allure
from src.read_yaml.read_yaml import Read_yaml
import pytest


class Test_quote_offer:
    def unitPrice(self, quoteDetail_cityLevel, supplierid):
        if quoteDetail_cityLevel == 'CITYL01':
            quote_price = supplierid[2]
        elif quoteDetail_cityLevel == 'CITYL001':
            quote_price = supplierid[3]
        elif quoteDetail_cityLevel == 'CITYL02':
            quote_price = supplierid[4]
        elif quoteDetail_cityLevel == 'CITYL03':
            quote_price = supplierid[5]
        elif quoteDetail_cityLevel == 'CITYL04':
            quote_price = supplierid[6]
        elif quoteDetail_cityLevel == 'CITYL05':
            quote_price = supplierid[7]
        else:
            print("未匹配上")
        return quote_price

    def fee_detail(self, quote_id, task_order_id, supplier_id):
        url = Read_yaml().yaml_show('host') + "/fsm-platform/fee/actual/taskOrder/detail"
        headers = {
            "r-auth": self.token,
            "Content-Type": "application/json"
        }
        data = {
            "taskOrderId": task_order_id,
            "quoteId": quote_id
        }
        res = requests.get(url=url, headers=headers, params=data)
        log_show(res, data)
        # print (res.json()['data'])
        data = res.json()['data']

        # 基础配置
        generalConfig = data['generalConfig']
        generalConfig_id = generalConfig['id']
        generalConfig_companyId = generalConfig['companyId']
        generalConfig_quoteSetting = generalConfig['quoteSetting']
        generalConfig_settlementSetting = generalConfig['settlementSetting']
        # print(generalConfig_companyId, generalConfig_quoteSetting, generalConfig_settlementSetting)

        # 保存过的才会有值，没有保存过为none，r_fee_task_summary
        # 所以需要判断，未保存，校验基础数据，保存过校验费用值，根据task_summary_id判断是否保存
        task_summary_id = data['id']
        taskOrderId = data['taskOrderId']
        workOrderId = data['workOrderId']
        requestOrderId = data['requestOrderId']
        artificialFee = data['artificialFee']
        materialFee = data['materialFee']
        transportFee = data['transportFee']
        measuresFee = data['measuresFee']
        additionalFee = data['additionalFee']
        # dayNight = data['dayNight']
        # holidaysFestivals = data['holidaysFestivals']
        workSummaryId = data['workSummaryId']
        quoteId = data['quoteId']
        # print(task_summary_id, taskOrderId, artificialFee, materialFee, transportFee, measuresFee, additionalFee)

        # 工时费
        quoteDetail = data['quoteDetailList'][0]
        quoteDetail_feedetailid = quoteDetail['id']
        quoteDetail_feeCode = quoteDetail['feeCode']
        # quoteDetail_feeName = quoteDetail['feeName']
        quoteDetail_unitPrice = quoteDetail['unitPrice']
        quoteDetail_num = quoteDetail['num']
        quoteDetail_totalPrice = quoteDetail['totalPrice']

        quoteDetail_productionName = quoteDetail['productionName']
        quoteDetail_profCode = quoteDetail['profCode']
        quoteDetail_dayNight = quoteDetail['dayNight']
        quoteDetail_holidaysFestivals = quoteDetail['holidaysFestivals']
        quoteDetail_urgencyDegree = quoteDetail['urgencyDegree']
        quoteDetail_cityLevel = quoteDetail['cityLevel']
        quoteDetail_cityId = quoteDetail['cityId']
        quoteDetail_areaId = quoteDetail['areaId']
        # print(quoteDetail_feeCode, quoteDetail_unitPrice, quoteDetail_num, quoteDetail_totalPrice,
        #       quoteDetail_productionName, quoteDetail_profCode, quoteDetail_dayNight, quoteDetail_holidaysFestivals,
        #       quoteDetail_urgencyDegree, quoteDetail_cityLevel, quoteDetail_cityId, quoteDetail_areaId)

        # 附加费
        additionalQuote = data['additionalQuoteList'][0]
        additionalQuote_feedetailid=additionalQuote['id']
        additionalQuote_feeCode = additionalQuote['feeCode']
        # additionalQuote_feeName = additionalQuote['feeName']
        additionalQuote_unitPrice = additionalQuote['unitPrice']
        additionalQuote_unit = additionalQuote['unit']
        additionalQuote_num = additionalQuote['num']
        additionalQuote_totalPrice = additionalQuote['totalPrice']
        additionalQuote_propId = additionalQuote['propId']
        additionalQuote_propName = additionalQuote['propName']
        # print(additionalQuote_feeCode, additionalQuote_unitPrice, additionalQuote_unit, additionalQuote_num,
        #       additionalQuote_totalPrice, additionalQuote_propId)

        # 运输费、交通费
        transportFee_id= data['otherFeeList'][0]['id']
        measuresFee_id= data['otherFeeList'][1]['id']

        # 材料费特殊处理，为none时，返回[]
        if data['materialDetailList'] == []:
            materialDetail_id = None
        else:
            materialDetail_id = data['materialDetailList'][0]['id']
        # 1、校验接口200
        assert res.status_code == 200
        # 2、校验基础配置校验
        general = [(quoteDetail_productionName, quoteDetail_profCode, quoteDetail_dayNight,
                    quoteDetail_holidaysFestivals, quoteDetail_urgencyDegree, quoteDetail_cityLevel,
                    int(quoteDetail_cityId), int(quoteDetail_areaId), int(generalConfig_companyId),
                    generalConfig_quoteSetting, generalConfig_settlementSetting)]
        check_general = Read_sql_Data.Conte(sql_check_general + str(task_order_id))
        assert general == check_general

        # 3、未保存，与基础数据匹配；
        if task_summary_id == None:
            # 3.1校验附加费费用,高空作业费
            # 不校验附加费总价是因为未保存时，接口没有返回total计算值
            addfee = [additionalQuote_unitPrice, additionalQuote_num]
            check_addfee = Read_sql_Data.Conte(
                sql_check_feedetail + str(task_order_id) + ' %s' % "and prop_key_type='PROPKT01'")
            assert addfee == [check_addfee[0][2], '1']
            # 3.2校验工时和单价
            # 接口返回的工时和单价
            quoteDetailfee = [(quoteDetail_unitPrice, Decimal(quoteDetail_num), quoteDetail_totalPrice)]
            # 工时，取hours
            quoteDetail_hours = Read_sql_Data.Conte(
                sql_check_feedetail + str(task_order_id) + ' %s' % "and prop_key_type='PROPKT02'")
            # print(quoteDetail_hours)
            # 单价，根据2、基础数据的值匹配，先匹配服务商，没有服务商匹配平台，最后再根据城市取值
            quoteDetail_value = sql_check_quoteDetail % \
                                {'1': quoteDetail_dayNight, '2': quoteDetail_holidaysFestivals,
                                 '3': quoteDetail_urgencyDegree, '4': quoteDetail_profCode}
            # 根据工时、单价，算出总价，与接口返回匹配
            check_quoteDetail = Read_sql_Data.Conte(quoteDetail_value)

            # 遍历取值，判断是否有厂商，没有厂商取平台数据
            for supplierid in check_quoteDetail:
                # print(quoteDetail_cityLevel)
                if str(supplier_id) == supplierid[0]:
                    unitPrice = self.unitPrice(quoteDetail_cityLevel, supplierid)

                else:
                    unitPrice = self.unitPrice(quoteDetail_cityLevel, supplierid)

            check_quote = [(unitPrice, (quoteDetail_hours[0][3]), int(quoteDetail_hours[0][3]) * unitPrice)]

            assert quoteDetailfee == check_quote

        # 4、保存后，从表里取值；校验总价、附加费用、工时费
        else:
            # 校验task_summary费用；
            feesummary=[(int(task_summary_id), int(taskOrderId), artificialFee, materialFee, transportFee, measuresFee, additionalFee)]
            check_feesummary = Read_sql_Data.Conte(sql_check_feesummary + str(task_order_id))
            # print(feesummary)
            # print(check_feesummary)
            assert feesummary == check_feesummary

        # 返回json，作为下个接口的入参
        json_str={"task_summary_id":task_summary_id, "taskOrderId":taskOrderId,"workOrderId":workOrderId, "requestOrderId":requestOrderId, "workSummaryId":workSummaryId, "quoteId":quoteId, "additionalQuote_feedetailid":additionalQuote_feedetailid, "additionalQuote_unitPrice":additionalQuote_unitPrice, "additionalQuote_unit":additionalQuote_unit, "additionalQuote_propId":additionalQuote_propId, "additionalQuote_propName":additionalQuote_propName, "generalConfig_id":generalConfig_id, "generalConfig_companyId":generalConfig_companyId, "generalConfig_quoteSetting":generalConfig_quoteSetting, "generalConfig_settlementSetting":generalConfig_settlementSetting, "quoteDetail_feedetailid":quoteDetail_feedetailid, "quoteDetail_unitPrice":quoteDetail_unitPrice, "quoteDetail_productionName":quoteDetail_productionName, "quoteDetail_profCode":quoteDetail_profCode, "quoteDetail_cityId":quoteDetail_cityId, "quoteDetail_areaId":quoteDetail_areaId, "quoteDetail_dayNight":quoteDetail_dayNight, "quoteDetail_holidaysFestivals":quoteDetail_holidaysFestivals, "quoteDetail_urgencyDegree":quoteDetail_urgencyDegree, "quoteDetail_cityLevel":quoteDetail_cityLevel, "materialDetail_id":materialDetail_id, "transportFee_id":transportFee_id, "measuresFee_id":measuresFee_id}

        return json_str


    def quote_save(self):
        # print(sql_check)
        self.token = Read_yaml().yaml_show('access_token', 'token.yaml')
        self.nomal_report = Read_yaml().yaml_show('nomal_report')
        if self.nomal_report:
            quoteId_data = Read_sql_Data.Conte(
                quoteId + "  and  t1.work_order_id = '%s'" % Read_yaml().yaml_show('workOrderId', 'token.yaml'))[0][0]
        else:
            quoteId_data = Read_sql_Data.Conte(quoteId)[0][0]

        # quoteId_data = Read_sql_Data.Conte(quoteId)[0][0]
        # print(quoteId_data)
        sql_fee_data = Read_sql_Data.Conte(result_quoteId + str(quoteId_data))
        # print(sql_fee_data)
        for i in  range(len(sql_fee_data)):
            quote_id = sql_fee_data[0][0]
            task_order_id = sql_fee_data[i][1]
            supplier_id = sql_fee_data[i][5]
            # print(quote_id, task_order_id,supplier_id)
            print(task_order_id)
            # 调detail接口先校验
            fee_data=self.fee_detail(quote_id, task_order_id, supplier_id)
            # 数量自由，1或者0随机数
            additional_num=random.randint(0,1)
            # 数量自由，0.5的倍数
            unitNum=random.randint(0,5)*0.5
            # 两位小数
            unitPrice=round(random.uniform(50,200),2)
            # 整数
            num=random.randint(1,10)
            material_total_price=round(unitPrice * num, 2)
            art_total_price=round(float(fee_data['quoteDetail_unitPrice']) * unitNum,2)
            trans_totalPrice=round(random.uniform(50,200),2)
            measures_totalPrice=round(random.uniform(50,200),2)
            add_totalPrice=round(float(fee_data['additionalQuote_unitPrice']) * additional_num,2)
            # 调用保存接口
            self.url_use = Read_yaml().yaml_show('host') + "/fsm-platform/fee/actual/taskOrder/submit"
            self.headers = {
                "r-auth": self.token,
                "Content-Type": "application/json",
                "r-idempotent": r_idempotent(self.token, "feeTaskOrder")
            }
            data = {
                    "id": fee_data['task_summary_id'],
                    "createUser": None,
                    "createTime": None,
                    "updateUser": None,
                    "updateTime": None,
                    "isDelete": None,
                    "taskOrderId": task_order_id,
                    "workOrderId": fee_data['workOrderId'],
                    "requestOrderId": fee_data['requestOrderId'],
                    "artificialFee": None,
                    "materialFee": None,
                    "trafficFee": None,
                    "stayFee": None,
                    "transportFee": None,
                    "measuresFee": None,
                    "additionalFee": None,
                    "dayNight": None,
                    "holidaysFestivals": None,
                    "workSummaryId": fee_data['workSummaryId'],
                    "quoteId": quote_id,
                    "taskCode": None,
                    "urgencyDegree": None,
                    "additionalQuoteList": [
                    {
                        "id": fee_data['additionalQuote_feedetailid'],
                        "createUser": None,
                        "createTime": None,
                        "updateUser": None,
                        "updateTime": None,
                        "isDelete": None,
                        "feeType": None,
                        "feeCode": "ADDITIONAL_FEE",
                        "feeName": "附加费用",
                        "parentId": None,
                        "materialId": None,
                        "materialName": None,
                        "unitPrice": fee_data['additionalQuote_unitPrice'],
                        "unit": fee_data['additionalQuote_unit'],
                        # 生成1或者0整数
                        "num": additional_num,
                        # 结算结果,单价*数量
                        "totalPrice":add_totalPrice ,
                        "remark": None,
                        "taskSummaryId": fee_data['task_summary_id'],
                        "warrantyTime": None,
                        "specifications": None,
                        "assetName": None,
                        "articleNumber": None,
                        "propId": fee_data['additionalQuote_propId'],
                        "propName": fee_data['additionalQuote_propName'],
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
                        "key": None
                        }
                    ],
                    "productionName": None,
                    "generalConfig": {
                        "id": fee_data['generalConfig_id'],
                        "createUser": None,
                        "createUser_label": None,
                        "createTime": None,
                        "updateUser": None,
                        "updateUser_label": None,
                        "updateTime": None,
                        "isDelete": None,
                        "companyId": fee_data['generalConfig_companyId'],
                        "quoteSetting": fee_data['generalConfig_quoteSetting'],
                        "settlementSetting": fee_data['generalConfig_settlementSetting'],
                        "settlementType": None,
                        "sendDingAlarm": None
                    },
                    "quoteDetailList": [
                    {
                        "id": fee_data['quoteDetail_feedetailid'],
                        "createUser": None,
                        "createTime": None,
                        "updateUser": None,
                        "updateTime": None,
                        "isDelete": None,
                        "feeType": None,
                        "feeCode": "ARTIFICIAL_FEE",
                        "feeName": "工时费",
                        "parentId": None,
                        "materialId": None,
                        "materialName": None,
                        "unitPrice": fee_data['quoteDetail_unitPrice'],
                        "unit": None,
                        # 数量是0.5的倍数，可以为0
                        "num": unitNum,
                        # 工时*单价，计算总额
                        "totalPrice": art_total_price,
                        "remark": None,
                        "taskSummaryId": fee_data['task_summary_id'],
                        "warrantyTime": None,
                        "specifications": None,
                        "assetName": None,
                        "articleNumber": None,
                        "propId": None,
                        "propName": None,
                        "productionId": None,
                        "productionName": fee_data['quoteDetail_productionName'],
                        "profCode": fee_data['quoteDetail_profCode'],
                        "skillCode": None,
                        "cityId": fee_data['quoteDetail_cityId'],
                        "areaId": fee_data['quoteDetail_areaId'],
                        "dayNight": fee_data['quoteDetail_dayNight'],
                        "holidaysFestivals": fee_data['quoteDetail_holidaysFestivals'],
                        "urgencyDegree": fee_data['quoteDetail_urgencyDegree'],
                        "cityLevel": fee_data['quoteDetail_cityLevel'],
                        "key": ""
                        }
                    ],
                    "materialDetailList": [
                    {
                        "id": fee_data['materialDetail_id'],
                        "createUser": None,
                        "createUser_label": None,
                        "createTime": None,
                        "updateUser": None,
                        "updateUser_label": None,
                        "updateTime": None,
                        "isDelete": None,
                        "feeType": None,
                        "feeCode": "NON_STANDARD_MATERIAL",
                        "feeName": "额外材料费",
                        # 自定义
                        "parentId": None,
                        "materialId": None,
                        "materialName": "额外材料费",
                        # 1-200之间，保留两位小数
                        "unitPrice": unitPrice,
                        "unit": "FSMSCU08",
                        # 1-10的整数
                        "num": num,
                        "totalPrice": material_total_price,
                        "remark": None,
                        "taskSummaryId": fee_data['task_summary_id'],
                        "warrantyTime": None,
                        "specifications": None,
                        "assetName": "额外材料费",
                        "articleNumber": None,
                        "propId": None,
                        "propName": None,
                        "productionId": None,
                        "productionName": None,
                        "profCode": None,
                        "key": ""
                        }
                    ],
                    "otherFeeList": [
                    {
                        "id": fee_data['transportFee_id'],
                        "createUser": None,
                        "createTime": None,
                        "updateUser": None,
                        "updateTime": None,
                        "isDelete": None,
                        "feeType": None,
                        "feeCode": "TRANSPORT_FEE",
                        "feeName": "运输费",
                        "parentId": None,
                        "materialId": None,
                        "materialName": None,
                        "unitPrice": None,
                        "unit": None,
                        "num": None,
                        # 自定义，两位小数
                        "totalPrice": trans_totalPrice,
                        "remark": "运输费用收取",
                        "taskSummaryId": None,
                        "warrantyTime": None,
                        "specifications": None,
                        "assetName": None,
                        "articleNumber": None,
                        "propId": None,
                        "propName": None,
                        "productionId": None,
                        "productionName": None,
                        "profCode": None,
                        "key": None
                    },
                    {
                        "id": fee_data['measuresFee_id'],
                        "createUser": None,
                        "createTime": None,
                        "updateUser": None,
                        "updateTime": None,
                        "isDelete": None,
                        "feeType": None,
                        "feeCode": "MEASURES_FEE",
                        "feeName": "措施费",
                        "parentId": None,
                        "materialId": None,
                        "materialName": None,
                        "unitPrice": None,
                        "unit": None,
                        "num": None,
                        # 自定义，两位小数
                        "totalPrice": measures_totalPrice,
                        "remark": "措施费用收取",
                        "taskSummaryId": None,
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
                        }
                    ]
                }

            res = requests.request(method="post", url=self.url_use, headers=self.headers, json=data)
            # log_show(res, data)
            assert res.status_code == 200
            data = res.json()['data']
            task_summary_id=data['id']
            # 判断r_fee_detail的数据正确性
            check_detail = Read_sql_Data.Conte(sql_check_detail +str(task_summary_id))
            # print(check_detail)
            for feecode in check_detail:
                if feecode[0] == "NON_STANDARD_MATERIAL" :
                    fee=[unitPrice,"FSMSCU08",float(num),material_total_price]
                    result=[feecode[2],feecode[3],feecode[4],feecode[5]]
                    assert fee ==result
                elif feecode[0] == "ARTIFICIAL_FEE":
                    fee=[float(fee_data['quoteDetail_unitPrice']),unitNum,art_total_price]
                    result=[feecode[2], feecode[4],feecode[5]]
                    assert fee == result
                elif feecode[0] == "TRANSPORT_FEE" :
                    fee=[trans_totalPrice,"运输费用收取"]
                    result=[feecode[5],feecode[6]]
                    assert fee == result
                elif feecode[0] == "MEASURES_FEE" :
                    fee=[measures_totalPrice,"措施费用收取"]
                    result=[feecode[5],feecode[6]]
                    assert fee == result
                elif feecode[0] == "ADDITIONAL_FEE" :
                    fee=[float(fee_data['additionalQuote_unitPrice']), fee_data['additionalQuote_unit'], float(additional_num),add_totalPrice]
                    result=[feecode[2],feecode[3],feecode[4],feecode[5]]
                    assert fee == result
                else:
                   print("未匹配上")
            # 校验r_fee_task_summary数据
            # 同样改成当前接口的返回值
            check_table_task_summary = Read_sql_Data.Conte(table_task_summary + str(task_summary_id))
            check_sql_task_summary = Read_sql_Data.Conte(sql_task_summary % str(task_summary_id))
            assert check_table_task_summary==[(check_sql_task_summary[0][2],check_sql_task_summary[1][2],check_sql_task_summary[2][2],check_sql_task_summary[3][2],check_sql_task_summary[4][2])]

            # 校验r_fee_work_summary数据
            check_table_worksummary = Read_sql_Data.Conte(table_work_summary + str(quote_id))
            # print(check_table_worksummary)
            # 报价含税
            if fee_data['generalConfig_quoteSetting'] =='QTSET01':
                check_worksummary_withtax = Read_sql_Data.Conte(sql_worksummary_withtax % str(quote_id))
                # print(check_worksummary_withtax)
                assert check_table_worksummary ==[(check_worksummary_withtax[1][1],check_worksummary_withtax[0][1],check_worksummary_withtax[4][1],check_worksummary_withtax[5][1],check_worksummary_withtax[6][1],check_worksummary_withtax[9][1],check_worksummary_withtax[10][1],check_worksummary_withtax[11][1])]

            # 报价不含税02
            else:
                check_worksummary_withnotax = Read_sql_Data.Conte(sql_worksummary_withnotax % str(quote_id))
                # print(check_worksummary_withnotax)
                assert check_table_worksummary == [(check_worksummary_withnotax[1][1], check_worksummary_withnotax[0][1],check_worksummary_withnotax[4][1], check_worksummary_withnotax[5][1],check_worksummary_withnotax[6][1], check_worksummary_withnotax[9][1],check_worksummary_withnotax[10][1], check_worksummary_withnotax[11][1])]
            # 获取提交接口入参
            quote_submit = Read_sql_Data.Conte(table_quote_submit + str(quote_id))
            # print(quote_submit)
        return quote_submit

    @allure.description("查看详情")
    @allure.suite('报价')
    @allure.title("报价")  # 测试用例的标题
    @allure.testcase('/fsm-platform/fee/actual/workOrder/submit')
    @pytest.mark.one
    def test_quote_submit(self):
        quote_submit = self.quote_save()
        print(quote_submit)
        url_use = Read_yaml().yaml_show('host') + "/fsm-platform/fee/actual/workOrder/submit"
        token = Read_yaml().yaml_show('access_token', 'token.yaml')
        headers = {
            "r-auth": token,
            "Content-Type": "application/json"
        }
        data = {
            "id": quote_submit[0][0],
            "workOrderId": quote_submit[0][2],
            "requestOrderId": quote_submit[0][1],
            "quoteId": quote_submit[0][3]
        }
        res = requests.request(method="post", url=url_use, headers=headers, json=data)
        assert res.status_code == 200
        log_show(res, data)
        quoteId = quote_submit[0][3]
        print (quoteId)
        list_sql_check = Read_sql_Data.Conte(check_quote_submit + str(quote_submit[0][3]))
        assert list_sql_check == [('APPLY', 'HAS_QUOTE', 1)]


