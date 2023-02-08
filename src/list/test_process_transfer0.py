# encoding=utf-8
from src.list.test_01_01_login import *
from src.list.test_02_01_place_order import *
from src.list.test_03_select_outlets import *
from src.list.test_04_handle import Test_handle
from src.list.test_13_transfer_order import *
from src.list.test_14_transfer_handle import *


class Test_process_transfer:
    @allure.description("整套流程跑测")
    @allure.suite('转单流程')
    @allure.title("转单流程")  # 测试用例的标题
    @pytest.mark.one
    def test_process_transfer0(self):
        # 下单
        place_or = Test_place_order()
        place_or.test_order()
        # 选择服务商
        sel_out = Test_select_outlets()
        sel_out.test_select_lets2()
        # 转单
        trans = Test_transfer_order()
        trans.test_transfer_order()
