# -*- coding: utf-8 -*-
# @Time    : 2019-11-19 09:59
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : company_name_pre_check.py
# @Software: PyCharm
import os
from common.MyTest import MyTest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
import random
from Providers.logger import Logger
from testcase.sunkai.sunkai_ele import elements

industries = ['网络科技', '电子', '教育科技', '资产', '融资租赁', '人力资源', '广告', '美容美发', '企业管理']
log = Logger('企业预核名1').getlog()


class CompanyNameCheck(MyTest, Operation):
    # 分类搜索预核名入口
    def entrance_in_all_search(self):
        self.new_find_element(By.XPATH, elements['all_style']).click()
        self.new_find_element(By.XPATH, elements['company_name_check_in_all']).click()

    # 通过banner封装进入企业预核名方法
    def entrance(self):
        count = 0
        # 获取屏幕比例
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.driver.swipe(0.8 * x, 0.52 * y, 0.2 * x, 0.52 * y, 300)
        base_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
        banner_path = os.path.join(base_path, 'Data/companyname_banner.png')
        while True:
            banner = self.new_find_element(By.ID, elements['banner'])
            # 截取当前banner
            self.extend.get_screenshot_by_element(banner)
            # 进行图像比对
            result = self.extend.classify_hist_with_split(banner_path)
            print('banner对比相似度：', result)
            # 判断图像对比结果和对比次数
            if count > 4:
                print('查找banner超过4次上限！！！请检查！！！')
                break
            elif result > 0.7:  # 图像对比结果判断
                # 点击banner进入企业预核名页面
                self.new_find_element(By.ID, elements['banner']).click()
                break
            else:
                # 左滑切换下一张banner
                self.driver.swipe(0.8 * x, 0.52 * y, 0.2 * x, 0.52 * y, 300)
                count += 1

    # 验证点击banner进入页面
    @getimage
    def test_01_entrance(self):
        log.info('验证点击banner进入页面')
        self.entrance()
        title = self.new_find_element(By.ID, elements['title']).text
        self.assertEqual(title, '企业名称检测')

    # 默认搜索词查询
    @getimage
    def test_02_default_search(self):
        log.info('默认搜索词查询')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['search_button']).click()
        default_result = self.isElementExist(By.XPATH, elements['default_result'])
        self.assertTrue(default_result)

    # 通过热门城市进行城市选择
    @getimage
    def test_03_select_city_by_hot(self):
        log.info('通过热门城市进行城市选择')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['city']).click()
        # 随机选择热门城市
        hot_city = elements['hot_city'] + str([random.randint(1, 12)]) + '/android.view.View[1]'
        city = self.new_find_element(By.XPATH, hot_city)
        city_name = city.text
        city.click()
        # 获取选择的城市名称
        choose_city = self.new_find_element(By.XPATH, elements['city']).text
        # 校验选择的和实际是否一致
        self.assertEqual(city_name, choose_city)

    # 通过搜索选择城市
    @getimage
    def test_04_select_city_by_search(self):
        log.info('通过搜索选择城市')
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements['city']).click()
        # 点击搜索框
        self.new_find_element(By.CLASS_NAME, elements['city_search']).click()
        # 输入城市
        self.new_find_element(By.XPATH, elements['city_search_input']).send_keys('张家口')
        # 选择搜索结果
        self.new_find_element(By.XPATH, elements['city_search_result']).click()
        city_name = self.new_find_element(By.XPATH, elements['city']).text
        # 校验搜索结果
        self.assertEqual(city_name, '张家口')

    # 敏感词输入
    @getimage
    def test_05_sensitive_words(self):
        log.info('敏感词输入')
        self.entrance_in_all_search()
        # 输入敏感词
        self.new_find_element(By.XPATH, elements['name_input']).send_keys('的的的的')
        self.new_find_element(By.XPATH, elements['search_button']).click()
        # 获取toast内容
        toast = self.new_find_element(By.XPATH, elements['sensitive_words_toast']).text
        # 校验敏感词
        self.assertEqual(toast, '企业名称不能包含敏感词')
