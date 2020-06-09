#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/7
# @Author  : Soner
# @version : 1.0.0

import os
from random import randint
from Providers.logger import Logger

log = Logger("case_files").getlog()


class CaseFilses:
    def __init__(self, file_name="test_", ex_name=".py"):
        """
        模糊查找文件
        :param now_dir:
        :param test_dir:
        :param file_name: 文件名匹配搜索的关键字
        :param ex_name: 文件的扩展名
        :return:
        """
        self.jenkins_param = os.environ["run_cases"]
        self.now_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        test_dir = self.now_dir + "/testcase/"

        # 获取指定路径下的所有文件，包括子目录
        files = list()
        for root, dirs, file in os.walk(test_dir):
            for f in file:
                if f.startswith(file_name) and f.endswith(ex_name):
                   files.append(f[:-3])
        self.case_files = []
        if self.jenkins_param == "all":
            self.case_files = files
        elif self.jenkins_param == "" or None:
            raise Exception("jenkins构建传参错误，请检查！！！！")
        else:
            param_cases = self.jenkins_param.split(";")
            for s in files:
                for p in param_cases:
                    if p in s:
                        self.case_files.append(s)
        # 清空文件内容
        # with open(self.now_dir + "/config/case_file.txt", "w") as f:
        #     f.truncate()
        #
        # # 写入查找到的文件
        # for f in files:
        #     if f.startswith(file_name) and f.endswith(ex_name):
        #         self.case_files.append(f[:-3])
        #         with open(self.now_dir + "/config/case_file.txt", "a") as fil:
        #             fil.writelines("{}\n".format(f[:-3]))
        log.info("查找到的case文件列表：{}".format(self.case_files))

    def get_case_file(self):
        """
        随机获取一个文件
        """
        if self.case_files:
            count = len(self.case_files)
            random_num = randint(0, count - 1)
            case_file = self.case_files.pop(random_num)
            self._del_file(random_num)
            log.info("获取到用例文件：{}，并移除".format(case_file))
        else:
            case_file = None
            log.info("已经没有case文件")
        return case_file

    def _del_file(self, num):
        """
        删除最后一行文件
        """
        with open(self.now_dir + "/config/case_file.txt", "r") as f:
            files = f.readlines()
        files.pop(num)
        # 清空文件内容
        with open(self.now_dir + "/config/case_file.txt", "w") as f:
            f.truncate()
        for f in files:
            with open(self.now_dir + "/config/case_file.txt", "a") as fil:
                fil.writelines("{}".format(f))


if __name__ == "__main__":
    cases = CaseFilses()
    # for i in range(0, 1):
    #     cases.get_case_file()
    log.info(cases)
