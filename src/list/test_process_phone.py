from src.list.test_02_01_place_order import *
from src.list.test_03_select_outlets import *
from src.list.test_18_phone_complete import *


class Test_process_phone:
    @allure.description("整套流程跑测")
    @allure.suite('电话指导流程')
    @allure.title("电话指导流程")  # 测试用例的标题
    @pytest.mark.one
    def test_process_phone(self):
        # 下单
        place_or = Test_place_order()
        place_or.test_order()
        # 选择服务商
        sel_out = Test_select_outlets()
        sel_out.test_select_lets2()
        # 电话指导
        p_comple = Test_phone_complete()
        p_comple.test_phone_complete()
