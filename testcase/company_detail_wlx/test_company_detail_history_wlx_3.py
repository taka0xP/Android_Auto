# -*- coding: utf-8 -*-
# @Time    : 2020-03-17 18:44
# @Author  : wlx
# @File    : company_detail_history_info.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep
from Providers.logger import Logger, error_format

log = Logger("历史信息_03").getlog()


class Company_detail_Test_wlx_3(MyTest, Operation):
    """非VIP用户进入公司详情页历史信息VIP拦截校验"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 获取excel
        cls.ELEMENT = Read_Ex().read_excel("company_detail_wlx")
        cls.user = cls.account.get_account()
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.account.release_account(account=cls.user, account_type="account", account_special="0")


    def go_company_detail(self, company_name, index=0):
        self.search_company(company_name)
        self.new_find_elements(
            By.XPATH, self.ELEMENT["company_name_search_result_list"]
        )[index].click()

    @getimage
    def test_history_info_001(self):
        log.info(self.test_history_info_001.__doc__)
        try:
            self.login(self.user, self.account.get_pwd())
            self.go_company_detail("宁夏天元锰业")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_gsxx"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-工商信息无VIP拦截",
            )
            self.driver.keyevent(4)

            self.new_find_element(By.XPATH, self.ELEMENT["his_lsgd"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-历史股东无VIP拦截",
            )
            self.driver.keyevent(4)

            self.new_find_element(By.XPATH, self.ELEMENT["his_dytz"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-对外投资无VIP拦截",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(
                By.XPATH, self.ELEMENT["his_ktgg"], click=True, check_cover=True
            )
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-开庭公告无VIP拦截",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_flss"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-法律诉讼无VIP拦截",
            )
            self.driver.keyevent(4)

            # self.new_find_element(By.XPATH, self.ELEMENT["his_fygg"]).click()
            # self.assertTrue(
            #     self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
            #     "非VIP进入历史信息-法院公告无VIP拦截",
            # )
            # self.driver.keyevent(4)

            self.swipe_up_while_ele_located(
                By.XPATH, self.ELEMENT["his_bzxr"], click=True, check_cover=True
            )
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-被执行人无VIP拦截",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_gqcz"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-股权出质无VIP拦截",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_dcdy"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-动产抵押无VIP拦截",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_wzba"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-网站备案无VIP拦截",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
    @getimage
    def test_history_info_002(self):
        log.info(self.test_history_info_002.__doc__)
        try:
            self.go_company_detail("上海毛巾十五厂")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_dcdy"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sbxx"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-商标信息无VIP拦截",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
