# -*- coding: utf-8 -*-
# @Time    : 2020-02-19 17:45
# @Author  : XU
# @File    : test_search_relation_sift_module_01.py
# @Software: PyCharm
import re
import random
import unittest
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from selenium.webdriver.common.by import By
from Providers.account.account import Account
from common.operation import Operation, getimage
from Providers.logger import Logger, error_format
from Providers.sift.sift_opera import SiftOperation

log = Logger("查关系_更多筛选_02").getlog()


class Search_relation_sift(MyTest, Operation):
    """查关系_更多筛选_02"""

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

    def get_company_zblx(self, selectTarget, inputTarget, index=None):
        """
        获取公司：资本类型并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        money = ["美", "新台币", "港", "澳", "日", "铢", "盾", "卢", "尼", " 镑", "尔"]
        selectText = self.sift_opera.point2company(selectTarget)
        name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("更多筛选-资本类型-{}，断言公司名称：{}".format(selectText, name))
        zblx_text = self.new_find_element(By.ID, self.ELEMENT["more_zblx_title_unit"]).text
        if index == 1:
            if "人民" not in zblx_text:
                # 若资本类型无币种，则默认归入人民币中，断言无其他币种即通过
                tag = True
                for i in money:
                    if i in zblx_text:
                        tag = False
                        break
                result = tag
            else:
                result = "人民" in zblx_text
        elif index == 2:
            result = "美" in zblx_text
        else:
            tag1 = "人民" not in zblx_text
            tag2 = "美" not in zblx_text
            result = tag1 and tag2
        self.sift_opera.back2relation_search(inputTarget)
        return result

    def get_company_qylx(self, selectTarget, inputTarget, index=None):
        """
        获取公司：企业类型并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        selectText = self.sift_opera.point2company(selectTarget)
        name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("更多筛选-企业类型-{}，断言公司名称：{}".format(selectText, name))
        result = self.sift_opera.company_type(selectText, index)
        self.sift_opera.back2relation_search(inputTarget)
        return result

    def get_company_cbrs(self, selectTarget, inputTarget, index=None):
        """
        获取公司：参保人数并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        result = None
        selectText = self.sift_opera.point2company(selectTarget)
        company_name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("更多筛选-参保人数-{}，断言公司名称：".format(selectText, company_name))
        for i in range(20):
            if self.isElementExist(By.XPATH, self.ELEMENT["more_gsxx_dimension"]):
                self.new_find_element(By.XPATH, self.ELEMENT["more_gsxx_dimension"]).click()
                # 工商信息维度，查找参保人数字段
                for j in range(20):
                    if self.isElementExist(By.ID, self.ELEMENT["tv_social_staff_num"]):
                        cbrsStr = self.new_find_element(By.ID, self.ELEMENT["tv_social_staff_num"]).text
                        cbrsNum = re.findall(r"\d+\.?\d*", cbrsStr)
                        log.info(company_name + "-参保人数：" + cbrsNum[0])
                        _dict = {
                            1: 0 <= int(cbrsNum[0]),
                            2: 50 <= int(cbrsNum[0]) <= 99,
                            3: 100 <= int(cbrsNum[0]) <= 499,
                            4: 500 <= int(cbrsNum[0]) <= 999,
                            5: 1000 <= int(cbrsNum[0]) <= 4999,
                            6: 5000 <= int(cbrsNum[0]) <= 9999,
                            7: 10000 <= int(cbrsNum[0]),
                        }
                        for k in _dict.keys():
                            if k == index:
                                result = _dict[index]
                        break
                    else:
                        self.swipeUp(0.5, 0.7, 0.3, 2000)
                        if i == 19:
                            result = "参保人数断言失败-工商信息详情页，参保人数未找到"
                break
            else:
                self.swipeUp(0.5, 0.7, 0.3, 2000)
                if i == 19:
                    result = "参保人数断言失败-公司详情页未找到「工商信息」"
        self.sift_opera.back2relation_search(inputTarget)
        return result

    @getimage
    def test_001_cgx_ptsx_zblx_p0(self):
        """查关系-搜索中间页，普通筛选：资本类型"""
        log.info(self.test_001_cgx_ptsx_zblx_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_zblx = random.randint(1, 3)
            selectTarget, selectText = self.sift_opera.get_key("more_zblx_title", "more_zblx", num_zblx)
            result = self.get_company_zblx(selectTarget, inputTarget, num_zblx)
            self.assertTrue(result, "===失败-更多筛选：资本类型：{}===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_ptsx_qylx_p0(self):
        """查关系-搜索中间页，普通筛选：企业类型"""
        log.info(self.test_002_cgx_ptsx_qylx_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_qylx = random.randint(1, 11)
            selectTarget, selectText = self.sift_opera.get_key("more_qylx_title", "more_qylx", num_qylx)
            result = self.get_company_qylx(selectTarget, inputTarget, num_qylx)
            if isinstance(result, type("返回值类型为str")):
                log.info(result)
            else:
                self.assertTrue(result, "===失败-工商信息详情页中，企业类型断言错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_cgx_ptsx_cbrs_p0(self):
        """查关系-搜索中间页，普通筛选：参保人数"""
        log.info(self.test_003_cgx_ptsx_cbrs_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_cbrs = random.randint(1, 7)
            selectTarget, selectText = self.sift_opera.get_key("more_cbrs_title", "more_cbrs", num_cbrs)
            result = self.get_company_cbrs(selectTarget, inputTarget, num_cbrs)
            if result is None:
                log.info(result)
            else:
                self.assertTrue(result, "===失败-工商信息详情页中，参保人数断言错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
