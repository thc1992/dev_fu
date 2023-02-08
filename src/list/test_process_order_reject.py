from src.list.test_02_01_place_order import *
from src.list.test_03_select_outlets import *
from src.list.test_04_handle import *
from src.list.test_20_order_reject import *


class Test_process_order_reject:
    @allure.description("整套流程跑测")
    @allure.suite('拒绝工单流程')
    @allure.title("拒绝工单流程")  # 测试用例的标题
    @pytest.mark.one
    def test_process_order_reject(self):
        # 下单
        place_or = Test_place_order()
        place_or.test_order()
        # 选择服务商
        sel_out = Test_select_outlets()
        sel_out.test_select_lets2()
        # 派单
        t_hand = Test_handle()
        t_hand.test_handle()

        # 拒绝工单
        re = Test_order_reject()
        re.test_order_reject()
