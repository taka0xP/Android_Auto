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
import os
import json
from Providers.account.account import Account

log = Logger("查公司_高级筛选_05").getlog()


class Search_company_sift_vip(MyTest, Operation):
    """查公司_高级筛选_05"""

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

    def get_company_sszt(self, selectTarget, index=None):
        """
        获取公司：上市状态并断言
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """

        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        self.sift_opera.click2company(selectText, selectTarget)
        if index == 1:
            for i in range(10):
                stock_tag = self.isElementExist(By.ID, self.ELEMENT["stock_title_tv"])
                if stock_tag:
                    stock_info = self.new_find_element(By.ID, self.ELEMENT["stock_title_tv"]).text
                    log.info("股票信息：{}".format(stock_info))
                    return stock_tag
                else:
                    self.swipeUp(x1=0.5, y1=0.7, y2=0.3, t=2000)
                    if i == 9:
                        log.error("===上市公司-股票信息获取失败===")
                        return stock_tag
        else:
            for i in range(10):
                company_bak = self.isElementExist(By.XPATH, self.ELEMENT["company_background"])
                if company_bak:
                    atlas = self.new_find_element(By.ID, self.ELEMENT["background_to_atlas"]).text
                    return atlas
                else:
                    self.swipeUp(x1=0.5, y1=0.7, y2=0.3, t=2000)
                    if i == 9:
                        log.error("===非上市公司「企业背景」上方「天眼风险」模块获取失败===")
                        return company_bak
        self.sift_opera.back2company_search()
        self.sift_opera.reset(selectTarget)

    def get_company_500(self, selectTarget):
        """
        获取公司：500强企业断言
        :param selectTarget: 选中条件
        """

        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        company_name = self.sift_opera.click2company(selectText, selectTarget)
        current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        json_dir = os.path.dirname(current_dir) + "/Data/500.json"
        with open(json_dir, "r") as json_file:
            data = json.load(json_file)
        self.sift_opera.back2company_search()
        self.sift_opera.reset(selectTarget)
        return company_name, data, selectText

    @getimage
    def test_001_cgs_gjsx_sszt_p0(self):
        """查公司-搜索中间页，高级筛选:上市状态"""
        log.info(self.test_001_cgs_gjsx_sszt_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_sszt = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_sszt_title", "more_sszt", num_sszt)
            result = self.get_company_sszt(selectTarget, num_sszt)

            if num_sszt == 1:
                self.assertTrue(result, "===失败-上市公司-股票信息获取失败===",)
            else:
                self.assertEqual("天眼图谱", str(result), "===失败-非上市公司-获取失败===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgs_gjsx_500_p0(self):
        """查公司-搜索中间页，高级筛选:500强"""
        log.info(self.test_002_cgs_gjsx_500_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_500 = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_500_title", "more_500", num_500)
            company_name, data, selectText = self.get_company_500(selectTarget)
            # 断言-世界/中国500强
            self.assertIn(company_name, data[str(num_500)], "===失败-「{}」，断言失败===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
