#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/24
# @Author  : Soner
# @version : 1.0.0

import unittest
import time

from selenium.webdriver.common.by import By
from random import randint
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from common.operation import Operation
from common.operation import getimage
from Providers.logger import Logger, error_format
from Providers.company.company import CompanyFunc
from Providers.account.account import Account
from Providers.random_str.random_str import RandomStr

log = Logger("公司底部TAB_更多_投诉").getlog()


class CompanyBottomTabMoreComplaint(MyTest):
    """
    公司底部TAB_更多_投诉
    """
    a = Read_Ex()
    ELEMENT = a.read_excel("company_bottom_tab")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.operation = Operation(cls.driver)
        cls.company = CompanyFunc(cls.driver, cls.ELEMENT)
        cls.account = Account()
        cls.company_name = '四川同辉实业有限公司'
        cls.rand_str = RandomStr()

    def tearDown(self):
        back_count = 0
        while True:
            back_count += 1
            if back_count > 10:
                break
            else:
                try:
                    self.driver.find_element_by_id('com.tianyancha.skyeye:id/tab1').click()
                    break
                except:
                    self.driver.keyevent(4)
                    if self.operation.isElementExist(By.ID, self.ELEMENT['email_neg'], outtime=1):
                        # 点击 「取消编辑」
                        self.operation.new_find_element(By.ID, self.ELEMENT['email_neg']).click()

    @getimage
    def test_gfxx_tab_ts_0001(self):
        "随机一个人员类型不填写投诉信息，点击「提交」，toast提示“请输入投诉内容”"
        log.info(self.test_gfxx_tab_ts_0001.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 投诉
            self.company.click_tab(more_local)
            # 随机获取一个投诉身份
            complaint_count = len(self.operation.new_find_elements(By.XPATH, self.ELEMENT['complaint_id']))
            complaint_num = randint(1, complaint_count)
            complaint = self.operation.new_find_element(By.XPATH,
                                                        self.ELEMENT['complaint_id'] + "[{}]".format(complaint_num))
            log.info("本次投诉人员类型：{}".format(complaint.text))
            complaint.click()
            self.operation.new_find_element(By.ID, self.ELEMENT['complaint_btn']).click()
            toast = self.operation.get_toast()
            text = "请输入投诉内容"
            self.assertEqual(text, toast, "预期toast：{}，待校验toast：{}".format(text, toast))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_ts_0002(self):
        "随机一个人员类型填写超过字数限制的内容，校验字数"
        log.info(self.test_gfxx_tab_ts_0002.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 投诉
            self.company.click_tab(more_local)
            # 随机获取一个投诉身份
            complaint_count = len(self.operation.new_find_elements(By.XPATH, self.ELEMENT['complaint_id']))
            complaint_num = randint(1, complaint_count)
            complaint = self.operation.new_find_element(By.XPATH,
                                                        self.ELEMENT['complaint_id'] + "[{}]".format(complaint_num))
            log.info("本次投诉人员类型：{}".format(complaint.text))
            complaint.click()
            # 输入内容
            self.operation.adb_send_input(By.ID, self.ELEMENT['content_et'], self.rand_str.zh_cn(510), self.device)
            # 校验 字数
            content_num = self.operation.new_find_element(By.ID, self.ELEMENT['content_length']).text
            text = "500/500"
            self.assertEqual(text, content_num, "预期字数文案：{}，待校验字数文案：{}".format(text, content_num))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_ts_0003(self):
        "随机一个人员类型填写投诉信息为空格，点击「提交」，toast提示“请输入投诉内容”"
        log.info(self.test_gfxx_tab_ts_0003.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 投诉
            self.company.click_tab(more_local)
            # 随机获取一个投诉身份
            complaint_count = len(self.operation.new_find_elements(By.XPATH, self.ELEMENT['complaint_id']))
            complaint_num = randint(1, complaint_count)
            complaint = self.operation.new_find_element(By.XPATH,
                                                        self.ELEMENT['complaint_id'] + "[{}]".format(complaint_num))
            log.info("本次投诉人员类型：{}".format(complaint.text))
            complaint.click()
            # 输入内容
            self.operation.adb_send_input(By.ID, self.ELEMENT['content_et'], "      ", self.device)
            # 点击 提交
            self.operation.new_find_element(By.ID, self.ELEMENT['complaint_btn']).click()
            toast = self.operation.get_toast()
            text = "请输入投诉内容"
            self.assertEqual(text, toast, "预期toast：{}，待校验toast：{}".format(text, toast))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_ts_0004(self):
        "随机一个人员类型，上传图片，不填写投诉内容，toast提示“请输入投诉内容”"
        log.info(self.test_gfxx_tab_ts_0004.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 投诉
            self.company.click_tab(more_local)
            # 随机获取一个投诉身份
            complaint_count = len(self.operation.new_find_elements(By.XPATH, self.ELEMENT['complaint_id']))
            complaint_num = randint(1, complaint_count)
            complaint = self.operation.new_find_element(By.XPATH,
                                                        self.ELEMENT['complaint_id'] + "[{}]".format(complaint_num))
            log.info("本次投诉人员类型：{}".format(complaint.text))
            complaint.click()
            # 上传图片
            self.operation.new_find_element(By.ID, self.ELEMENT['up_pic']).click()
            self.company.up_pic(9)
            # 点击 提交
            time.sleep(2)
            self.operation.swipeUp()
            self.operation.new_find_element(By.ID, self.ELEMENT['complaint_btn']).click()
            toast = self.operation.get_toast()
            text = "请输入投诉内容"
            self.assertEqual(text, toast, "预期toast：{}，待校验toast：{}".format(text, toast))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_ts_0005(self):
        "随机一个人员类型，因测试机随机获取，只校验上传图片功能正常"
        log.info(self.test_gfxx_tab_ts_0005.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 投诉
            self.company.click_tab(more_local)
            # 随机获取一个投诉身份
            complaint_count = len(self.operation.new_find_elements(By.XPATH, self.ELEMENT['complaint_id']))
            complaint_num = randint(1, complaint_count)
            complaint = self.operation.new_find_element(By.XPATH,
                                                        self.ELEMENT['complaint_id'] + "[{}]".format(complaint_num))
            log.info("本次投诉人员类型：{}".format(complaint.text))
            complaint.click()
            # 输入内容
            self.operation.adb_send_input(By.ID, self.ELEMENT['content_et'], self.rand_str.zh_cn(15), self.device)
            # 上传图片
            self.operation.new_find_element(By.ID, self.ELEMENT['up_pic']).click()
            self.company.up_pic(9)
            # 判断 提交 按钮是否存在，不存在则下拉一次
            if not self.operation.isElementExist(By.ID, self.ELEMENT['complaint_btn'], outtime=10):
                log.info("没有找到上传按钮，下拉页面寻找")
                self.operation.swipeUp()
            self.operation.new_find_element(By.ID, self.ELEMENT['complaint_btn']).click()
            complaint_title = self.operation.new_find_element(By.ID, self.ELEMENT['complaint_title']).text
            text = '你的投诉内容已提交成功'
            self.assertEqual(text, complaint_title, "预期title：{}，待校验title：{}".format(text, complaint_title))
            self.operation.new_find_element(By.ID, self.ELEMENT['complaint_close']).click()
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_ts_0006(self):
        "随机一个人员类型，提交成功，点击提示框图片，跳转天眼服务"
        log.info(self.test_gfxx_tab_ts_0006.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 投诉
            self.company.click_tab(more_local)
            # 随机获取一个投诉身份
            complaint_count = len(self.operation.new_find_elements(By.XPATH, self.ELEMENT['complaint_id']))
            complaint_num = randint(1, complaint_count)
            complaint = self.operation.new_find_element(By.XPATH,
                                                        self.ELEMENT['complaint_id'] + "[{}]".format(complaint_num))
            log.info("本次投诉人员类型：{}".format(complaint.text))
            complaint.click()
            # 输入内容
            self.operation.adb_send_input(By.ID, self.ELEMENT['content_et'], self.rand_str.zh_cn(15), self.device)
            # 点击 提交
            self.operation.new_find_element(By.ID, self.ELEMENT['complaint_btn']).click()
            self.operation.new_find_element(By.ID, self.ELEMENT['jump_intro']).click()
            new_title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            text = '电话咨询律师'
            self.assertEqual(text, new_title, "预期title：{}，待校验title：{}".format(text, new_title))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_ts_0007(self):
        "随机一个人员类型，点击「取消编辑」，放弃编辑内容"
        log.info(self.test_gfxx_tab_ts_0007.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 投诉
            self.company.click_tab(more_local)
            title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            # 随机获取一个投诉身份
            complaint_count = len(self.operation.new_find_elements(By.XPATH, self.ELEMENT['complaint_id']))
            complaint_num = randint(1, complaint_count)
            complaint = self.operation.new_find_element(By.XPATH,
                                                        self.ELEMENT['complaint_id'] + "[{}]".format(complaint_num))
            log.info("本次投诉人员类型：{}".format(complaint.text))
            complaint.click()
            # 输入内容
            self.operation.adb_send_input(By.ID, self.ELEMENT['content_et'], self.rand_str.zh_cn(15), self.device)
            # 点击 回退键
            self.driver.keyevent(4)
            # 点击 「取消编辑」
            self.operation.new_find_element(By.ID, self.ELEMENT['email_neg']).click()
            # 新页面的title
            new_title = self.operation.new_find_element(By.ID, self.ELEMENT['detail_title']).text
            log.info('新页面title：{}'.format(new_title))
            self.assertNotEqual(title, new_title, "投诉页title文案：{}，新页面title文案：{}".format(title, new_title))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_gfxx_tab_ts_0008(self):
        "随机一个人员类型，点击「继续编辑」，停留本页"
        log.info(self.test_gfxx_tab_ts_0008.__doc__)
        try:
            # 搜索公司
            self.company.search_company(self.company_name, self.device)
            # 是否有问大家
            self.company.ask_banner()
            # 点击 更多
            more = self.operation.new_find_element(By.ID, self.ELEMENT['click_more'])
            more_local = more.location
            more.click()
            # 鼠标定位 投诉
            self.company.click_tab(more_local)
            title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            # 随机获取一个投诉身份
            complaint_count = len(self.operation.new_find_elements(By.XPATH, self.ELEMENT['complaint_id']))
            complaint_num = randint(1, complaint_count)
            complaint = self.operation.new_find_element(By.XPATH,
                                                        self.ELEMENT['complaint_id'] + "[{}]".format(complaint_num))
            log.info("本次投诉人员类型：{}".format(complaint.text))
            complaint.click()
            # 输入内容
            self.operation.adb_send_input(By.ID, self.ELEMENT['content_et'], self.rand_str.zh_cn(15), self.device)
            # 点击 回退键
            self.driver.keyevent(4)
            # 点击 「继续编辑」
            self.operation.new_find_element(By.ID, self.ELEMENT['email_neg_pos']).click()
            # 页面的title
            new_title = self.operation.new_find_element(By.ID, self.ELEMENT['order_title']).text
            self.assertEqual(title, new_title, "预期title文案：{}，实际title文案：{}".format(title, new_title))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e


if __name__ == '__main__':
    unittest.main()
