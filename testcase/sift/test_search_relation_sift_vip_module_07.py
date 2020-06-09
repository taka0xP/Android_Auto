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
import re
from Providers.logger import Logger, error_format
from Providers.account.account import Account

log = Logger("查关系_高级筛选_07").getlog()


class Search_relation_sift_vip(MyTest, Operation):
    """查关系_高级筛选_07"""

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

    def get_company_sjhm(self, selectTarget, inputTarget, index=None):
        """
        获取公司：手机号码并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        result = None
        phone_list = []
        tempNum = 0
        tv_phn = '//*[@resource-id="com.tianyancha.skyeye:id/tv_phn"]'
        selectText = self.sift_opera.point2company(selectTarget)
        company = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("高级筛选：{}，断言公司名称：{}".format(selectText, company))
        if not self.isElementExist(By.ID, self.ELEMENT['tv_base_info_phone']):
            # 无手机号码/无联系电话，不展示基本信息「电话按钮」
            result = "2" is str(index)
        else:
            phone_attr = self.driver.find_element_by_id(self.ELEMENT["tv_base_info_phone"]).get_attribute("enabled")
            if "true" == phone_attr:
                self.driver.find_element_by_id(self.ELEMENT["tv_base_info_phone"]).click()
                phones = self.new_find_elements(By.XPATH, self.ELEMENT["ll_msg"])
                for i in range(len(phones)):
                    phn_xpath = "{}[{}]{}".format(self.ELEMENT["ll_msg"], str(i + 1), tv_phn)
                    phn_text = self.new_find_element(By.XPATH, phn_xpath).text
                    phone_list.append(phn_text)
                log.info(phone_list)
                for i in range(len(phone_list)):
                    if not re.match(r"^1[35678]\d{9}$", phone_list[i]):
                        tempNum += 1
                if index == 1:
                    result = len(phone_list) == tempNum
                else:
                    if self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_score_tip"):
                        tag = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_score_tip").text
                        if "认证" in tag:
                            result = len(phone_list) == tempNum
                        elif "年审" in tag:
                            if len(phone_list) == tempNum:
                                result = "===该企业处在「认证待年审状态」，【无】手机/联系电话==="
                            else:
                                result = "===该企业处在「认证待年审状态」，【有】手机/联系电话==="
                    else:
                        if len(phone_list) == tempNum:
                            result = "===该企业处在「已认证状态」，【无】手机/联系电话==="
                        else:
                            result = "===该企业处在「已认证状态」，【有】手机/联系电话==="
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/iv_close").click()
            else:
                if index == 1:
                    result = False
                else:
                    result = True
        self.sift_opera.back2relation_search(inputTarget)
        return result

    @getimage
    def test_001_cgx_gjsx_sjhm_p0(self):
        """查关系-搜索中间页，高级筛选:手机号码"""
        log.info(self.test_001_cgx_gjsx_sjhm_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_sjhm = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_sjhm_title", "more_sjhm", num_sjhm)
            result = self.get_company_sjhm(selectTarget, inputTarget, num_sjhm)
            if isinstance(result, type("返回值类型为str")):
                log.info(result)
            else:
                self.assertTrue(result)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_gjsx_zlxx_p0(self):
        """查关系-搜索中间页，高级筛选:专利信息"""
        log.info(self.test_002_cgx_gjsx_zlxx_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_zlxx = random.randint(1, 2)
            selectTarget, selectText = self.sift_opera.get_key("more_zlxx_title", "more_zlxx", num_zlxx)
            result = self.sift_opera.detail4relation("专利信息", selectTarget, inputTarget, num_zlxx)
            if num_zlxx == 1:
                self.assertTrue(result, "===失败-高级筛选：「有专利信息」错误===")
            else:
                self.assertFalse(result, "===失败-高级筛选：「无专利信息」错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
