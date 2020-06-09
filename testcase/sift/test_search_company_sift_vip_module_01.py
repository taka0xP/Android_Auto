# -*- coding: utf-8 -*-
# @Time    : 2020-02-20 20:36
# @Author  : XU
# @File    : test_search_company_sift_vip_module_01.py
# @Software: PyCharm

from common.operation import Operation, getimage
import unittest
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from Providers.sift.sift_opera import SiftOperation
from common.ReadData import Read_Ex
import random
from Providers.logger import Logger, error_format
from selenium.webdriver.support.wait import WebDriverWait
from Providers.account.account import Account

log = Logger("查公司_高级筛选_01").getlog()


class Search_company_sift_vip(MyTest, Operation):
    """查公司_高级筛选_01"""

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

    def get_company_lxfs(self, selectTarget, index=None):
        """
        获取公司：联系方式并断言
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        self.sift_opera.click2company(selectText, selectTarget)
        WebDriverWait(self.driver, 5).until(
            lambda driver: driver.find_element_by_id(self.ELEMENT["tv_base_info_phone"])
        )
        result = self.driver.find_element_by_id(self.ELEMENT["tv_base_info_phone"]).get_attribute("enabled")
        if "true" == result and index != 1:
            if self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_score_tip"):
                result = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_score_tip").text
            else:
                result = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/iv_claim_label")
        self.sift_opera.back2company_search()
        self.sift_opera.reset(selectTarget)
        return result

    @getimage
    def test_001_cgs_gjsx_lxfs_p0(self):
        """查公司-搜索中间页，高级筛选:联系方式"""
        log.info(self.test_001_cgs_gjsx_lxfs_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_lxfs = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_lxfs_title", "more_lxfs", num_lxfs)
            result = self.get_company_lxfs(selectTarget, 1)
            if num_lxfs == 1:
                self.assertEqual("true", result, "===失败-联系方式（VIP特权）筛选：有联系方式===")
            else:
                if "true" == result and num_lxfs != 1:
                    if self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_score_tip"):
                        self.assertIn("年审", result, "===年审企业，包含「手机/联系」电话===")
                    else:
                        self.assertFalse(result, "===已认证企业，包含「手机/联系」电话===")
                else:
                    self.assertEqual("false", result, "===失败-联系方式（VIP特权）筛选：无联系方式===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgs_gjsx_zpzzq_p0(self):
        """查公司-搜索中间页，高级筛选:作品著作权"""
        log.info(self.test_002_cgs_gjsx_zpzzq_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_zpzzq = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_zpzzq_title", "more_zpzzq", num_zpzzq)
            result = self.sift_opera.detail4company(selectText, "著作权", selectTarget, num_zpzzq)
            if num_zpzzq == 2 and not result:
                # 断言-详情页「著作权」维度无数据时
                self.assertFalse(result, "===失败-高级筛选：「{}」错误===".format(selectText))
            else:
                if num_zpzzq == 1:
                    # 断言-「有作品著作权」
                    self.assertNotIn("0", result, "===失败-高级筛选：「{}」错误===".format(selectText))
                else:
                    # 断言-详情页「有软件著作权」，「无作品著作权」
                    self.assertIn("0", result, "===失败-高级筛选：「{}」错误===".format(selectText))

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
