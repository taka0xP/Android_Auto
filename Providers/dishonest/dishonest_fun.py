#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/21
# @Author  : Soner
# @version : 1.0.0

from selenium.webdriver.common.by import By
from common.operation import Operation
from common.extend import Extend
from Providers.logger import Logger,error_format
import os

log = Logger("dishonest_phase_operation").getlog()
class Dishonest:
    def __init__(self, driver, element):
        self.driver = driver
        self.ELEMENT = element
        self.operation = Operation(self.driver)
        self.extend = Extend(self.driver)

    def into_dishonest_mid(self):
        search_input = self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_search_input"]
        )
        return search_input

    # 通过banner封装进入企业预核名方法
    def entrance(self):
        count = 0
        # 获取屏幕比例
        x = self.driver.get_window_size()["width"]
        y = self.driver.get_window_size()["height"]
        self.driver.swipe(0.8 * x, 0.52 * y, 0.2 * x, 0.52 * y, 300)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        banner_path = os.path.join(base_path, "Data/search_dishonest.png")
        while True:
            banner = self.operation.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/sdv_banner"
            )
            # 截取当前banner
            self.extend.get_screenshot_by_element(banner)
            # 进行图像比对
            result = self.extend.classify_hist_with_split(banner_path)
            # 判断图像对比结果和对比次数
            if count > 4:
                log.warning("查找banner超过4次上限！！！请检查！！！")
                break
            elif result > 0.7:  # 图像对比结果判断
                # 点击banner进入企业预核名页面
                self.operation.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/sdv_banner"
                ).click()
                break
            else:
                # 左滑切换下一张banner
                self.driver.swipe(0.8 * x, 0.52 * y, 0.2 * x, 0.52 * y, 300)
                count += 1

    def clean_search_history(self):
        """从「查老赖首页」开始，进入「搜索中间页」，删除「最近搜索记录」"""
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_search_input"]
        ).click()
        res = self.operation.isElementExist(
            By.ID, self.ELEMENT["dishonest_del_history"], outtime=3
        )
        # 如果「删除最近搜索按钮」存在：
        if res:
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_del_history"]
            ).click()
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_del_submit"]
            ).click()
        # 「删除最近搜索按钮」不存在，然后返回「查老赖」首页
        self.operation.new_find_element(
            By.ID, self.ELEMENT["dishonest_mid_cancel"]
        ).click()
        log.info("清除查老赖搜索历史")

    def get_hotword_element_in_mid(self, idx=1):
        return self.operation.new_find_elements(
            By.ID, self.ELEMENT["dishonest_hot_words"]
        )[idx]

    def click_hotword_in_mid(self, idx=1):
        hotword_element = self.get_hotword_element_in_mid(idx)
        text_value = hotword_element.text
        log.info("查看 {} 老赖信息".format(text_value))
        hotword_element.click()
        return text_value

    def broken_faith_enterprise(self):
        "进入 失信企业"
        enterprise = self.operation.new_find_element(
            By.XPATH, self.ELEMENT["broken_faith_enterprise_tab"]
        )
        return enterprise

    def search_city(self, province, city, pr_y1=0.7, pr_y2=0.5, ci_y1=0.7, ci_y2=0.3):
        "按区域筛选"
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_screen"].format(1)
        ).click()  # 点击 1.全部区域
        # 滑动省份
        pr_count = 5
        while True:
            if (
                    self.operation.isElementExist(
                        By.XPATH, self.ELEMENT["dishonest_city"].format(province), outtime=2
                    )
                    or pr_count <= 0
            ):
                break
            self.operation.swipeUp(0.1, pr_y1, pr_y2)  # 滑动省份
            pr_count -= 1
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_city"].format(province)
        ).click()
        # 滑动城市
        city_count = 5
        while True:
            if (
                    self.operation.isElementExist(
                        By.XPATH, self.ELEMENT["dishonest_city"].format(city), outtime=2
                    )
                    or city_count <= 0
            ):
                break
            self.operation.swipeUp(0.5, ci_y1, ci_y2)  # 滑动城市
            city_count -= 1
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_city"].format(city)
        ).click()

    def search_year(self, year, y1=0.8, y2=0.6):
        "按年龄筛选"
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_screen"].format(2)
        ).click()  # 点击 出生年月
        self.operation.swipeUp(0.1, y1, y2)  # 滑动年份
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_city"].format(year)
        ).click()
        year_count = 10
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_screen"].format(2)
        ).click()  # 点击 出生年月
        while True:
            if (
                    self.operation.isElementExist(
                        By.XPATH, self.ELEMENT["dishonest_screen"].format(2)
                    )
                    or year_count <= 0
            ):
                break
            self.operation.swipeUp(0.1, y1, y2)  # 滑动年份
            year_count -= 1
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_city"].format(year)
        ).click()

    def search_sex(self, sex):
        "按性别筛选"
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_screen"].format(3)
        ).click()  # 点击 性别
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_city"].format(sex)
        ).click()

    def back_all_regions(self, province="全部区域", city="全部区域", pr_y1=0.5, pr_y2=0.7, ci_y1=0.3, ci_y2=0.7):
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_screen"].format(1)
        ).click()
        # 滑动省份
        pr_count = 5
        while True:
            if (self.operation.isElementExist(By.XPATH, self.ELEMENT["dishonest_city"].format(province),
                                              outtime=2) or pr_count <= 0):
                break
            self.operation.swipeDown(0.1, pr_y1, pr_y2)  # 滑动省份
            pr_count -= 1
        self.operation.new_find_element(By.XPATH, self.ELEMENT["dishonest_city"].format(province)).click()
        # 滑动城市
        city_count = 5
        while True:
            if (self.operation.isElementExist(By.XPATH, self.ELEMENT["dishonest_city"].format(city),
                                              outtime=2) or city_count <= 0):
                break
            self.operation.swipeDown(0.5, ci_y1, ci_y2)  # 滑动城市
            city_count -= 1
        if city == '全部区域':
            self.operation.new_find_element(By.ID, self.ELEMENT["dishonest_city_low"]).click()
        else:
            self.operation.new_find_element(By.XPATH, self.ELEMENT["dishonest_city"].format(city)).click()
