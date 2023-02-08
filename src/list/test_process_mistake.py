from src.list.test_02_01_place_order import *
from src.list.test_03_select_outlets import *
from src.list.test_15_mistake_complete import *


class Test_process_mistake:
    @allure.description("整套流程跑测")
    @allure.suite('误发起完成流程')
    @allure.title("误发起完成流程")  # 测试用例的标题
    @pytest.mark.one
    def test_process_mistake(self):
        # 下单
        place_or = Test_place_order()
        place_or.test_order()
        # 选择服务商
        sel_out = Test_select_outlets()
        sel_out.test_select_lets2()
        # 误发起完成
        m_comple = Test_mistake_complete()
        m_comple.test_mistake_complete()