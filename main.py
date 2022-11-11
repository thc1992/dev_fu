#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest

from src.file_case.allure_report_data import AllureFileClean
from src.file_case.ding_talk import DingTalkSendMsg
from src.file_case.read_case import reader_pro
from src.read_yaml.read_yaml import *

if __name__ == '__main__':
    # args = ['-s, -q,--alluredir=allure-results']
    # args = []
    # case_list = get_case()
    # for item in case_list:
    #     args.append(str(item))
    # for i in args:
    # pytest.main(['-s', '-q', str(i), '--alluredir', 'allure-results', ])
    # pytest.main(['--alluredir', 'allure-results', ])
    # pytest.main(['-v', '-W', 'ignore:Module already imported:pytest.PytestWarning', str(i),
    #              '--alluredir', './report/tmp', "--clean-alluredir"])
    # 生成可视化报告
    pytest.main(
        ['-v', '-m', 'one', os.path.dirname(os.path.abspath(__file__)) + '/src/list', '--alluredir', './report/tmp',
         "--clean-alluredir"])
    reader_pro(os.path.dirname(os.path.abspath(__file__)))

    os.system(r"allure generate ./report/tmp -o ./report/html --clean")

    # 判断是否发送钉钉消息
    boole = Read_yaml().yaml_show('notification_type')
    if boole == 1:
        send_email = DingTalkSendMsg(AllureFileClean().get_case_count())
        send_email.send_ding_notification()
