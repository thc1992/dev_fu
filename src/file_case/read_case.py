# -*- coding: utf-8 -*-

import os
import time

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fileList = []
unExcuteFileList = []


def get_case():
    """
    获取用例
    :return:list_case
    """
    path_lst = os.path.dirname(os.path.abspath(__file__)) + "/../common/execute.txt"
    with open(path_lst, 'r') as file:
        content_list = file.readlines()
        list_case = [os.path.join(root_path, line.strip()) for line in content_list if line.strip()]
        file.close()
    list_case.sort()
    return list_case


def path_file(file_path):
    """
        判断文件是否属于不可执行文件
        :param file_path:测试脚本路径
        :return:属于不可执行返回False
        """
    for unExcuteFile in unExcuteFileList:
        if unExcuteFile in file_path or '.py' not in file_path:
            return False
    return True


def get_run_file(dir_path):
    """
            筛选出可执行脚本
            :param dir_path:脚本目录
            """
    list_file2 = []
    list_file = os.listdir(dir_path)  # 列出文件夹下所有的目录与文件
    # print(list_file)
    for name in list_file:
        if name.endswith('py'):
            list_file2.append(name)
        else:
            list_file.remove(name)
    for index in range(0, len(list_file)):
        file_path = os.path.join(dir_path, list_file[index])
        if os.path.isfile(file_path):
            if path_file(file_path):
                fileList.append(file_path)
                # print(file_path)
        elif os.path.isdir(file_path):
            get_run_file(file_path)


def generate_excute_file(file_path):
    """
    将可以跑测的case写入到文件中
    :param file_path: 验证路径
    :return:
    """
    if os.path.isdir(file_path):
        get_run_file(file_path)
        with open(os.path.dirname(os.path.abspath(__file__)) + "/../common/execute.txt", "w+",
                  encoding='utf-8') as File:
            for filePath in fileList:
                File.writelines(filePath + '\n')
            File.close()
        time.sleep(1)


def reader_pro(path):
    """
    环境显示
    """
    with open(path + '/environment.properties', 'r') as f:
        with open(path + '/report/tmp/environment.properties', 'w+', encoding='utf-8') as file:
            for i in f.readlines():
                file.writelines(i)
            file.close()
        f.close()
