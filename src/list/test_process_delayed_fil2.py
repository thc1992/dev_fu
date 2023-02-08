from src.list.test_02_01_place_order import *
from src.list.test_03_select_outlets import *
from src.list.test_04_handle import *
from src.list.test_11_delayed_filing import *
from src.list.test_12_delay_time import *


class Test_process_delayed_fil:
    @allure.description("整套流程跑测")
    @allure.suite('延迟申请通过流程')
    @allure.title("延迟申请通过流程")  # 测试用例的标题
    @pytest.mark.one
    def test_process_delayed_fil2(self):

        # 下单
        place_or = Test_place_order()
        place_or.test_order()
        # 选择服务商
        sel_out = Test_select_outlets()
        sel_out.test_select_lets2()
        # 派单
        t_hand = Test_handle()
        t_hand.test_handle()
        # 延迟申请
        d_fil = Test_delayed_fil()
        d_fil.test_delayed()
        # 延迟通过
        d_time = Test_delay_time()
        d_time.test_delay2()
