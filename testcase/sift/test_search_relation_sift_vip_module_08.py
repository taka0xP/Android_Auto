# -*- coding: utf-8 -*-
# @Time    : 2020-02-20 12:23
# @Author  : XU
# @File    : test_search_relation_sift_vip_module_01.py
# @Software: PyCharm

from common.operation import Operation, getimage
import unittest
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from Providers.sift.sift_opera import SiftOperation
from common.ReadData import Read_Ex
import random
from Providers.logger import Logger, error_format
from Providers.account.account import Account

log = Logger("查关系_高级筛选_08").getlog()


class Search_relation_sift_vip(MyTest, Operation):
    """查关系_高级筛选_08"""

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
        cls.account.release_account(cls.phone_vip, "vip")
        super().tearDownClass()

    def get_company_lxfs(self, selectTarget, inputTarget):
        """
        获取公司：联系方式并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        """
        selectText = self.sift_opera.point2company(selectTarget)
        firm_name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("高级筛选:{}，断言公司名称：{}".format(selectText, firm_name))
        result = self.driver.find_element_by_id(self.ELEMENT["tv_base_info_phone"]).get_attribute("enabled")
        self.sift_opera.back2relation_search(inputTarget)
        return result

    @getimage
    def test_001_cgx_gjsx_lxfs_p0(self):
        """查关系-搜索中间页，高级筛选:联系方式"""
        log.info(self.test_001_cgx_gjsx_lxfs_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_lxfs = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_lxfs_title", "more_lxfs", num_lxfs)
            result = self.get_company_lxfs(selectTarget, inputTarget)
            if num_lxfs == 1:
                self.assertEqual("true", result, "===失败-联系方式（VIP特权）筛选：有联系方式===")
            else:
                self.assertEqual("false", result, "===失败-联系方式（VIP特权）筛选：无联系方式===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_gjsx_zpzzq_p0(self):
        """查关系-搜索中间页，高级筛选:作品著作权"""
        log.info(self.test_002_cgx_gjsx_zpzzq_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_zpzzq = random.randint(1, 2)
            num_zpzzq = 2
            selectTarget, selectText = self.sift_opera.get_key("more_zpzzq_title", "more_zpzzq", num_zpzzq)
            result = self.sift_opera.detail4relation("著作权", selectTarget, inputTarget, num_zpzzq)
            if num_zpzzq == 2 and not result:
                # 断言-详情页「著作权」维度无数据时
                self.assertFalse(result, "===失败-高级筛选：「无作品著作权」错误===")
            else:
                if num_zpzzq == 1:
                    # 断言-「有作品著作权」
                    # self.assertNotIn("0", result, "===失败-高级筛选：「有作品著作权」错误===")
                    log.info("作品著作权：{}个".format(result))
                    self.assertNotEqual(0, result, "===失败-高级筛选：「有作品著作权」错误===")
                else:
                    # 断言-「无作品著作权」
                    # self.assertIn("0", result, "===失败-高级筛选：「无作品著作权」错误===")
                    self.assertEqual(0, result, "===失败-高级筛选：「无作品著作权」错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
