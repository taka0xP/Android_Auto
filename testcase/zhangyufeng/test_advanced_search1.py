# -*- coding: utf-8 -*-
# @Time    : 2020-05-26 14:42
# @Author  : ZYF
# @File    : test_advanced_search1.py

import time
import random
import unittest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger
from Providers.account.account import Account

log = Logger('金刚区_高级搜索').getlog()
class Advanced_search(MyTest, Operation):
    """金刚区_高级搜索"""
    a = Read_Ex()
    ELEMENT = a.read_excel('All_server')

    def in_allserver(self, value, size=1):
        """
        金刚区 全部服务进入对应的入口
        value: 模块名称
        example: cll(查老赖)
        """
        self.value = value
        self.new_find_elements(By.ID, self.ELEMENT['king_area'])[4].click()
        if size is 1:
            pass
        else:
            self.swipeUp()
        self.new_find_element(By.XPATH, self.ELEMENT[self.value]).click()

    def hit_login(self, account='18535081116', password='zyf643163'):
        """
        点击操作正好遇到需要登录的时候使用
        :param account: 账号
        :param password: 密码
        """
        try:
            loc = (By.XPATH, '//*[@class="android.widget.TextView" and @text="短信验证码登录"]')
            login = self.isElementExist(*loc)
            if login:
                self.new_find_element(By.XPATH, "//*[@class='android.widget.TextView' and @text='密码登录']").click()
                self.new_find_element(By.XPATH, "//*[@class='android.widget.EditText' and @text='输入手机号']").send_keys(account)
                self.new_find_element(By.XPATH, "//*[@class='android.widget.EditText' and @text='输入密码']").send_keys(password)
                # 点击勾选协议
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/cb_login_check").click()
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_login").click()
                time.sleep(1)
            else:
                pass
        except Exception as e:
            print(e, '用户已登录')
            pass

    @getimage
    def test_001_jgq_gjss_p0(self):
        """
        金刚区-进入高级搜索页面
        """
        log.info(self.test_001_jgq_gjss_p0.__doc__)
        try:
            self.in_allserver('gjss')
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual('高级搜索', page_title, msg='页面title不一致')
            title1 = self.new_find_element(By.ID, self.ELEMENT['advance_search_keyword_input_et']).text
            self.assertEqual('请输入关键词（非必填）', title1, msg='页面标识不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_002_jgq_gjss_p0(self):
        """
        金刚区-进入高级搜索页面
        用户未登查看结果---调起登录
        普通用户查看结果---开通VIP
        """
        log.info(self.test_001_jgq_gjss_p0.__doc__)
        try:
            self.in_allserver('gjss')
            # 关键字搜索---有限公司
            self.new_find_element(By.ID, self.ELEMENT['advance_search_keyword_input_et']).send_keys('有限公司')
            # 点击「查看结果」
            self.new_find_element(By.ID, self.ELEMENT['advance_search_check_result_tv']).click()
            log.info("未登录查看结果拉起登录")
            login = self.isElementExist(By.ID, self.ELEMENT['btv_title'])
            self.assertTrue(login)
            # 获取普通账号登录
            account = Account()
            acc_pt_name = account.get_account('account')
            acc_pwd = account.get_pwd()
            log.info("登录普通账号:{},账号密码:{}".format(acc_pt_name, acc_pwd))
            # 登录普通账号
            self.hit_login(account=acc_pt_name, password=acc_pwd)
            # 普通账号没有权限----调起VIP弹框
            VIP = self.new_find_element(By.ID, self.ELEMENT['tv_top_title']).text
            self.assertEqual(VIP, "开通VIP会员使用高级搜索")
            # 账号退出
            self.logout()
            # 退还账号
            account.release_account(acc_pt_name, "account")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_003_jgq_gjss_p0(self):
        """
        金刚区-进入高级搜索页面
        VIP用户登查看结果---
        """
        log.info(self.test_001_jgq_gjss_p0.__doc__)
        try:
            self.in_allserver('gjss')
            # 关键字搜索---有限公司
            self.new_find_element(By.ID, self.ELEMENT['advance_search_keyword_input_et']).send_keys('有限公司')
            # 点击「查看结果」
            self.new_find_element(By.ID, self.ELEMENT['advance_search_check_result_tv']).click()
            log.info("未登录查看结果拉起登录")
            login = self.isElementExist(By.ID, self.ELEMENT['btv_title'])
            self.assertTrue(login)
            # 获取VIP账号登录
            account = Account()
            acc_vip_name = account.get_account('vip')
            acc_pwd = account.get_pwd()
            log.info("登录VIP账号:{},账号密码:{}".format(acc_vip_name, acc_pwd))
            # 登录vip账号
            self.new_find_element(By.ID, self.ELEMENT['et_phone']).clear()
            self.hit_login(account=acc_vip_name, password=acc_pwd)
            # 登录后进入搜索结果页
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            log.info("搜素结果页页面title:{}".format(page_title))
            self.assertEqual(page_title, "搜索结果")
            self.logout()
            account.release_account(acc_vip_name, "vip")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_004_jgq_gjss_p0(self):
        """
        金刚区-进入高级搜索页面
        VIP用户登查看有结果
        """
        log.info(self.test_001_jgq_gjss_p0.__doc__)
        try:
            # 获取普通账号登录
            account = Account()
            acc_vip_name = account.get_account('vip')
            acc_pwd = account.get_pwd()
            log.info("登录普通账号:{},账号密码:{}".format(acc_vip_name, acc_pwd))
            # 登录vip账号
            self.login(phone_num=acc_vip_name, password=acc_pwd)
            self.in_allserver('gjss')
            # 关键字搜索---有限公司
            self.new_find_element(By.ID, self.ELEMENT['advance_search_keyword_input_et']).send_keys('有限公司')
            # 点击「查看结果」
            self.new_find_element(By.ID, self.ELEMENT['advance_search_check_result_tv']).click()
            # 进入搜索结果页
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            log.info("搜素结果页页面title:{}".format(page_title))
            self.assertEqual(page_title, "搜索结果")
            result = self.isElementExist(By.ID, self.ELEMENT['advance_search_result_count'])
            self.assertTrue(result)
            self.logout()
            account.release_account(acc_vip_name, "vip")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_005_jgq_gjss_p0(self):
        """
        金刚区-进入高级搜索页面
        VIP用户登查看无结果---我也是醉了基金
        """
        log.info(self.test_001_jgq_gjss_p0.__doc__)
        try:
            # 获取普通账号登录
            account = Account()
            acc_vip_name = account.get_account('vip')
            acc_pwd = account.get_pwd()
            log.info("登录普通账号:{},账号密码:{}".format(acc_vip_name, acc_pwd))
            # 登录vip账号
            self.login(phone_num=acc_vip_name, password=acc_pwd)
            self.in_allserver('gjss')
            # 关键字搜索---有限公司
            self.new_find_element(By.ID, self.ELEMENT['advance_search_keyword_input_et']).send_keys('我也是醉了基金')
            # 点击「查看结果」
            self.new_find_element(By.ID, self.ELEMENT['advance_search_check_result_tv']).click()
            # 进入搜索结果页
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            log.info("搜素结果页页面title:{}".format(page_title))
            self.assertEqual(page_title, "搜索结果")
            result = self.isElementExist(By.ID, self.ELEMENT['advance_search_result_count'])
            self.assertFalse(result)
            no_result = self.new_find_element(By.ID, self.ELEMENT['tv_empty_title']).text
            log.info(no_result)
            # 搜索结果页-无结果重新搜索
            ele = self.new_find_element(By.ID, self.ELEMENT['tv_empty_sub_title'])
            print("-------", print(ele.size))

            # self.driver.tap()
            # time.sleep(5)

            log.info("搜索无结果，点击重新搜索")

            self.logout()
            account.release_account(acc_vip_name, "vip")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception