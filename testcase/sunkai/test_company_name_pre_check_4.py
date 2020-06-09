# -*- coding: utf-8 -*-
# @Time    : 2020-02-21 15:17
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : test_company_name_pre_check_4.py
# @Software: PyCharm
from common.MyTest import MyTest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from time import sleep
from Providers.logger import Logger
from testcase.sunkai.sunkai_ele import elements


industries = ["网络科技", "电子", "教育科技", "资产", "融资租赁", "人力资源", "广告", "美容美发", "企业管理"]
log = Logger("企业预核名4").getlog()


class CompanyNameCheck(MyTest, Operation):
    # 分类搜索预核名入口
    def entrance_in_all_search(self):
        self.new_find_element(By.XPATH, elements["all_style"]).click()
        self.new_find_element(By.XPATH, elements["company_name_check_in_all"]).click()

    # 在城市查看全部
    @getimage
    def test_14_show_all_result_in_city(self):
        log.info("在城市查看全部")
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements["name_input"]).send_keys("如意")
        self.new_find_element(By.XPATH, elements["search_button"]).click()
        # 获取元素坐标
        location = self.new_find_element(By.XPATH, elements["in_city"]).location
        self.driver.swipe(location["x"], location["y"], location["x"], 520, 1000)
        self.new_find_element(By.XPATH, elements["in_city"]).click()
        self.new_find_element(By.XPATH, elements["name_same_all_result"]).click()
        same_items = len(
            self.new_find_elements(By.CLASS_NAME, elements["all_results_all_items"])
        )
        self.assertGreaterEqual(same_items, 10 + 3, msg="在城市字号相同查看全部失败")
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, elements["name_like_all_result"]).click()
        like_items = len(
            self.new_find_elements(By.CLASS_NAME, elements["all_results_all_items"])
        )
        self.assertGreaterEqual(like_items, 10 + 3, msg="在城市字号相似查看全部失败")
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, elements["name_read_same_all_result"]).click()
        read_same_items = len(
            self.new_find_elements(By.CLASS_NAME, elements["all_results_all_items"])
        )
        self.assertGreaterEqual(read_same_items, 10 + 3, msg="在城市字号读音相同查看全部失败")
        self.driver.keyevent(4)
        self.new_find_element(
            By.XPATH, elements["trademark_register_all_result"]
        ).click()
        trademark_items = len(
            self.new_find_elements(By.CLASS_NAME, elements["all_results_all_items"])
        )
        self.assertGreaterEqual(trademark_items, 10 + 3, msg="在城市注册了商标的查看全部失败")

    # 想注册公司吗banner跳转
    @getimage
    def test_15_want_register_company_banner_goto(self):
        log.info("想注册公司吗banner跳转")
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements["search_button"]).click()
        self.new_find_element(
            By.XPATH, elements["want_register_company_banner"]
        ).click()
        import time
        time.sleep(3)
        page_title = self.new_find_element(
            By.ID, elements["title"]
        ).text
        self.assertEqual(page_title, "您是否要注册公司？")

    # 结果页底部banner跳转
    @getimage
    def test_16_page_bottom_banner_goto(self):
        log.info("结果页底部banner跳转")
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements["search_button"]).click()
        for i in range(3):
            self.driver.swipe(100, 1000, 100, 100, 500)
        self.new_find_element(
            By.XPATH, elements["page_bottom_banner_company_register"]
        ).click()
        sleep(1)
        company_register_title = self.new_find_element(
            By.ID, elements["tyc-service_buy_title"]
        ).text
        self.assertEqual(company_register_title, "公司注册")
        self.driver.keyevent(4)
        self.new_find_element(
            By.XPATH, elements["page_bottom_banner_bank_open"]
        ).click()
        sleep(1)
        bank_open_title = self.new_find_element(
            By.ID, elements["tyc-service_buy_title"]
        ).text
        self.assertEqual(bank_open_title, "银行开户")

    # 在全国中字号相似和读音相同的企业count数和实际展示数量校验
    @getimage
    def test_17_count_in_country_result(self):
        log.info("在全国中字号相似和读音相同的企业count数和实际展示数量校验")
        self.entrance_in_all_search()
        self.new_find_element(By.XPATH, elements["name_input"]).send_keys("吃哈")
        self.new_find_element(By.XPATH, elements["search_button"]).click()
        # 获取元素坐标
        location = self.new_find_element(By.XPATH, elements["in_china"]).location
        self.driver.swipe(location["x"], location["y"], location["x"], 520, 1000)
        # 字号相似的企业count数
        like_out_count = int(
            self.new_find_element(By.XPATH, elements["country_name_like_count"]).text
        )
        # 字号读音相似的企业count数
        read_like_out_count = int(
            self.new_find_element(By.XPATH, elements["country_read_same_count"]).text
        )
        self.new_find_element(By.XPATH, elements["name_like_all_result"]).click()
        name_like_show_number = len(
            self.new_find_elements(By.XPATH, elements["country_name_Like_items"])
        )
        self.assertEqual(
            like_out_count, name_like_show_number - 1, msg="字号相似企业count与实际不符合"
        )
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, elements["name_read_same_all_result"]).click()
        read_same_show_number = len(
            self.new_find_elements(By.XPATH, elements["country_read_same_items"])
        )
        self.assertEqual(
            read_like_out_count, read_same_show_number - 1, msg="字号读音相似count与实际不符"
        )
