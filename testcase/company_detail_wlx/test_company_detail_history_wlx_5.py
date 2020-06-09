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
from common.check_rules import *

log = Logger("历史信息_05").getlog()


class Company_detail_Test_wlx_5(MyTest, Operation):
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
        """历史对外投资维度"""
        log.info(self.test_003.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.go_company_detail("宁夏天元锰业集团有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            out_money = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_dytz"])
            out_money_count = self.new_find_element(
                By.XPATH, self.ELEMENT["his_dytz_count"]
            ).text
            # print(out_money_count)
            out_money.click()

            # 经营状态
            operates = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_jyzt"])
            for n in operates:
                self.assertTrue(operating_check(1, n.text), "公司详情页-历史信息-对外投资列表经营状态字段校验错误")
            # 投资数额
            out_num = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_tzse"])
            for n in out_num:
                self.assertTrue(is_bill_available(n.text), "公司详情页-历史信息-对外投资列表投资数额字段校验错误")
            # 投资比例
            percent = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_tzbl"])
            for n in percent:
                self.assertTrue(
                    is_percentage_available(n.text), "公司详情页-历史信息-对外投资列表投资比例字段校验错误"
                )
            # 成立日期
            date = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_clrq"])
            for n in date:
                self.assertTrue(check_time(n.text), "公司详情页-历史信息-对外投资列表成立日期字段校验错误")

            click_company = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_company"])[
                0
            ]
            click_name = click_company.text
            click_company.click()
            jump_name = self.new_find_element(
                By.ID, self.ELEMENT["detail_company_name"]
            ).text
            self.assertEqual(
                click_name,
                jump_name,
                "对外投资公司展示名称{}和跳转详情页名称{}不一致".format(click_name, jump_name),
            )
            self.driver.keyevent(4)
            self.new_find_elements(By.ID, self.ELEMENT["his_dytz_pic"])[0].click()
            title = self.new_find_element(By.ID, self.ELEMENT["app_page_title"]).text
            self.assertEqual(title, "股权结构", "对外投资股权结构跳转失败")
            self.driver.keyevent(4)
            law_person = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_law_person"])[
                0
            ]
            law_name = law_person.text
            law_person.click()
            jump_law_name = self.human_detail_name()
            self.assertEqual(
                law_name,
                jump_law_name,
                "对外投资法定代表人外侧名称{}和详情页名称{}不一致".format(law_name, jump_law_name)
            )
            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_dytz_item"])
            self.assertEqual(
                int(out_money_count),
                real_num,
                "历史对外投资实际数量{}与外侧count数量{}不相等".format(real_num, out_money_count)
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
    @getimage
    def test_002(self):
        """历史股东维度"""
        log.info(self.test_002.__doc__)
        try:
            self.go_company_detail("宁夏天元锰业")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            his_boss = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_lsgd"])
            his_boss_count = self.new_find_element(By.XPATH, self.ELEMENT["his_lsgd_count"]).text
            his_boss.click()

            # 认缴出资数额
            out_num = self.new_find_elements(By.XPATH, self.ELEMENT["his_dytz_rjcz"])
            for n in out_num:
                self.assertTrue(is_bill_available(n.text),'公司详情页-历史信息-历史股东认缴出资数额字段校验错误')

            # 认缴出资日期
            pay_date = self.new_find_elements(By.XPATH, self.ELEMENT["his_dytz_rjczrq"])
            for n in pay_date:
                self.assertTrue(check_time(n.text,is_compare=True), '公司详情页-历史信息-历史股东认缴出资日期字段校验错误')
            # 参股日期
            in_date = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_cgrq"])
            for n in in_date:
                self.assertTrue(check_time(n.text,is_compare=True), '公司详情页-历史信息-历史股东参股日期字段校验错误')
            # 退股日期
            out_date = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_tgrq"])
            for n in out_date:
                self.assertTrue(check_time(n.text,is_compare=True), '公司详情页-历史信息-历史股东退股日期字段校验错误')

            # 持股比例
            percent = self.new_find_elements(By.ID, self.ELEMENT["his_dytz_chigubl"])
            for n in percent:
                self.assertTrue(is_percentage_available(n.text), '公司详情页-历史信息-历史股东持股比例字段校验错误')
            # 公司跳转+股权结构跳转
            click_company = self.new_find_elements(By.XPATH, self.ELEMENT["his_lsgd_company"])[0]
            click_name = click_company.text
            click_company.click()
            jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(
                click_name,
                jump_name,
                "历史股东公司展示名称{}和跳转详情页名称{}不一致".format(click_name, jump_name)
            )
            self.driver.keyevent(4)
            self.new_find_elements(By.ID, self.ELEMENT["his_dytz_gqjg"])[0].click()
            title = self.new_find_element(By.ID, self.ELEMENT["app_page_title"]).text
            self.assertEqual(title, "股权结构", "历史股东股权结构跳转失败")
            self.driver.keyevent(4)

            # 人员跳转
            his_boss_name = self.new_find_elements(By.XPATH,self.ELEMENT['his_lsgd_name'])[0]
            law_name = his_boss_name.text
            his_boss_name.click()
            jump_law_name = self.human_detail_name()
            self.assertEqual(
                law_name,
                jump_law_name,
                "历史股东法定代表人外侧名称{}和详情页名称{}不一致".format(law_name, jump_law_name)
            )
            self.driver.keyevent(4)


            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_lsgd_item"])
            self.assertEqual(
                int(his_boss_count),
                real_num,
                "历史股东实际数量{}与外侧count数量{}不相等".format(real_num,his_boss_count)
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
    @getimage
    def test_003(self):
        """历史开庭公告维度"""
        log.info(self.test_003.__doc__)
        try:
            self.go_company_detail("滴滴")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_dytz"])
            ktgg = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_ktgg"],check_cover=True)
            ktgg_count = self.new_find_element(By.XPATH, self.ELEMENT["his_ktgg_count"]).text
            ktgg.click()

            list_case_reason = self.new_find_elements(By.ID,self.ELEMENT['his_ktgg_list_title'])
            list_case_reason_1 = list_case_reason[1].text
            list_start_time = self.new_find_elements(By.ID,self.ELEMENT['his_ktgg_list_start_time'])
            for n in list_start_time:
                self.assertTrue(check_time(n.text, is_compare=True), '公司详情页-历史信息-开庭公告列表开庭日期日期字段校验错误')
            list_start_time_1 = list_start_time[1].text
            list_case_num = self.new_find_elements(By.ID,self.ELEMENT['his_ktgg_list_case_num'])[1].text
            list_plaintiff = self.ocr(By.XPATH,self.ELEMENT['his_ktgg_list_plaintiff'])
            list_defendant = self.ocr(By.XPATH,self.ELEMENT['his_ktgg_list_defendant'])

            list_case_reason[1].click()

            detail_case_reason = self.new_find_element(By.ID,self.ELEMENT['his_ktgg_detail_case_reason']).text
            self.assertEqual(detail_case_reason,list_case_reason_1,'历史信息-开庭公告列表页案由和详情页案由内容不一致')

            detail_case_num = self.new_find_element(By.ID,self.ELEMENT['his_ktgg_detail_case_num']).text
            self.assertEqual(detail_case_num,list_case_num,'历史信息-开庭公告列表页案号和详情页案号内容不一致')

            detail_plaintiff = self.new_find_element(By.XPATH,self.ELEMENT['his_ktgg_detail_plaintiff']).text
            # print(detail_plaintiff,'--------',list_plaintiff)
            self.assertEqual(detail_plaintiff,list_plaintiff,'历史信息-开庭公告列表页原告和详情页原告内容不一致')

            detail_defendant = self.new_find_element(By.XPATH,self.ELEMENT['his_ktgg_detail_defendant']).text
            self.assertEqual(detail_defendant,list_defendant,'历史信息-开庭公告列表页被告和详情页被告内容不一致')

            detail_start_time = self.new_find_element(By.ID,self.ELEMENT['his_ktgg_detail_start_time']).text
            self.assertEqual(detail_start_time,list_start_time_1,'历史信息-开庭公告列表页开庭时间和详情页开庭时间不一致')
            self.assertTrue(check_time(detail_start_time), '公司详情页-历史信息-开庭公告详情页开庭日期日期字段校验错误')

            schedule_time = self.new_find_element(By.ID,self.ELEMENT['his_ktgg_detail_schedule_time']).text
            self.assertTrue(check_time(schedule_time), '公司详情页-历史信息-开庭公告详情页开庭排期日期日期字段校验错误')

            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_ktgg_item"])
            self.assertEqual(
                int(ktgg_count),
                real_num,
                "历史开庭公告实际数量{}与外侧count数量{}不相等".format(real_num, ktgg_count)
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e