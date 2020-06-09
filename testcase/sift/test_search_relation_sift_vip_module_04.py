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
import os
import json
from Providers.account.account import Account

log = Logger("查关系_高级筛选_04").getlog()


class Search_relation_sift_vip(MyTest, Operation):
    """查关系_高级筛选_04"""

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

    def get_company_sszt(self, selectTarget, inputTarget, index=None):
        """
        获取公司：上市状态并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        result = None
        selectText = self.sift_opera.point2company(selectTarget)
        firm_name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("高级筛选：{}，断言公司名称：{}".format(selectText, firm_name))
        if index == 1:
            for i in range(10):
                if self.isElementExist(By.ID, self.ELEMENT["stock_title_tv"]):
                    stock_info = self.new_find_element(By.ID, self.ELEMENT["stock_title_tv"]).text
                    log.info("股票信息：{}".format(stock_info))
                    stock_title = self.isElementExist(By.ID, self.ELEMENT["stock_title_tv"])
                    result = stock_title
                    break
                else:
                    self.swipeUp(x1=0.5, y1=0.7, y2=0.3, t=2000)
                    if i == 29:
                        stock_title = self.isElementExist(By.ID, self.ELEMENT["stock_title_tv"])
                        result = stock_title
        else:
            for i in range(10):
                if self.isElementExist(By.XPATH, self.ELEMENT["company_background"]):
                    atlas = self.new_find_element(By.XPATH, self.ELEMENT["background_to_atlas"]).text
                    result = "天眼图谱" is atlas
                    break
                else:
                    self.swipeUp(x1=0.5, y1=0.7, y2=0.3, t=2000)
                    if i == 29:
                        company_backgrand = self.isElementExist(By.ID, self.ELEMENT["company_background"])
                        result = company_backgrand
        self.sift_opera.back2relation_search(inputTarget)
        return result

    def get_company_500(self, selectTarget, inputTarget, index=None):
        """
        获取公司：500强企业断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        selectText = self.sift_opera.point2company(selectTarget)
        company_name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("高级筛选：{}，断言公司名称：{}".format(selectText, company_name))
        current_dir = os.path.abspath(os.path.dirname(__file__))
        json_dir = os.path.dirname(current_dir) + "/../Data/500.json"
        with open(json_dir, "r") as json_file:
            data = json.load(json_file)
        self.sift_opera.back2relation_search(inputTarget)
        return company_name, data[str(index)]

    @getimage
    def test_001_cgx_gjsx_sszt_p0(self):
        """查关系-搜索中间页，高级筛选:上市状态"""
        log.info(self.test_001_cgx_gjsx_sszt_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_sszt = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_sszt_title", "more_sszt", num_sszt)
            result = self.get_company_sszt(selectTarget, inputTarget, num_sszt)
            self.assertTrue(result)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_gjsx_500_p0(self):
        """查关系-搜索中间页，高级筛选:500强"""
        log.info(self.test_002_cgx_gjsx_500_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_500 = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_500_title", "more_500", num_500)
            company, data = self.get_company_500(selectTarget, inputTarget, num_500)
            self.assertIn(company, data, "===失败-「{}」，断言失败===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
