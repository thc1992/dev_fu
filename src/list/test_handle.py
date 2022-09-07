# encoding=utf-8
from src.base.Read_sql_Data import *
from src.base.R_idempotent import *
import allure
import re
class Test_handle():

    @allure.title("网点管理员派单")

    def setup_class(self):
        self.url = URL_link()
        # 数据库查询可派单work_order_id和人员
        sql_search="select t1.id as work_order_id,t2.user_id from rdp_fsm.r_work_order t1 LEFT JOIN rdp_fsm.r_supplier_rel_user t2 LEFT JOIN rdp_system.r_user t3 on t2.user_id =t3.id on t1.supplier_id=t2.sup_id and t1.outlets_id = t2.outlet_id where t1.order_status='FSMWOS02'  and t2.user_type='engineer' and t2.is_delete=0 and t3.account ='18810007982' ORDER BY t1.create_time DESC"
        self.list_sql_search = Read_sql_Data.Conte(self.url.HOST, self.url.PASSWD, self.url.PORT,sql_search)

    def teardown_class(self):
        pass
    @allure.description("派单")
    @allure.suite('派单')
    @allure.title("正常派单")  # 测试用例的标题
    @allure.testcase('/fsm-platform/operation/handle')
    def test_handle(self):
        work_order_id=self.list_sql_search[0][0]
        user_id = self.list_sql_search[0][1]
        # print(work_order_id)
        # print(user_id)
        url_use = self.url.BASE_URL+"/fsm-platform/operation/handle"
        headers = {
            "r-auth":read_token(),
            "Content-Type": "application/json",
            "r-idempotent":test_r_idempotent()
        }
        data={
                "operationType": "DISPATCH",
                "remark": "",
                "engineerId": user_id,
                "workOrderIds": [
                    work_order_id
                ]
            }
        res = requests.request(method="post", url=url_use, headers=headers, json=data)
        # print(res.text)
        # 1、检查r_request_order表order_status为FSMROS02（进行中）
        # 2、检查r_work_order表order_status为FSMWOS03（进行中）
        # 3、根据r_order的request_order_id+work_order_id查询，检查r_order表work_order_state为FSMWOS03，
        # 检查request_order_status为FSMROS02，current_stage_code为APPOINT_TIME，order_status（聚合订单状态）为FSMIOS01（进行中）
        # 4、根据r_task_order表request、work、task id关联r_task_order,task_status为FSMTOS01（待预约），engineer_id为入参值
        #     print(work_order_id)
        assert res.status_code == 200
        sql_check = "SELECT t2.order_status AS request_status,t1.order_status AS work_status,t3.work_order_state,t3.request_order_status,t3.current_stage_code,t3.order_status,t4.task_status,t4.engineer_id FROM rdp_fsm.r_work_order t1 LEFT JOIN rdp_fsm.r_request_order t2 ON t1.request_order_id = t2.id LEFT JOIN rdp_fsm.r_order t3 ON t1.id = t3.work_order_id  AND t1.request_order_id = t3.request_order_id LEFT JOIN rdp_fsm.r_task_order t4 ON t3.work_order_id = t4.work_order_id  AND t3.request_order_id = t4.request_order_id  AND t3.task_order_id = t4.id WHERE t1.id = " + str(
            work_order_id) + ""
        list_sql_check = Read_sql_Data.Conte(self.url.HOST, self.url.PASSWD, self.url.PORT, sql_check)
        assert list_sql_check[0] == (
        'FSMROS02', 'FSMWOS03', 'FSMWOS03', 'FSMROS02', 'APPOINT_TIME', 'FSMIOS01', 'FSMTOS01', user_id)
