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
        cls.user = cls.account.get_account()
        cls.company_name = '四川同辉实业有限公司'

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.user)
        super().tearDownClass()

    @getimage
    def test_gfxx_tab_bg_0001(self):
        "未登录账号，点击「报告」，拉起登陆"
        log.info(self.test_gfxx_tab_bg_0001.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()
            # 点击 报告 按钮
            self.operation.new_find_element(By.ID, self.ELEMENT['click_report']).click()
            # 判断是否调起登陆
            login_text = self.operation.new_find_element(By.ID, self.ELEMENT['log_title']).text
            log.info("调起登陆文案：{}".format(login_text))
            self.assertEqual(login_text, '短信验证码登录')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_0002(self):
        "非VIP账号，显示下载次数"
        log.info(self.test_gfxx_tab_bg_0002.__doc__)
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
            down_text = self.operation.new_find_element(By.ID, self.ELEMENT['base_down_num']).text
            num = self.operation.count_num(By.ID, self.ELEMENT['base_down_num'])
            check_text = "今日剩余 {} 次".format(num)
            self.assertEqual(check_text, down_text, "预期文案：{}，实际文案：{}".format(check_text, down_text))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_0003(self):
        "登录非VIP账号，点击「报告」，下载基础版PDF，成功后进入到订单页"
        log.info(self.test_gfxx_tab_bg_0003.__doc__)
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

            # 是否能获取到 toast
            frequency = self.operation.new_find_element(By.ID, self.ELEMENT['base_down_num']).text
            if frequency == "今日次数已用尽":
                raise UserWarning("今日次数已用尽")

            # 选择报告格式为PDF
            self.company.report_format('pdf')

            # 点击 基础版报告的 立即下载
            self.operation.new_find_element(By.ID, self.ELEMENT['base_report']).click()

            # 是否进入订单页
            order_title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            title = "我的订单"
            self.assertEqual(title, order_title, "实际title：{}，待校验title：{}".format(order_title, title))
            # 校验订单类型
            order_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_type']).text
            check_type = "企业信用报告-基础版"
            self.assertEqual(check_type, order_type, "实际订单类型：{}，待校验title：{}".format(order_type, check_type))
            # 校验订单 报告目标
            order_report_name = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_name']).text
            self.assertEqual(self.company_name, order_report_name,
                             "实际报告目标名：{}，待校验目标名：{}".format(self.company_name, order_report_name))
            # 校验订单 报告格式
            order_report_format = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_format']).text
            check_report_format = 'PDF'
            self.assertEqual(check_report_format, order_report_format,
                             "实际报告格式：{}，待校验格式：{}".format(order_report_format, check_report_format))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_0004(self):
        "登录非VIP账号，点击「报告」，下载基础版PDF+WORD，成功后进入到订单页"
        log.info(self.test_gfxx_tab_bg_0004.__doc__)
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
            # 是否能获取到 toast
            frequency = self.operation.new_find_element(By.ID, self.ELEMENT['base_down_num']).text
            if frequency == "今日次数已用尽":
                raise UserWarning("今日次数已用尽")

            # 选择报告格式为PDF+WORD
            self.company.report_format('pdf+word')

            # 点击 基础版报告的 立即下载
            self.operation.new_find_element(By.ID, self.ELEMENT['base_report']).click()

            # 是否进入订单页
            order_title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            title = "我的订单"
            self.assertEqual(title, order_title, "实际title：{}，待校验title：{}".format(order_title, title))
            # 校验订单类型
            order_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_type']).text
            check_type = "企业信用报告-基础版"
            self.assertEqual(check_type, order_type, "实际订单类型：{}，待校验title：{}".format(order_type, check_type))
            # 校验订单 报告目标
            order_report_name = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_name']).text
            self.assertEqual(self.company_name, order_report_name,
                             "实际报告目标名：{}，待校验目标名：{}".format(self.company_name, order_report_name))
            # 校验订单 报告格式
            order_report_format = self.operation.new_find_element(By.XPATH, self.ELEMENT['order_report_format']).text
            check_report_format = 'PDF+Word'
            self.assertEqual(check_report_format, order_report_format,
                             "实际报告格式：{}，待校验格式：{}".format(order_report_format, check_report_format))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_0005(self):
        "非VIP账户，点击专业版+董监高+股权，弹出VIP购买框"
        log.info(self.test_gfxx_tab_bg_0005.__doc__)
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
            # 校验 专业版 下载按钮文案
            vip_report_text = self.operation.new_find_element(By.ID, self.ELEMENT['vip_report']).text
            check_report_text = "成为VIP会员，立即下载"
            self.assertEqual(check_report_text, vip_report_text,
                             "预期文案：{}，待校验文案：{}".format(check_report_text, vip_report_text))
            # 点击 专业版 报告
            self.operation.new_find_element(By.ID, self.ELEMENT['vip_report']).click()
            # 校验是否弹出 VIP购买框
            purchase_dialog_title = self.operation.new_find_element(By.ID, self.ELEMENT['vip_purchase_title']).text
            check_dialog_title = "无限次下载企业信用报告"
            self.assertIn(check_dialog_title, purchase_dialog_title,
                             "预期文案：{}，待校验文案：{}".format(check_dialog_title, purchase_dialog_title))
            self.operation.new_find_element(By.ID, self.ELEMENT['vip_purchase_close']).click()

            self.operation.swipeUp()
            # 点击董监高
            self.operation.new_find_element(By.XPATH, self.ELEMENT['vip_submit'].format(2)).click()
            # 校验是否弹出 VIP购买框
            purchase_dialog_title = self.operation.new_find_element(By.ID, self.ELEMENT['vip_purchase_title']).text
            check_dialog_title = "无限次下载董监高信用报告"
            self.assertIn(check_dialog_title, purchase_dialog_title,
                             "预期文案：{}，待校验文案：{}".format(check_dialog_title, purchase_dialog_title))
            self.operation.new_find_element(By.ID, self.ELEMENT['vip_purchase_close']).click()

            # 点击股权
            self.operation.new_find_element(By.XPATH, self.ELEMENT['vip_submit'].format(2)).click()
            # 校验是否弹出 VIP购买框
            purchase_dialog_title = self.operation.new_find_element(By.ID, self.ELEMENT['vip_purchase_title']).text
            check_dialog_title = "无限次下载董监高信用报告"
            self.assertIn(check_dialog_title, purchase_dialog_title,
                             "预期文案：{}，待校验文案：{}".format(check_dialog_title, purchase_dialog_title))


        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_bg_0006(self):
        "校验每个报告类型的说明文案"
        log.info(self.test_gfxx_tab_bg_0006.__doc__)
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
            # 获取 报告类型
            report_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['report_type'].format(2)).text
            # 校验 专业版报告说明
            self.company.check_caption_info(report_type, 2)

            # 获取 报告类型
            report_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['report_type'].format(3)).text
            # 校验 基础版报告说明
            self.company.check_caption_info(report_type, 3)

            # 滑动一屏
            self.operation.swipeUp()

            # 获取 报告类型
            report_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['report_type'].format(2)).text
            # 校验 董监高报告说明
            self.company.check_caption_info(report_type, 2)

            # 获取 报告类型
            report_type = self.operation.new_find_element(By.XPATH, self.ELEMENT['report_type'].format(3)).text
            # 校验 股权报告说明
            self.company.check_caption_info(report_type, 3)

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e





if __name__ == '__main__':
    unittest.main()
