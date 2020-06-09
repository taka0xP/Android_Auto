# -*- coding: utf-8 -*-
# @Time    : 2020-02-20 12:23
# @Author  : XU
# @File    : test_search_relation_sift_vip_module_01.py
# @Software: PyCharm

from common.operation import Operation, getimage
import unittest
from common.MyTest import MyTest
from Providers.sift.sift_opera import SiftOperation
from common.ReadData import Read_Ex
import random
from Providers.logger import Logger, error_format
from Providers.account.account import Account

log = Logger("查关系_高级筛选_03").getlog()


class Search_relation_sift_vip(MyTest, Operation):
    """查关系_高级筛选_03"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_relation")
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
    def test_001_cgx_gjsx_sxxx_p0(self):
        """查关系-搜索中间页，高级筛选:失信信息"""
        log.info(self.test_001_cgx_gjsx_sxxx_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_sxxx = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_sxxx_title", "more_sxxx", num_sxxx)
            result = self.sift_opera.detail4relation("失信信息", selectTarget, inputTarget, num_sxxx)
            if num_sxxx == 1:
                self.assertTrue(result, "===失败-高级筛选：「有失信信息」错误===")
            else:
                self.assertFalse(result, "===失败-高级筛选：「无失信信息」错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
