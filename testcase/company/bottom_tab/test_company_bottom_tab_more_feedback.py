#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31
# @Author  : Soner
# @version : 1.0.0

import unittest
import time

from selenium.webdriver.common.by import By
from random import randint
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from common.operation import Operation
from common.operation import getimage
from Providers.logger import Logger, error_format
from Providers.company.company import CompanyFunc
from Providers.account.account import Account
from Providers.random_str.random_str import RandomStr

log = Logger("公司底部TAB_更多_反馈").getlog()


class CompanyBottomTabMoreFeedback(MyTest):
    """
    公司底部TAB_更多_反馈
    """
    a = Read_Ex()
    ELEMENT = a.read_excel("company_bottom_tab")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.operation = Operation(cls.driver)
        cls.company = CompanyFunc(cls.driver, cls.ELEMENT)
        cls.account = Account()
        cls.company_name = '四川同辉实业有限公司'
        cls.rand_str = RandomStr()

    @getimage
    def test_gfxx_tab_fk_0001(self):
        "纠错反馈页面，校验公司名是否是进入的公司名"
        log.info(self.test_gfxx_tab_fk_0001.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 反馈
            self.company.click_tab(more_local, y_proportion=50)
            # 获取 纠错页面 公司名
            new_company_name = self.operation.new_find_element(By.ID, self.ELEMENT['feedback_company_name']).text
            self.assertEqual(self.company_name, new_company_name,
                             "预期公司名称：{}，实际公司名称：{}".format(self.company_name, new_company_name))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_fk_0002(self):
        "纠错反馈页面，校验问题描述最多300字，提交，toast“提交成功”"
        log.info(self.test_gfxx_tab_fk_0002.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 反馈
            self.company.click_tab(more_local, y_proportion=50)
            # 输入 问题描述
            self.operation.adb_send_input(By.ID, self.ELEMENT['feedback_content_et'],
                                          self.rand_str.zh_cn(300), self.device)
            # 校验 字数
            content_text = self.operation.new_find_element(By.ID, self.ELEMENT['feedback_content_length']).text
            text = "300/300"
            self.assertEqual(text, content_text, "预期文本：{}，实际文本：{}".format(text, content_text))
            content_len = len(self.operation.new_find_element(By.ID, self.ELEMENT['feedback_content_et']).text)
            self.assertTrue(content_len == 300, "实际输入内容长度：{}".format(content_len))
            # 校验 toast
            self.operation.new_find_element(By.ID, self.ELEMENT['feedback_content_btn']).click()
            toast = self.operation.get_toast()
            toast_text = "提交成功"
            self.assertEqual(toast_text, toast, "预期toast：{}，实际toast：{}".format(toast_text, toast))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_fk_0003(self):
        "纠错反馈页面，校验 问题描述为必填项、图片最多上传3张"
        log.info(self.test_gfxx_tab_fk_0003.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 反馈
            self.company.click_tab(more_local, y_proportion=50)
            # 校验 描述是否为必填项 toast
            self.operation.new_find_element(By.ID, self.ELEMENT['feedback_content_btn']).click()
            toast = self.operation.get_toast()
            content_toast = "请填写问题描述"
            self.assertEqual(content_toast, toast, "预期toast：{}，实际toast：{}".format(content_toast, toast))
            # 点击 上传图片
            self.operation.new_find_element(By.ID, self.ELEMENT['up_pic']).click()
            self.company.up_pic(3)
            self.operation.new_find_element(By.ID, self.ELEMENT['feedback_content_btn']).click()
            toast = self.operation.get_toast()
            toast_text = "请填写问题描述"
            self.assertEqual(toast_text, toast, "预期toast：{}，实际toast：{}".format(toast_text, toast))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e


if __name__ == '__main__':
    unittest.main()
