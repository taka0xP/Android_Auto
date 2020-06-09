# -*- coding: utf-8 -*-
# @Time    : 2020-02-21 15:17
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : test_company_name_pre_check_2.py
# @Software: PyCharm
from common.MyTest import MyTest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
import random
from time import sleep
from Providers.logger import Logger
from testcase.sunkai.sunkai_ele import elements


industries = ['网络科技', '电子', '教育科技', '资产', '融资租赁', '人力资源', '广告', '美容美发', '企业管理']
log = Logger('企业预核名2').getlog()


class CompanyNameCheck(MyTest, Operation):
    # 分类搜索预核名入口
    def entrance_in_all_search(self):
        self.new_find_element(By.XPATH, elements['all_style']).click()
        self.new_find_element(By.XPATH, elements['company_name_check_in_all']).click()

    # 字号输入字母
    @getimage
    def test_06_input_english_number(self):
        log.info('字号输入字母')
        self.entrance_in_all_search()
        # 输入字母
        self.new_find_element(By.XPATH, elements['name_input']).send_keys('sunkai')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        english_toast = self.isElementExist(By.XPATH, elements['name_no_chinese_toast'])
        self.assertTrue(english_toast)
        sleep(0.5)
        # 清空字号输入
        if self.isElementExist(By.XPATH, elements['name_input_one_key_clear']):
            self.new_find_element(By.XPATH, elements['name_input_one_key_clear']).click()
        else:
            self.new_find_element(By.XPATH, elements['name_input']).clear()
        # 输入数字
        self.new_find_element(By.XPATH, elements['name_input']).send_keys('123456')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        number_toast = self.isElementExist(By.XPATH, elements['name_no_chinese_toast'])
        self.assertTrue(number_toast)
        sleep(0.5)
        # 清空字号输入
        if self.isElementExist(By.XPATH, elements['name_input_one_key_clear']):
            self.new_find_element(By.XPATH, elements['name_input_one_key_clear']).click()
        else:
            self.new_find_element(By.XPATH, elements['name_input']).clear()
        # 输入特殊字符
        self.new_find_element(By.XPATH, elements['name_input']).send_keys(',.，。？?、/;；*#￥$%()')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        special_toast = self.isElementExist(By.XPATH, elements['name_no_chinese_toast'])
        self.assertTrue(special_toast)

    # 行业选择
    @getimage
    def test_07_industry_select(self):
        log.info('行业选择')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['industry_select']).click()
        page_goto = self.isElementExist(By.XPATH, elements['assert_industry_page'])
        # 校验是否进入到行业选择页
        self.assertTrue(page_goto)
        choose_industry = random.choice(industries)
        xpath = elements['every_industry'].format(choose_industry)
        self.new_find_element(By.XPATH, xpath).click()
        show_industry = self.new_find_element(By.XPATH, elements['industry_select']).text
        self.assertEqual(choose_industry, show_industry)

    # 公司类型选择
    @getimage
    def test_08_company_style_select(self):
        log.info('公司类型选择')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['company_friend_style']).click()
        self.new_find_element(By.XPATH, elements['search_button']).click()
        # 通过判断展示的公司名称确认公司类型是否选择正确
        result = self.isElementExist(By.XPATH, elements['friend_company_result'])
        self.assertTrue(result)

    # 字号中包含特殊词语展示友情提示
    @getimage
    def test_09_special_company_name(self):
        log.info('字号中包含特殊词语展示友情提示')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['name_input']).send_keys('国际')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        friendship_tips = self.isElementExist(By.XPATH, elements['friendship_tips'])
        self.assertTrue(friendship_tips)
