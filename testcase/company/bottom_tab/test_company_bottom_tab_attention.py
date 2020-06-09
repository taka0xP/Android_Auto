#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/19
# @Author  : Soner
# @version : 1.0.0


import unittest
import time
from random import randint
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from common.operation import Operation
from common.operation import getimage
from Providers.logger import Logger, error_format
from Providers.company.company import CompanyFunc
from Providers.account.account import Account



log = Logger("公司底部TAB_关注").getlog()

class CompanyBottomTabAttention(MyTest):
    """
    公司底部TAB_关注
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
    def test_gfxx_tab_gz_0001(self):
        "未登录账号，点击「关注」，拉起登陆"
        log.info(self.test_gfxx_tab_gz_0001.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            collect_status = self.company.is_collect()
            log.info("关注状态：{}".format(collect_status))
            if collect_status:
                # 取消 关注
                self.company.click_collect()
            self.company.click_collect()
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
    def test_gfxx_tab_gz_0002(self):
        "登录账号，点击「关注」，弹出「选择分组」框"
        log.info(self.test_gfxx_tab_gz_0002.__doc__)
        try:
            login_status = self.operation.is_login()
            if not login_status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            collect_status = self.company.is_collect()
            log.info("关注状态：{}".format(collect_status))
            if collect_status:
                # 取消 关注
                self.company.click_collect()
            self.company.click_collect()
            collect_title = self.operation.new_find_element(By.ID, self.ELEMENT['email_title']).text
            text = "选择分组"
            self.assertEqual(text, collect_title, '获取的title：「{}」与预期值「{}」 不一致'.format(collect_title, text))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_gz_0003(self):
        "登录账号，点击「关注」，弹出「选择分组」框，选择「取消」，放弃关注操作"
        log.info(self.test_gfxx_tab_gz_0003.__doc__)
        try:
            login_status = self.operation.is_login()
            if not login_status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            collect_status = self.company.is_collect()
            log.info("关注状态：{}".format(collect_status))
            if collect_status:
                # 取消 关注
                self.company.click_collect()
            self.company.click_collect(collect_status=True)
            # 再次检测关注状态
            new_collect_status = self.company.is_collect()
            self.assertFalse(new_collect_status, "关注实际状态为：{}".format(new_collect_status))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_gz_0004(self):
        "登录账号，点击「关注」，弹出「选择分组」框，点击「确认」，关注列表出现该公司"
        log.info(self.test_gfxx_tab_gz_0004.__doc__)
        try:
            login_status = self.operation.is_login()
            if not login_status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            collect_status = self.company.is_collect()
            log.info("关注状态：{}".format(collect_status))
            if collect_status:
                # 取消 关注
                self.company.click_collect()
            self.company.click_collect(collect_status=True, click_status=True)
            # 进入 我的关注
            self.company.entry_collect()
            # 获取 第一个公司的名字（默认刚关注的排第一个）
            collect_list_status = self.company.exists_monitor_list(self.company_name)
            self.assertTrue(collect_list_status, '关注列表未找到 {}'.format(self.company_name))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_gz_0005(self):
        "登录账号，点击「关注」，弹出「选择分组」框，选择分组，点击「确定」"
        log.info(self.test_gfxx_tab_gz_0005.__doc__)
        try:
            login_status = self.operation.is_login()
            if not login_status:
                self.operation.login(phone_num=self.user, password=self.account.get_pwd())
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            log.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            # 是否有问大家
            self.company.ask_banner()
            log.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            collect_status = self.company.is_collect()
            log.info("关注状态：{}".format(collect_status))
            if collect_status:
                # 取消 关注
                self.company.click_collect()
            self.company.click_collect()
            # 选择分组框
            groups = self.operation.new_find_elements(By.XPATH, self.ELEMENT['collect_group'])
            rand = randint(1, len(groups))
            group = self.operation.new_find_element(By.XPATH, self.ELEMENT['collect_group']+"[{}]/android.widget.TextView".format(rand))
            # 获取分组名
            group_name = group.text
            group.click()
            # 点击确定
            self.operation.new_find_element(
                By.ID, self.ELEMENT['email_neg_pos']
            ).click()
            toast = self.company.operation.get_toast()
            text = "关注成功"
            self.assertEqual(text, toast, '获取的toast：「{}」与预期值「{}」 不一致'.format(toast, text))
            # 进入 我的-我的关注
            self.company.entry_collect()
            # 进入我的分组
            self.operation.new_find_element(By.ID, self.ELEMENT['my_group']).click()
            # 判断分组是否存在
            status = self.company.is_group(group_name)
            self.assertTrue(status, "关注公司 {} 不在分组中".format(self.company_name))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

if __name__ == '__main__':
    unittest.main()
