# -*- coding: utf-8 -*-
# @Time    : 2020-02-20 20:36
# @Author  : XU
# @File    : test_search_company_sift_vip_module_01.py
# @Software: PyCharm

from common.operation import Operation, getimage
import unittest
from common.MyTest import MyTest
from Providers.sift.sift_opera import SiftOperation
from selenium.webdriver.common.by import By
from common.ReadData import Read_Ex
import random
from Providers.logger import Logger, error_format
from Providers.account.account import Account

log = Logger("查公司_高级筛选_03").getlog()


class Search_company_sift_vip(MyTest, Operation):
    """查公司_高级筛选_03"""

    a = Read_Ex()
    ELEMENT = a.read_excel("test_search_company_sift")
    account = Account()
    phone_vip = account.get_account("vip")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sift_opera = SiftOperation(cls.driver, cls.ELEMENT)
        cls.sift_opera.login_vip(cls.phone_vip, cls.account.get_pwd())

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.phone_vip, 'vip')
        super().tearDownClass()

    @getimage
    def test_001_cgs_gjsx_lxyx_p0(self):
        """查公司-搜索中间页，高级筛选:联系邮箱"""
        log.info(self.test_001_cgs_gjsx_lxyx_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_lxyx = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_lxyx_title", "more_lxyx", num_lxyx)
            result = self.sift_opera.basic4company(selectText, selectTarget)

            if num_lxyx == 1:  # 有邮箱
                self.assertEqual("true", result, "===失败-「有邮箱」，断言失败===")
            else:  # 无邮箱
                self.assertEqual("false", result, "===失败-「无邮箱」，断言失败===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgs_gjsx_sbxx_p0(self):
        """查公司-搜索中间页，高级筛选:商标信息"""
        log.info(self.test_002_cgs_gjsx_sbxx_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_sbxx = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_sbxx_title", "more_sbxx", num_sbxx)
            result = self.sift_opera.detail4company(selectText, "商标信息", selectTarget, num_sbxx)
            if num_sbxx == 1:
                # 断言-有商标信息
                self.assertTrue(result, "===失败-高级筛选：「{}」错误===".format(selectText))
            else:
                # 断言-无商标信息
                self.assertFalse(result, "===失败-高级筛选：「{}」错误===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
