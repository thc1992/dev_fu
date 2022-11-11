#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import allure

from src.base.modles import AllureAttachmentType
from src.read_yaml.read_yaml import Read_yaml


def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    """
    with allure.step(step):
        allure.attach(
            json.dumps(
                str(var),
                ensure_ascii=False,
                indent=4),
            step,
            allure.attachment_type.JSON)


def allure_attach(source: str, name: str, extension: str):
    """
    allure报告上传附件、图片、excel等
    :param source: 文件路径，相当于传一个文件
    :param name: 附件名称
    :param extension: 附件的拓展名称
    :return:
    """
    # 获取上传附件的尾缀，判断对应的 attachment_type 枚举值
    _name = name.split('.')[-1].upper()
    _attachment_type = getattr(AllureAttachmentType, _name, None)

    allure.attach.file(
        source=source,
        name=name,
        attachment_type=_attachment_type if _attachment_type is None else _attachment_type.value,
        extension=extension
    )


def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    with allure.step(step):
        pass


def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    with allure.step(step):
        pass


def log_show(res, datas, showlog=1):
    if showlog == 1:
        if Read_yaml().yaml_show('is_run'):
            _log_msg = f"\n==========================================================================\n" \
                       f"请求路径: {res.request.url}\n" \
                       f"请求方式: {res.request.method}\n" \
                       f"请求头:   {res.request.headers}\n" \
                       f"请求内容: {datas}\n" \
                       f"接口响应内容: {res.text}\n" \
                       f"Http状态码: {res.status_code}\n" \
                       "================================================================================="
            if res.status_code == 200:
                """ 在allure中记录请求数据 """
                allure_step_no(f"请求URL: {res.request.url}")
                allure_step_no(f"请求方式: {res.request.method}")
                allure_step("请求头: ", res.request.headers)
                allure_step("请求数据: ", datas)
                allure_step("响应结果: ", res.text)
                # 打印请求数据

                print('\n\033[92m' + f"请求URL: {res.request.url}")
                print('\033[92m' + f"请求方式: {res.request.method}")
                print('\033[92m' + f"请求头: {res.request.headers}")
                print('\033[92m' + f"请求数据: {datas}")
                print('\033[92m' + f"响应结果: {res.text}")

            else:
                """ 在allure中记录请求数据 """
                allure_step_no(f"请求URL: {res.request.url}")
                allure_step_no(f"请求方式: {res.request.method}")
                allure_step("请求头: ", res.request.headers)
                allure_step("请求数据: ", datas)
                allure_step("响应结果: ", res.text)

                print('\n\033[91m' + f"请求URL: {res.request.url}")
                print('\033[91m' + f"请求方式: {res.request.method}")
                print('\033[91m' + f"请求头: {res.request.headers}")
                print('\033[91m' + f"请求数据: {datas}")
                print('\033[91m' + f"响应结果: {res.text}")

        if "access_token" in res.json():
            json_str = {'access_token': res.json()['access_token']}
            # Read_yaml().write_yaml(json_str)
            old_data = Read_yaml().read_yaml_all('token.yaml')  # 读取文件数据
            old_data['access_token'] = json_str
            Read_yaml().update_yaml(old_data, 'token.yaml')
