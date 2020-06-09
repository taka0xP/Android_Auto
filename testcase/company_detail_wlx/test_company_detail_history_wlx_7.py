# -*- coding: utf-8 -*-
# @Time    : 2020-03-23 10:00
# @Author  : wlx
# @File    : company_detail_history_info.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep
from Providers.logger import Logger, error_format
from common.check_rules import *

log = Logger("历史信息_07").getlog()


class Company_detail_Test_wlx_7(MyTest, Operation):
    """VIP用户进入公司详情页历史信息校验"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 获取excel
        cls.ELEMENT = Read_Ex().read_excel("company_detail_wlx")
        cls.vip_user = cls.account.get_account("vip", "0")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.account.release_account(account=cls.vip_user, account_type="vip", account_special="0")

    def go_company_detail(self, company_name, index=0):
        self.search_company(company_name)
        self.new_find_elements(
            By.XPATH, self.ELEMENT["company_name_search_result_list"]
        )[index].click()

    @getimage
    def test_001(self):
        """历史失信被执行人维度"""
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.go_company_detail("滴滴")
            cname = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            bzxr = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_bzxr"], check_cover=True)
            bzxr_count = self.new_find_element(By.XPATH, self.ELEMENT["his_bzxr_count"]).text
            bzxr.click()

            list_case_num = self.new_find_elements(By.ID, self.ELEMENT['his_bzxr_list_case_num'])[0].text
            list_court = self.new_find_elements(By.ID, self.ELEMENT['his_bzxr_list_court'])[0].text
            list_exec_money = self.new_find_elements(By.ID, self.ELEMENT['his_bzxr_list_exec_money'])[0].text
            list_regdate = self.new_find_elements(By.ID, self.ELEMENT['his_bzxr_list_regdate'])[0].text
            self.new_find_elements(By.ID, self.ELEMENT['his_bzxr_list_item'])[0].click()

            detail_company = self.new_find_element(By.ID, self.ELEMENT['his_bzxr_detail_company'])
            bzxr_detail_company = detail_company.text
            self.assertEqual(cname, bzxr_detail_company, '历史失信被执行人详情页名称与当前公司名不符')
            # detail_company.click()
            # jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            # self.assertEqual(jump_name, bzxr_detail_company, '历史失信被执行人详情页跳转公司详情页公司名称不对应')
            # self.driver.keyevent(4)

            detail_court = self.new_find_element(By.ID, self.ELEMENT['his_bzxr_detail_court']).text
            self.assertEqual(detail_court, list_court, '历史失信被执行人详情页执行法院字段与列表页不匹配')

            detail_case_num = self.new_find_element(By.ID, self.ELEMENT['his_bzxr_detail_case_num']).text
            self.assertEqual(detail_case_num, list_case_num, '历史失信被执行人详情页案号字段与列表页不匹配')

            detail_regdate = self.new_find_element(By.ID, self.ELEMENT['his_bzxr_detail_regdate']).text
            self.assertEqual(detail_regdate, list_regdate, '历史失信被执行人详情页立案日期字段与列表页不匹配')
            self.assertTrue(check_time(detail_regdate, is_compare=True), '历史失信被执行人详情页立案日期字段校验错误')

            detail_exec_money = self.new_find_element(By.ID, self.ELEMENT['his_bzxr_detail_exec_money']).text
            self.assertEqual(detail_exec_money, list_exec_money, '历史失信被执行人详情页执行标的列表页与详情页不符')
            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_bzxr_list_item"])
            self.assertEqual(int(bzxr_count), real_num, "历史失信被执行人实际数量{}与外侧count数量{}不相等".format(real_num, bzxr_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        """历史限制消费令维度"""
        log.info(self.test_001.__doc__)
        try:
            self.go_company_detail("山东常林机械集团股份有限公司")
            cname = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            xzxfl = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_xzxfl"], check_cover=True)
            xzxfl_count = self.new_find_element(By.XPATH, self.ELEMENT["his_xzxfl_count"]).text
            xzxfl.click()

            bzxr_hname = self.new_find_elements(By.ID, self.ELEMENT['his_xzxfl_list_hname'])
            bzxr_cname = self.new_find_elements(By.ID, self.ELEMENT['his_xzxfl_list_cname'])
            list_regdate = self.new_find_elements(By.ID, self.ELEMENT['his_xzxfl_list_regdate'])
            for i in list_regdate:
                self.assertTrue(check_time(i.text, is_compare=True), '历史限制消费令列表页立案时间校验错误')
            list_hname = bzxr_hname[0].text
            list_cname = bzxr_cname[0].text
            self.assertEqual(cname, list_cname, '')

            bzxr_cname[0].click()
            company_detail_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(company_detail_name, list_cname, '')
            self.driver.keyevent(4)

            bzxr_hname[0].click()
            human_detail_name = self.human_detail_name()
            self.assertEqual(human_detail_name, list_hname, '')
            self.driver.keyevent(4)

            self.new_find_elements(By.ID, self.ELEMENT['his_xzxfl_list_item'])[0].click()
            self.assertTrue(self.isElementExist(By.ID, 'com.tianyancha.skyeye:id/pdf_web_title_name'), '历史限制消费令详情页进入失败')
            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_xzxfl_list_item"])
            self.assertEqual(int(xzxfl_count), real_num, "历史限制消费令实际数量{}与外侧count数量{}不相等".format(real_num, xzxfl_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
