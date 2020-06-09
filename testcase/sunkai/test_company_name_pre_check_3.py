# -*- coding: utf-8 -*-
# @Time    : 2020-02-21 15:17
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : test_company_name_pre_check_3.py
# @Software: PyCharm
from common.MyTest import MyTest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
import random
from Providers.logger import Logger
from testcase.sunkai.sunkai_ele import elements


industries = ['网络科技', '电子', '教育科技', '资产', '融资租赁', '人力资源', '广告', '美容美发', '企业管理']
log = Logger('企业预核名3').getlog()


class CompanyNameCheck(MyTest, Operation):
    # 分类搜索预核名入口
    def entrance_in_all_search(self):
        self.new_find_element(By.XPATH, elements['all_style']).click()
        self.new_find_element(By.XPATH, elements['company_name_check_in_all']).click()

    # 搜索结果-全国和城市全部由四个模块组成
    @getimage
    def test_10_result_check(self):
        log.info('搜索结果-全国和城市全部由四个模块组成')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['name_input']).send_keys('字节')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        # 获取元素坐标
        location = self.new_find_element(By.XPATH, elements['in_china']).location
        self.driver.swipe(location['x'], location['y'], location['x'], 520, 1000)
        # 在全国组成部分
        name_same_china = self.isElementExist(By.XPATH, elements['name_same'])
        name_like_china = self.isElementExist(By.XPATH, elements['name_like'])
        name_read_same_china = self.isElementExist(By.XPATH, elements['name_read_same'])
        trademark_register_china = self.isElementExist(By.XPATH, elements['trademark_register'])
        self.assertTrue(name_same_china, msg='在全国缺少字号相同模块')
        self.assertTrue(name_like_china, msg='在全国缺少字号相似模块')
        self.assertTrue(name_read_same_china, msg='在全国缺少字号读音相同模块')
        self.assertTrue(trademark_register_china, msg='在全国缺少注册了商标模块')
        self.new_find_element(By.XPATH, elements['in_city']).click()
        # 在城市组成部分
        name_same_city = self.isElementExist(By.XPATH, elements['name_same'])
        name_like_city = self.isElementExist(By.XPATH, elements['name_like'])
        name_read_same_city = self.isElementExist(By.XPATH, elements['name_read_same'])
        trademark_register_city = self.isElementExist(By.XPATH, elements['trademark_register'])
        self.assertTrue(name_same_city, msg='在城市缺少字号相同模块')
        self.assertTrue(name_like_city, msg='在城市缺少字号相似模块')
        self.assertTrue(name_read_same_city, msg='在城市缺少字号读音相同模块')
        self.assertTrue(trademark_register_city, msg='在城市缺少注册了商标模块')

    # 点击搜索结果公司跳转到详情页
    @getimage
    def test_11_click_company(self):
        log.info('点击搜索结果公司跳转到详情页')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['city']).click()
        # 随机选择热门城市
        hot_city = elements['hot_city'] + str([random.randint(1, 12)]) + '/android.view.View[1]'
        self.new_find_element(By.XPATH, hot_city).click()
        self.new_find_element(By.XPATH, elements['name_input']).send_keys('阿里')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        self.new_find_element(By.XPATH, elements['company_item']).click()
        i_know = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn')
        if i_know:
            i_know.click()
        company_detail_mark = self.new_find_element(By.ID, elements['company_detail_mark']).text
        self.assertTrue(company_detail_mark, '官方信息')

    # 搜索无结果
    @getimage
    def test_12_no_search_result(self):
        log.info('搜索无结果')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['name_input']).send_keys('九十多斤卡斯柯')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        no_result = self.new_find_element(By.XPATH, elements['no_result'])
        self.assertTrue(no_result)

    # 在全国查看全部
    @getimage
    def test_13_show_all_result_in_china(self):
        log.info('在全国查看全部')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['name_input']).send_keys('随便')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        # 获取元素坐标
        location = self.new_find_element(By.XPATH, elements['in_china']).location
        self.driver.swipe(location['x'], location['y'], location['x'], 520, 1000)
        self.new_find_element(By.XPATH, elements['name_same_all_result']).click()
        same_items = len(self.new_find_elements(By.CLASS_NAME, elements['all_results_all_items']))
        self.assertGreaterEqual(same_items, 10 + 3, msg='在全国字号相同查看全部失败')
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, elements['name_like_all_result']).click()
        like_items = len(self.new_find_elements(By.CLASS_NAME, elements['all_results_all_items']))
        self.assertGreaterEqual(like_items, 10 + 3, msg='在全国字号相似查看全部失败')
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, elements['name_read_same_all_result']).click()
        read_same_items = len(self.new_find_elements(By.CLASS_NAME, elements['all_results_all_items']))
        self.assertGreaterEqual(read_same_items, 10 + 3, msg='在全国字号读音相同查看全部失败')
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, elements['trademark_register_all_result']).click()
        trademark_items = len(self.new_find_elements(By.CLASS_NAME, elements['all_results_all_items']))
        self.assertGreaterEqual(trademark_items, 10 + 3, msg='在全国注册了商标的查看全部失败')
