# -*- coding: utf-8 -*-
# @Time    : 2020-03-17 16:39
# @Author  : XU
# @File    : test_company_detail_basic_module_02.py
# @Software: PyCharm

from common.operation import Operation
from Providers.sift.sift_opera import SiftOperation
import unittest
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger, error_format
from Providers.account.account import Account

log = Logger("公司详情页-股东/高管").getlog()


class Company_detail_baseinfo(MyTest, Operation):
    """公司详情页_股东/高管"""

    a = Read_Ex()
    ELEMENT = a.read_excel("company_detail_xu")
    account = Account()
    phone_vip = account.get_account("vip")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sift_opera = SiftOperation(cls.driver, cls.ELEMENT)

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.phone_vip, 'vip')
        super().tearDownClass()

    def detail_opera(self, *opera, num=1, tag=1):
        self.new_find_element(*opera).click()
        if tag == 1:
            result = self.isElementExist(By.ID, self.ELEMENT["btv_title"])
        else:
            result = self.new_find_element(By.ID, self.ELEMENT["app_title_name"]).text
        if num == 0:
            result = self.isElementExist(By.ID, self.ELEMENT["radio_person_detail"])
        elif num == 2:
            result = self.isElementExist(By.ID, self.ELEMENT["radio_firm_detail"])
        self.driver.keyevent(4)
        if num == 0:
            self.new_find_element(By.ID, self.ELEMENT["iv_score"]).click()
        return result

    def test_001_gsxx_jcxx_p0(self):
        """公司基本信息，未登录态校验"""
        log.info(self.test_001_gsxx_jcxx_p0.__doc__)
        try:
            self.sift_opera.into_company(company="万科企业股份有限公司")
            self.new_find_element(By.ID, self.ELEMENT["tv_des"]).click()
            self.new_find_element(By.ID, self.ELEMENT["tv_des"]).click()

            result = self.detail_opera(By.ID, self.ELEMENT["tv_des_sub_value_1"])
            self.assertTrue(result, "===法定代表人，未登录限制失败===")

            result = self.detail_opera(By.XPATH, self.ELEMENT["rv_riskinfo_item1"])
            self.assertTrue(result, "===天眼风险-自身风险，未登录限制失败===")

            result = self.detail_opera(By.XPATH, self.ELEMENT["rv_riskinfo_item2"])
            self.assertTrue(result, "===天眼风险-周边风险，未登录限制失败===")

            result = self.detail_opera(By.XPATH, self.ELEMENT["rv_riskinfo_item3"])
            self.assertTrue(result, "===天眼风险-预警信息，未登录限制失败===")

            result = self.detail_opera(By.ID, self.ELEMENT["tv_base_info_phone"])
            self.assertTrue(result, "===电话，未登录限制失败===")

            result = self.detail_opera(By.ID, self.ELEMENT["tv_base_info_address"], tag=0)
            self.assertEqual("公司地图", result, "===点击「地址」，跳转地图页失败===")

            self.driver.keyevent(4)
            self.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).send_keys("上海彩亿信息技术有限公司")
            self.new_find_element(By.XPATH, '//*[@class="android.widget.TextView" and @text="上海彩亿信息技术有限公司"]').click()

            result = self.detail_opera(By.XPATH, self.ELEMENT["tv_shareholder_1"])
            self.assertTrue(result, "===自然人股东，未登录限制失败===")

            result = self.detail_opera(By.XPATH, self.ELEMENT["tv_staff_1"])
            self.assertTrue(result, "===自然人股东，未登录限制失败===")

            result = self.detail_opera(By.ID, self.ELEMENT["tv_shareholder_count"], tag=0)
            self.assertEqual("股东信息", result, "===失败-非上市公司，点击「股东」未进入「股东信息页」===")

            result = self.detail_opera(By.ID, self.ELEMENT["tv_staff_count"], tag=0)
            self.assertEqual("主要人员", result, "===失败-非上市公司，点击「高管」未进入「主要人员页」===")

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))

    def test_002_gsxx_jcxx_p0(self):
        """公司详情页，登陆vip账号"""
        log.info(self.test_002_gsxx_jcxx_p0.__doc__)
        try:
            self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
            self.sift_opera.into_company(company="万科企业股份有限公司")

            result = self.detail_opera(By.ID, self.ELEMENT["tv_des_sub_value_1"], num=0)
            self.assertTrue(result, "===登陆态，跳转「法定代表人」详情页失败===")

            result = self.detail_opera(By.ID, self.ELEMENT["tv_claim"], tag=0)
            self.assertEqual("选择认证套餐", result, "===评分弹出，认证入口，跳转失败===")

            self.new_find_element(By.ID, self.ELEMENT["tv_base_info_phone"]).click()
            delte_cancel = self.new_find_element(By.ID, self.ELEMENT["delte_cancel"]).text
            self.assertEqual("修改电话", delte_cancel, "===电话弹窗，弹出失败===")

            result = self.detail_opera(By.ID, self.ELEMENT["delte_cancel"], tag=0)
            self.assertEqual("选择认证套餐", result, "===电话弹窗，修改电话，跳转失败===")

            result = self.detail_opera(By.ID, self.ELEMENT["iv_claim_label"], tag=0)
            self.assertEqual("选择认证套餐", result, "===登录态点击「我要认证」标签，跳转失败===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))

    def test_003_gsxx_gd_p0(self):
        """公司详情页，股东/高管"""
        log.info(self.test_003_gsxx_gd_p0.__doc__)
        try:
            self.sift_opera.into_company(company="万科企业股份有限公司")
            # 股东
            holder = self.isElementExist(By.ID, self.ELEMENT["holder_type_iv"])
            self.assertTrue(holder, "===大股东标签缺失===")

            result = self.detail_opera(By.ID, self.ELEMENT["tv_shareholder_count"], tag=0)
            self.assertEqual("十大股东", result, "===失败-上市公司，点击「股东」未进入「十大股东页」===")

            result = self.detail_opera(By.XPATH, self.ELEMENT["tv_shareholder_1"], num=2)
            self.assertTrue(result, "===非自然人股东，跳转详情页错误===")

            # 高管
            result = self.detail_opera(By.ID, self.ELEMENT["tv_staff_count"], tag=0)
            self.assertEqual("高管信息", result, "===失败-上市公司，点击「高管」未进入「高管信息页」===")

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))


if __name__ == "__main__":
    unittest.main()
