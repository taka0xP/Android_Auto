#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/20
# @Author  : Soner
# @version : 1.0.0


import unittest

from selenium.webdriver.common.by import By

from Providers.account.account import Account
from Providers.company.company import CompanyFunc
from Providers.logger import Logger, error_format
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from common.operation import Operation
from common.operation import getimage

log = Logger("公司底部TAB_报告").getlog()


class CompanyBottomTabReport(MyTest):
    """
    公司底部TAB_报告
    """
    a = Read_Ex()
    ELEMENT = a.read_excel("company_bottom_tab")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.operation = Operation(cls.driver)
        cls.company = CompanyFunc(cls.driver, cls.ELEMENT)
        cls.account = Account()
        cls.user = cls.account.get_account('vip')
        cls.company_name = '四川同辉实业有限公司'

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.user)
        super().tearDownClass()

    @getimage
    def test_gfxx_tab_bg_vip_0001(self):
        "VIP账号，不显示下载次数"
        global down_text
        down_text = None
        log.info(self.test_gfxx_tab_bg_vip_0001.__doc__)
        try:
            # 判断是否登录
            status = self.operation.is_login()
            if not status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()
            # 点击 报告 按钮
            self.operation.new_find_element(By.ID, self.ELEMENT['click_report']).click()
            down_status = self.operation.isElementExist(By.ID, self.ELEMENT['base_down_num'])
            if down_status:
                down_text = self.operation.new_find_element(By.ID, self.ELEMENT['base_down_num']).text
            self.assertFalse(down_status, "VIP账号不应该显示文案「{}」".format(down_text))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_vip_0002(self):
        "登录VIP账号，点击「报告」，下载专业版PDF，成功后进入到订单页"
        log.info(self.test_gfxx_tab_bg_vip_0002.__doc__)
        try:
            # 判断是否登录
            status = self.operation.is_login()
            if not status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()
            # 点击 报告 按钮
            self.operation.new_find_element(By.ID, self.ELEMENT['click_report']).click()

            # 选择报告格式为PDF
            self.company.report_format('pdf')

            # 获取 报告类型  2=专业版 3=基础版 4=董监高
            report_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['report_type'].format(2)).text
            # 点击 专业版报告的 立即下载
            self.operation.new_find_element(By.ID, self.ELEMENT['vip_report']).click()

            # 是否进入订单页
            order_title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            title = "我的订单"
            self.assertEqual(title, order_title, "预期title：{}，待校验title：{}，未进入到我的订单".format(title, order_title))
            # 校验订单类型
            order_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_type']).text
            self.assertEqual(report_type, order_type, "预期订单类型：{}，待校验订单类型：{}".format(report_type, order_type))
            # 校验订单 报告目标
            order_report_name = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_name']).text
            self.assertEqual(self.company_name, order_report_name,
                             "预期报告目标名：{}，待校验目标名：{}".format(self.company_name, order_report_name))
            # 校验订单 报告格式
            order_report_format = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_format']).text
            check_report_format = 'PDF'
            self.assertEqual(check_report_format, order_report_format,
                             "预期报告格式：{}，待校验格式：{}".format(check_report_format, order_report_format))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_vip_0003(self):
        "登录VIP账号，点击「报告」，下载专业版PDF+WORD，成功后进入到订单页"
        log.info(self.test_gfxx_tab_bg_vip_0003.__doc__)
        try:
            # 判断是否登录
            status = self.operation.is_login()
            if not status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()
            # 点击 报告 按钮
            self.operation.new_find_element(By.ID, self.ELEMENT['click_report']).click()
            # 选择报告格式为PDF
            self.company.report_format('pdf+word')

            # 获取 报告类型  2=专业版 3=基础版 4=董监高
            report_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['report_type'].format(2)).text
            # 点击 专业版报告的 立即下载
            self.operation.new_find_element(By.ID, self.ELEMENT['vip_report']).click()

            # 是否进入订单页
            order_title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            title = "我的订单"
            self.assertEqual(title, order_title, "预期title：{}，待校验title：{}，未进入到我的订单".format(title, order_title))
            # 校验订单类型
            order_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_type']).text
            self.assertEqual(report_type, order_type, "预期订单类型：{}，待校验订单类型：{}".format(report_type, order_type))
            # 校验订单 报告目标
            order_report_name = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_name']).text
            self.assertEqual(self.company_name, order_report_name,
                             "预期报告目标名：{}，待校验目标名：{}".format(self.company_name, order_report_name))
            # 校验订单 报告格式
            order_report_format = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_format']).text
            check_report_format = 'PDF+Word'
            self.assertEqual(check_report_format, order_report_format,
                             "预期报告格式：{}，待校验格式：{}".format(check_report_format, order_report_format))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_vip_0004(self):
        "登录VIP账号，点击「报告」，下载股权结构，成功后进入到订单页"
        log.info(self.test_gfxx_tab_bg_vip_0004.__doc__)
        try:
            # 判断是否登录
            status = self.operation.is_login()
            if not status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()
            # 点击 报告 按钮
            self.operation.new_find_element(By.ID, self.ELEMENT['click_report']).click()
            # 选择报告格式为PDF
            self.company.report_format('pdf')

            # 上滑一屏
            self.operation.swipeUp()
            # 获取 报告类型
            report_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['report_type'].format(3)).text

            # 点击 报告的 立即下载
            self.operation.new_find_element(By.XPATH, self.ELEMENT['vip_submit'].format(3)).click()

            # 是否进入订单页
            order_title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            title = "我的订单"
            self.assertEqual(title, order_title, "预期title：{}，待校验title：{}，未进入到我的订单".format(title, order_title))
            # 校验订单类型
            order_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_type']).text
            self.assertIn(report_type, order_type, "预期订单类型：{}，待校验订单类型：{}".format(report_type, order_type))
            # 校验订单 报告目标
            order_report_name = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_name']).text
            self.assertEqual(self.company_name, order_report_name,
                             "预期报告目标名：{}，待校验目标名：{}".format(self.company_name, order_report_name))
            # 校验订单 报告格式
            order_report_format = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_format']).text
            check_report_format = 'PDF'
            self.assertEqual(check_report_format, order_report_format,
                             "预期报告格式：{}，待校验格式：{}".format(check_report_format, order_report_format))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_vip_0005(self):
        "登录VIP账号，校验董监高最对选择6人"
        log.info(self.test_gfxx_tab_bg_vip_0005.__doc__)
        try:
            company_name = "南昌亨得利股份有限公司"
            # 判断是否登录
            status = self.operation.is_login()
            if not status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()

            # 点击 报告 按钮
            self.operation.new_find_element(By.ID, self.ELEMENT['click_report']).click()

            # 上滑一屏
            self.operation.swipeUp()
            # 获取 报告类型
            report_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['report_type'].format(2)).text
            # 点击 报告的 立即下载
            self.operation.new_find_element(By.XPATH, self.ELEMENT['vip_submit'].format(2)).click()

            # 是否弹出选择人员页
            select_people_title = self.operation.isElementExist(By.ID, self.ELEMENT['select_people_title'])
            self.assertTrue(select_people_title, "选择人员页未展示")
            # people_page = self.operation.new_find_elements(By.XPATH, self.ELEMENT['people_page'])
            select_people_list = list()
            for i in range(1,8):
                people = self.operation.new_find_element(By.XPATH, self.ELEMENT['people_page'].format(i))
                if i < 7:
                    select_people_list.append(people.text)
                if i != 1:
                    people.click()
                log.info("选择的人员列表：{}".format(select_people_list))
            toast = self.operation.get_toast()
            expect_toast = "最多可选6个人"
            self.assertEqual(expect_toast, toast, "预期toast：{}，实际toast：{}".format(expect_toast, toast))

            # 点击 完成 按钮
            self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_complete").click()

            # 是否进入订单页
            order_title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            title = "我的订单"
            self.assertEqual(title, order_title, "预期title：{}，待校验title：{}，未进入到我的订单".format(title, order_title))
            # 校验订单类型
            order_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_type']).text
            self.assertIn(report_type, order_type, "预期订单类型：{}，待校验订单类型：{}".format(report_type, order_type))
            # 校验订单 报告目标
            order_report_name = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_name']).text
            self.assertEqual(company_name, order_report_name,
                             "预期报告目标名：{}，待校验目标名：{}".format(company_name, order_report_name))
            # 校验相关人员
            people_result = self.operation.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/pre_paid_recycler']/android.widget.LinearLayout[1]//*[@resource-id='com.tianyancha.skyeye:id/person_about_tv']").text
            people_result_list = people_result.split('、')
            self.assertListEqual(select_people_list, people_result_list, "选择列表：{}、实际列表：{}".format(select_people_list, people_result_list))


        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_vip_0006(self):
        "信用报告_校验邮箱格式"
        log.info(self.test_gfxx_tab_bg_vip_0006.__doc__)
        try:
            # 判断是否登录
            status = self.operation.is_login()
            if not status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()
            # 点击 报告 按钮
            self.operation.new_find_element(By.ID, self.ELEMENT['click_report']).click()

            # 校验 非邮箱 格式
            self.operation.adb_send_input(By.ID, self.ELEMENT['email_report'], 'adfads', self.device)
            # 点击 专业版报告的 立即下载
            self.operation.new_find_element(By.ID, self.ELEMENT['vip_report']).click()
            toast = self.operation.get_toast()
            email_format = "邮箱格式不正确"
            self.assertEqual(email_format, toast, "预期toast：{}，待校验toast：{}".format(email_format, toast))

            # 校验 带汉字 格式
            self.operation.adb_send_input(By.ID, self.ELEMENT['email_report'], '时代峻峰了@ds.com', self.device)
            # 点击 专业版报告的 立即下载
            self.operation.new_find_element(By.ID, self.ELEMENT['vip_report']).click()
            toast = self.operation.get_toast()
            self.assertEqual(email_format, toast, "预期toast：{}，待校验toast：{}".format(email_format, toast))

            # 校验 带特殊字符 格式
            self.operation.adb_send_input(By.ID, self.ELEMENT['email_report'], 'lijun~!$@tianyancha.com', self.device)
            # 点击 专业版报告的 立即下载
            self.operation.new_find_element(By.ID, self.ELEMENT['vip_report']).click()
            toast = self.operation.get_toast()
            self.assertEqual(email_format, toast, "预期toast：{}，待校验toast：{}".format(email_format, toast))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e


if __name__ == '__main__':
    unittest.main()
