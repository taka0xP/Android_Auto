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

log = Logger("历史信息_02").getlog()


class Company_detail_Test_wlx_2(MyTest, Operation):
    """未登录用户进入公司详情页历史信息校验"""

    a = Read_Ex()
    ELEMENT = a.read_excel("company_detail_wlx")

    def go_company_detail(self, company_name, index=0):
        self.search_company(company_name)
        self.new_find_elements(
            By.XPATH, self.ELEMENT["company_name_search_result_list"]
        )[index].click()

    @getimage
    def test_history_info_001(self):
        log.info(self.test_history_info_001.__doc__)
        try:
            self.go_company_detail("上海毛巾十五厂")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_dcdy"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sbxx"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["login_new"]), "进入历史信息-商标信息未调起登录"
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
            self.go_company_detail("乐视控股（北京）有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sxxx"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["login_new"]), "进入历史信息-失信信息未调起登录"
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_zbaj"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["login_new"]), "进入历史信息-终本案件未调起登录"
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(
                By.XPATH, self.ELEMENT["his_jyyc"], click=True, check_cover=True
            )
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["login_new"]), "进入历史信息-经营异常未调起登录"
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
            self.go_company_detail("北京小桔科技有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(
                By.XPATH, self.ELEMENT["his_xzxk"], click=True, check_cover=True
            )
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["login_new"]), "进入历史信息-行政许可未调起登录"
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_history_info_004(self):
        log.info(self.test_history_info_004.__doc__)
        try:
            self.go_company_detail("湖南盛华夏矿业投资有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_xzxfl"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["login_new"]),
                "进入历史信息-限制消费令未调起登录",
            )
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sfxz"], click=True)
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["login_new"]), "进入历史信息-司法协助未调起登录"
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
