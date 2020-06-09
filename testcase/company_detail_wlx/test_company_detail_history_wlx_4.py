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

log = Logger("历史信息_04").getlog()


class Company_detail_Test_wlx_4(MyTest, Operation):
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
            self.go_company_detail("湖南盛华夏矿业投资有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sxxx"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-失信信息无VIP拦截",
            )

            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_xzxfl"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-限制消费令无VIP拦截",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sfxz"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-司法协助无VIP拦截",
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
            self.go_company_detail("乐视网信息技术（北京）股份有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_zbaj"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-终本案件无VIP拦截",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(
                By.XPATH, self.ELEMENT["his_jyyc"], click=True, check_cover=True
            )
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-经营异常无VIP拦截",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_xzcf"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-行政处罚无VIP拦截",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_history_info_003(self):
        log.info(self.test_history_info_003.__doc__)
        try:
            self.go_company_detail("一汽海马汽车有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(
                By.XPATH, self.ELEMENT["his_xzxk"], click=True, check_cover=True
            )
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["his_vip_text"]),
                "非VIP进入历史信息-行政许可无VIP拦截",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e