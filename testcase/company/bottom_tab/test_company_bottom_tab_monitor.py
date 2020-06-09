#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/3
# @Author  : Soner
# @version : 1.0.0

import unittest
import time
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from common.operation import Operation
from common.operation import getimage
from Providers.logger import Logger, error_format
from Providers.company.company import CompanyFunc
from Providers.account.account import Account


log = Logger("公司底部TAB_监控").getlog()
class CompanyBottomTab(MyTest):
    """
    公司底部TAB_监控
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
        cls.company_name = '宝宝巴士（福建）网络科技有限公司'

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.user)
        super().tearDownClass()

    @getimage
    def test_gfxx_tab_jk_0001(self):
        "未登录账号，点击「监控」，拉起登陆"
        log.info(self.test_gfxx_tab_jk_0001.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 公司是否被监控
            monitor = self.company.is_monitor()
            log.info("监控状态：{}".format(monitor))
            if monitor:
                # 取消 「监控」
                self.company.click_monitor(monitor_status=True)
                time.sleep(2)
            # 点击「监控」
            self.company.click_monitor()
            # 判断是否调起登陆
            login_text = self.operation.new_find_element(By.ID, self.ELEMENT["log_title"]).text
            text = "短信验证码登录"
            self.assertEqual(login_text, text, "获取的文案 {}，实际文案：{}".format(login_text, text))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_jk_0002(self):
        "未监控该公司，点击「监控」，toast提示“监控成功”且出现在监控列表"
        log.info(self.test_gfxx_tab_jk_0002.__doc__)
        try:
            # 判断是否登录
            login_status = self.operation.is_login()
            if not login_status:
                # 未登录则登录
                self.operation.login(self.user, self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()
            # 公司是否被监控
            monitor = self.company.is_monitor()
            log.info("监控状态：{}".format(monitor))
            if monitor:
                # 取消 「监控」
                self.company.click_monitor(monitor_status=monitor)
                time.sleep(2)
            # 点击「监控」
            text = "监控成功"
            self.company.click_monitor()
            toast = self.operation.get_toast()
            self.assertEqual(text, toast, "获取的toast：「{}」与预期值「{}」 不一致".format(toast, text))
            # 账号是否是第一次监控，是的话需要关闭填写邮箱
            self.company.is_first_monitor()
            # 判断监控列表是否存在
            self.company.entry_monitor()
            status = self.company.exists_monitor_list(self.company_name)
            self.assertTrue(status, "监控列表未找到 {}".format(self.company_name))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_jk_0003(self):
        "监控列表取消监控，在公司详情页，监控状态为「未监控」"
        log.info(self.test_gfxx_tab_jk_0003.__doc__)
        try:
            # 判断是否登录
            status = self.operation.is_login()
            if not status:
                self.operation.login(phone_num="11099995021", password=self.account.get_pwd())
            # 进入监控列表页
            self.company.entry_monitor()
            # 监控列表页是否有监控
            status = self.company.monitor_list_info()
            if not status:
                raise AssertionError("监控列表没有任何监控")
            # 将第一个监控取消，并获得该公司名字
            company_name = self.operation.new_find_element(By.XPATH, self.ELEMENT["monitor_list_company_name"].format(1)).text
            log.info("待取消监控的公司名称：{}".format(company_name))
            # 点击 取消监控
            self.operation.new_find_element(By.XPATH, self.ELEMENT["cancel_monitor"].format(1)).click()
            toast = self.operation.get_toast()
            text = "已取消监控"
            self.assertEqual(text, toast, "获取的toast：「{}」与预期值「{}」 不一致".format(toast, text))
            # 进入公司详情页
            self.company.search_company(company_name, self.device)
            # 获取监控状态
            monitor_status = self.company.is_monitor()
            self.assertFalse(monitor_status, "{} 的监控状态为{}".format(company_name, monitor_status))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_jk_0004(self):
        "点击「已监控」，弹窗提示，点击「我在想想」，放弃取消监控操作"
        log.info(self.test_gfxx_tab_jk_0004.__doc__)
        try:
            login_status = self.operation.is_login()
            if not login_status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 进入 公司详情页
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 公司是否被监控
            monitor = self.company.is_monitor()
            log.info("监控状态：{}".format(monitor))
            if not monitor:
                self.company.click_monitor()
            # 点击取消监控，并点击「我在想想」
            self.company.click_monitor(monitor_status=True, click_status=True)
            # 再次查看 监控 状态
            monitor_status = self.company.is_monitor()
            self.assertTrue(monitor_status, "实际监控状态：{}".format(monitor_status))
        except AssertionError:
            raise self.failureException
        except Exception as e:
            log.error(error_format(e))

    @getimage
    def test_gfxx_tab_jk_0005(self):
        "点击「已监控」，弹窗提示，点击「确认」，执行取消监控操作"
        log.info(self.test_gfxx_tab_jk_0005.__doc__)
        try:
            login_status = self.operation.is_login()
            if not login_status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 进入 公司详情页
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 公司是否被监控
            monitor = self.company.is_monitor()
            log.info("监控状态：{}".format(monitor))
            if not monitor:
                self.company.click_monitor()
            # 点击取消监控，并点击「确认」
            self.company.click_monitor(monitor_status=True)
            toast = self.operation.get_toast()
            text = "已取消监控"
            self.assertEqual(text, toast, "获取的toast：「{}」与预期值「{}」 不一致".format(toast, text))
            # 再次查看 监控 状态
            monitor_status = self.company.is_monitor()
            self.assertFalse(monitor_status, "实际监控状态：{}".format(monitor_status))
        except AssertionError:
            raise self.failureException
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_jk_0006(self):
        "点击「已监控」，弹窗提示，点击任意非弹窗区域，隐藏弹窗"
        log.info(self.test_gfxx_tab_jk_0006.__doc__)
        try:
            login_status = self.operation.is_login()
            if not login_status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 进入 公司详情页
            self.company.search_company(self.company_name, self.device)
            # 是否有 问大家 条幅
            self.company.ask_banner()
            # 公司是否被监控
            monitor = self.company.is_monitor()
            log.info("监控状态：{}".format(monitor))
            if not monitor:
                self.company.click_monitor()
            # 点击取消监控，弹出提示框
            self.company.click_monitor()
            # 账号是否是第一次监控，是的话需要关闭填写邮箱
            self.company.is_first_monitor(outtime=5)
            # 点击 弹框外任意区域，取消弹框
            TouchAction(self.driver).press(x=300, y=500).release().perform()
            # 再次查看 监控 状态
            monitor_status = self.company.is_monitor()
            self.assertTrue(monitor_status, "实际监控状态：{}".format(monitor_status))
        except AssertionError:
            raise self.failureException
        except Exception as e:
            log.error(error_format(e))
            raise e


if __name__ == "__main__":
    unittest.main()
