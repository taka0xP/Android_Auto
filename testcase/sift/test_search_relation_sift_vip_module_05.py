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

log = Logger("查关系_高级筛选_05").getlog()


class Search_relation_sift_vip(MyTest, Operation):
    """查关系_高级筛选_05"""

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
    def test_001_cgx_gjsx_rjzzq_p0(self):
        """查关系-搜索中间页，高级筛选:软件著作权"""
        log.info(self.test_001_cgx_gjsx_rjzzq_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_rjzzq = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_rjzzq_title", "more_rjzzq", num_rjzzq)
            result = self.sift_opera.detail4relation("著作权", selectTarget, inputTarget, num_rjzzq)
            if num_rjzzq == 2 and not result:
                # 断言-详情页「著作权」维度无数据时
                self.assertFalse(result, "===失败-高级筛选：「无软件著作权」错误===")
            else:
                if num_rjzzq == 1:
                    # 断言-「有软件著作权」
                    log.info("软件著作权：{}个".format(result))
                    self.assertNotEqual(0, result, "===失败-高级筛选：「有软件著作权」错误===")
                else:
                    # 断言-详情页「有作品著作权」，「无软件著作权」
                    self.assertEqual(0, result, "===失败-高级筛选：「无软件著作权」错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_gjsx_rzxx_p0(self):
        """查关系-搜索中间页，高级筛选:融资信息"""
        log.info(self.test_002_cgx_gjsx_rzxx_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_rzxx = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_rzxx_title", "more_rzxx", num_rzxx)
            result = self.sift_opera.detail4relation("融资历程", selectTarget, inputTarget, num_rzxx)
            if num_rzxx == 1:
                self.assertTrue(result, "===失败-高级筛选：「有融资历程」错误===")
            else:
                self.assertFalse(result, "===失败-高级筛选：「无融资历程」错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
