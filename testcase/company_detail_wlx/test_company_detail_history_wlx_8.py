# -*- coding: utf-8 -*-
# @Time    : 2020-03-23 18:30
# @Author  : wlx
# @File    : company_detail_history_info.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep, time
from Providers.logger import Logger, error_format
from common.check_rules import *

log = Logger("历史信息_08").getlog()


class Company_detail_Test_wlx_8(MyTest, Operation):
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
        """历史终本案件维度"""
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.go_company_detail("山东常林机械集团股份有限公司")
            cname = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            zbaj = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_zbaj"])
            zbaj_count = self.new_find_element(By.XPATH, self.ELEMENT["his_zbaj_count"]).text
            zbaj.click()

            list_cname = self.new_find_elements(By.ID, self.ELEMENT['his_zbaj_list_cname'])[0].text
            self.assertEqual(list_cname, cname, '历史终本案件列表页公司名称与当前公司名称不符')

            list_case_num = self.new_find_elements(By.ID, self.ELEMENT['his_zbaj_list_case_num'])[0].text
            list_regdate = self.new_find_elements(By.ID, self.ELEMENT['his_zbaj_list_regdate'])[0].text
            self.new_find_elements(By.ID, self.ELEMENT['his_zbaj_list_item'])[0].click()

            detail_company = self.new_find_element(By.ID, self.ELEMENT['his_zbaj_detail_company'])
            zbaj_detail_company = detail_company.text
            self.assertEqual(list_cname, zbaj_detail_company, '历史终本案件详情页名称与当前公司名不符')
            detail_company.click()
            jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(jump_name, zbaj_detail_company, '历史终本案件详情页跳转公司详情页公司名称不对应')
            self.driver.keyevent(4)

            detail_case_num = self.new_find_element(By.ID, self.ELEMENT['his_zbaj_detail_case_num']).text
            self.assertEqual(detail_case_num, list_case_num, '历史终本案件详情页案号字段与列表页不匹配')

            detail_regdate = self.new_find_element(By.ID, self.ELEMENT['his_zbaj_detail_regdate']).text
            self.assertEqual(detail_regdate, list_regdate, '历史终本案件详情页立案日期字段与列表页不匹配')
            self.assertTrue(check_time(detail_regdate, is_compare=True), '历史终本案件详情页立案日期字段校验错误')

            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_zbaj_list_item"])
            self.assertEqual(int(zbaj_count), real_num, "历史终本案件实际数量{}与外侧count数量{}不相等".format(real_num, zbaj_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        """历史司法协助维度"""
        log.info(self.test_002.__doc__)
        try:
            self.go_company_detail("天津市海王星海上工程技术股份有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            sfxz = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sfxz"])
            sfxz_count = self.new_find_element(By.XPATH, self.ELEMENT["his_sfxz_count"]).text
            sfxz.click()

            list_name = self.new_find_elements(By.ID, self.ELEMENT['his_sfxz_list_name'])[2].text
            list_exec_money = self.new_find_elements(By.ID, self.ELEMENT['his_sfxz_list_exec_money'])[2].text
            list_case_num = self.new_find_elements(By.ID, self.ELEMENT['his_sfxz_list_case_num'])[2].text
            type = self.new_find_elements(By.ID, self.ELEMENT['his_sfxz_list_type'])[2].text
            list_type = type.replace(' ', '')
            print(list_type)
            print(self.new_find_elements(By.ID, self.ELEMENT['his_sfxz_list_item'])[2])
            self.new_find_elements(By.ID, self.ELEMENT['his_sfxz_list_item'])[2].click()

            detail_company = self.new_find_element(By.ID, self.ELEMENT['his_sfxz_detail_company'])
            sfxz_detail_company = detail_company.text
            self.assertEqual(list_name, sfxz_detail_company, '历史司法协助详情页被执行人名称与当前公司名不符')
            detail_company.click()
            if self.isElementExist(By.ID, self.ELEMENT["human_detail_name"]):
                jump_name = self.human_detail_name()
            else:
                jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(jump_name, sfxz_detail_company, '历史司法协助详情页跳转公司详情页公司名称不对应')
            self.driver.keyevent(4)

            detail_type = self.new_find_element(By.ID, self.ELEMENT['his_sfxz_detail_type']).text
            self.assertEqual(detail_type, list_type, '历史司法协助详情页类型状态字段与列表页不匹配')

            detail_case_num = self.new_find_element(By.ID, self.ELEMENT['his_sfxz_detail_case_num']).text
            self.assertEqual(detail_case_num, list_case_num, '历史司法协助案号字段与列表页不匹配')

            detail_exec_money = self.new_find_element(By.ID, self.ELEMENT['his_sfxz_detail_exec_money']).text
            self.assertEqual(detail_exec_money, list_exec_money, '历史司法协助详情页股权数额列表页与详情页不符')

            self.new_find_element(By.ID, self.ELEMENT['his_sfxz_detail_open_icon']).click()
            self.assertFalse(self.isElementExist(By.ID, self.ELEMENT['his_sfxz_detail_type']), '历史司法协助收起按钮无法收起')

            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_sfxz_list_item"])
            self.assertEqual(int(sfxz_count), real_num, "历史司法协助实际数量{}与外侧count数量{}不相等".format(real_num, sfxz_count, ))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
    @getimage
    def test_003(self):
        """历史经营异常维度"""
        log.info(self.test_003.__doc__)
        try:
            self.go_company_detail("一帆鱼塘")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            jyyc = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_jyyc"], check_cover=True)
            jyyc_count = self.new_find_element(By.XPATH, self.ELEMENT["his_jyyc_count"]).text
            jyyc.click()

            put_date = self.new_find_elements(By.ID, self.ELEMENT['his_jyyc_put_date'])[0].text
            self.assertTrue(check_time(put_date, is_compare=True), '经营异常列入日期校验错误')

            remove_date = self.new_find_elements(By.ID, self.ELEMENT['his_jyyc_remove_date'])[0].text
            self.assertTrue(check_time(remove_date, is_compare=True), '历史经营异常移出日期校验错误')

            self.assertTrue(self.isElementExist(By.ID, self.ELEMENT['his_jyyc_put_reason']), '历史经营异常列入原因字段检验错误')
            self.assertTrue(self.isElementExist(By.ID, self.ELEMENT['his_jyyc_remove_reason']), '历史经营异常移出原因字段检验错误')
            self.assertTrue(self.isElementExist(By.ID, self.ELEMENT['his_jyyc_put_department']), '历史经营异常决定机关字段检验错误')

            real_num = self.all_count_compute_v1(By.XPATH, self.ELEMENT["his_jyyc_list_item"])
            self.assertEqual(int(jyyc_count), real_num, "历史经营异常实际数量{}与外侧count数量{}不相等".format(real_num, jyyc_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e