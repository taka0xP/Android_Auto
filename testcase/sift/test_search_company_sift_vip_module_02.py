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
import re
from Providers.logger import Logger, error_format
from Providers.account.account import Account

log = Logger("查公司_高级筛选_02").getlog()


class Search_company_sift_vip(MyTest, Operation):
    """查公司_高级筛选_02"""

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

    def get_company_sjhm(self, selectText, selectTarget, index=None):
        """
        获取公司：手机号码并断言
        :param selectText: 更多筛选-筛选项
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """

        phone_list = []
        tempNum = 0
        result = None
        company_name = self.sift_opera.click2company(selectText, selectTarget)
        if not self.isElementExist(By.ID, self.ELEMENT['tv_base_info_phone']):
            # 无手机号码/无联系电话，不展示基本信息「电话按钮」
            # tag = str(index) is "2"
            # self.assertTrue(tag, "===「无手机/联系号码」断言失败-公司基本信息「有」手机/联系号码===")
            result = index == 2
        else:
            phone_tag = self.driver.find_element_by_id(self.ELEMENT["tv_base_info_phone"]).get_attribute("enabled")
            if "true" == phone_tag:
                self.driver.find_element_by_id(self.ELEMENT["tv_base_info_phone"]).click()
                phones = self.new_find_elements(By.XPATH, self.ELEMENT["ll_msg"])
                for i in range(len(phones)):
                    phone_xpath = "{}[{}]{}".format(self.ELEMENT["ll_msg"], str(i + 1),
                                                    '//*[@resource-id="com.tianyancha.skyeye:id/tv_phn"]')
                    phone_list.append(self.new_find_element(By.XPATH, phone_xpath).text)
                log.info(phone_list)
                for i in range(len(phone_list)):
                    if not re.match(r"^1[35678]\d{9}$", phone_list[i]):
                        tempNum += 1
                if index == 1:
                    phone_tag = len(phone_list) != tempNum
                    # self.assertTrue(phone_tag, "===「有手机号码」断言失败-号码列表中「无」手机号码===")
                    result = phone_tag
                else:
                    if self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_score_tip"):
                        tag = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_score_tip").text
                        if "认证" in tag:
                            phone_tag = len(phone_list) == tempNum
                            # self.assertTrue(phone_tag, "===「无手机号码」断言失败-号码列表中「有」手机号码===")
                            result = phone_tag
                        elif "年审" in tag:
                            if len(phone_list) == tempNum:
                                # log.info("===该企业处在「认证待年审状态」，【无】手机/联系电话===")
                                result = "===该企业：「{}」处在「认证待年审状态」，【无】手机/联系电话===".format(company_name)
                            else:
                                # log.info("===该企业处在「认证待年审状态」，【有】手机/联系电话===")
                                result = "===该企业：「{}」处在「认证待年审状态」，【有】手机/联系电话===".format(company_name)
                        else:
                            result = "非「认证」「年审」企业：{}".format(company_name)
                    else:
                        if len(phone_list) == tempNum:
                            # log.info("===该企业处在「已认证状态」，【无】手机/联系电话===")
                            result = "===该企业：「{}」处在「已认证状态」，【无】手机/联系电话===".format(company_name)
                        else:
                            # log.info("===该企业处在「已认证状态」，【有】手机/联系电话===")
                            result = "===该企业：「{}」处在「已认证状态」，【有】手机/联系电话===".format(company_name)
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/iv_close").click()
            else:
                if index == 1:
                    # self.assertTrue(False, "===「有手机号码」断言失败-公司基本信息「无」手机号码===")
                    result = False
                else:
                    result = True
        self.sift_opera.back2company_search()
        self.sift_opera.reset(selectTarget)
        return result

    @getimage
    def test_001_cgs_gjsx_sjhm_p0(self):
        """查公司-搜索中间页，高级筛选:手机号码"""
        log.info(self.test_001_cgs_gjsx_sjhm_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_sjhm = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_sjhm_title", "more_sjhm", num_sjhm)
            result = self.get_company_sjhm(selectText, selectTarget, num_sjhm)
            log.info("===result===")
            if isinstance(result, type("返回值类型为str")):
                log.info(result)
            else:
                self.assertTrue(result, "===「有手机号码」断言失败-公司基本信息「无」手机号码===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgs_gjsx_zlxx_p0(self):
        """查公司-搜索中间页，高级筛选:专利信息"""
        log.info(self.test_002_cgs_gjsx_zlxx_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_zlxx = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_zlxx_title", "more_zlxx", num_zlxx)
            result = self.sift_opera.detail4company(selectText, "专利信息", selectTarget, num_zlxx)
            if num_zlxx == 1:
                # 断言-有专利信息
                self.assertTrue(result, "===失败-高级筛选：「{}」错误===".format(selectText))
            else:
                # 断言-无专利信息
                self.assertFalse(result, "===失败-高级筛选：「{}」错误===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
