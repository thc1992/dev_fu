from src.list.test_02_01_place_order import *
from src.list.test_03_select_outlets import *
from src.list.test_04_handle import *
from src.list.test_05_time_appointment import *
from src.list.test_06_signIn_Check import *
from src.list.test_07_complete_result import *
from src.list.test_08_operation_confirm import *


class Test_process_all_order:
    @allure.description("整套流程跑测")
    @allure.suite('完成服务流程')
    @allure.title("完成服务流程")  # 测试用例的标题
    @pytest.mark.one
    def test_all_order(self):
        # 下单
        place_or = Test_place_order()
        place_or.test_order()
        # 选择服务商
        sel_out = Test_select_outlets()
        sel_out.test_select_lets2()
        # 派单
        t_hand = Test_handle()
        t_hand.test_handle()
        # 预约时间
        tt_appoin = Test_time_appointment()
        tt_appoin.test_appointment()
        # 签到
        t_signin = Test_signIn_Check()
        t_signin.test_signIn()
        # 工程师完成工单
        t_com = Test_complete_result()
        t_com.test_complete()
        # 门店确认工单完成
        op_con = Test_operation_confirm()
        op_con.test_operation_confirm()