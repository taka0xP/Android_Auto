# -*- coding: utf-8 -*-
# @Time    : 2020-05-21 10:40
# @Author  : XU
# @File    : relation_opera.py
# @Software: PyCharm
from common.operation import Operation
from selenium.webdriver.common.by import By
from Providers.logger import Logger, error_format
from Providers.sift.sift_opera import SiftOperation
import time


class RelationOperation:
    def __init__(self, driver, element):
        self.driver = driver
        self.opera = Operation(driver)
        self.ELEMENT = element

    def home_page(self):
        """回到首页"""
        while not self.opera.isElementExist(By.ID, self.ELEMENT["search_relation"]):
            self.driver.keyevent(4)

    def hot_relation(self):
        """进入热搜关系"""
        self.opera.new_find_element(By.ID, self.ELEMENT["search_relation"]).click()
        relation_tab_tag = self.opera.new_find_element(By.ID, self.ELEMENT["search_box"]).text
        self.opera.new_find_element(By.XPATH, self.ELEMENT["hot_relation"]).click()
        self.opera.new_find_element(By.ID, self.ELEMENT["discover_btn"]).click()
        hot_relation_point_tag = self.opera.isElementExist(By.XPATH, self.ELEMENT["relation_point"])
        self.opera.new_find_element(By.ID, self.ELEMENT["app_title_logo"]).click()
        home_page_tag = self.opera.isElementExist(By.ID, self.ELEMENT["search_relation"])
        return relation_tab_tag, hot_relation_point_tag, home_page_tag

    def search_relation_point(self, index):
        """
        查关系未登陆、非vip、vip三种状态断言
        :param index: 1：未登录；2：非vip；其他：vip
        :return:
        """
        self.opera.new_find_element(By.ID, self.ELEMENT["search_relation"]).click()
        self.opera.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.opera.new_find_element(By.ID, self.ELEMENT["from_input_textview"]).click()
        self.opera.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).send_keys("北京金堤科技有限公司")
        self.opera.new_find_element(By.XPATH, self.ELEMENT["from_target_item_1"]).click()
        self.opera.new_find_element(By.ID, self.ELEMENT["to_input_textview"]).click()
        self.opera.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).send_keys("盐城金堤科技有限公司")
        self.opera.new_find_element(By.XPATH, self.ELEMENT["from_target_item_1"]).click()
        self.opera.new_find_element(By.ID, self.ELEMENT["discover_btn"]).click()
        if index == 1:
            result = self.opera.new_find_element(By.XPATH, self.ELEMENT['passwd_login']).text
            self.home_page()
        elif index == 2:
            time.sleep(3)
            self.opera.new_find_element(By.ID, "com.tianyancha.skyeye:id/explore_must_vip_open_btn").click()
            result = self.opera.new_find_element(By.ID, self.ELEMENT['tv_top_title']).text
            self.home_page()
        else:
            result = self.opera.new_find_element(By.XPATH, self.ELEMENT['relation_point']).text
        return result

    def check_relation(self):
        """校验查关系结果"""
        self.opera.new_find_element(By.ID, self.ELEMENT["to_input_textview"]).click()
        self.opera.new_find_element(By.XPATH, self.ELEMENT["to_target_human"]).click()
        human_tag = self.opera.new_find_element(By.ID, self.ELEMENT["to_input_textview"]).text
        self.opera.new_find_element(By.ID, self.ELEMENT["discover_btn"]).click()
        relation_point_tag = self.opera.new_find_element(By.XPATH, self.ELEMENT["relation_point"]).text
        return human_tag, relation_point_tag

    def exam_relation(self):
        """示例关系"""
        self.opera.new_find_element(By.ID, self.ELEMENT["search_relation"]).click()
        self.opera.new_find_element(By.XPATH, self.ELEMENT["hot_relation"]).click()

    def all_screen(self):
        """关系图全屏"""
        self.opera.new_find_element(By.ID, self.ELEMENT["full_screen"]).click()
        discover_btn_tag = self.opera.isElementExist(By.ID, self.ELEMENT["discover_btn"])
        exit_fullscreen_tag = self.opera.isElementExist(By.ID, self.ELEMENT["exit_fullscreen"])
        relation_point_tag = self.opera.isElementExist(By.XPATH, self.ELEMENT["relation_point"])
        return discover_btn_tag, exit_fullscreen_tag, relation_point_tag

    def exit_screen(self):
        """退出全屏"""
        self.opera.new_find_element(By.ID, self.ELEMENT["exit_fullscreen"]).click()
        exit_fullscreen_tag = self.opera.isElementExist(By.ID, self.ELEMENT["exit_fullscreen"])
        discover_btn_tag = self.opera.isElementExist(By.ID, self.ELEMENT["discover_btn"])
        return exit_fullscreen_tag, discover_btn_tag

    def confirm(self):
        """确认清空关系图"""
        self.opera.new_find_element(By.ID, self.ELEMENT["clear_all"]).click()
        delte_tag = self.opera.isElementExist(By.ID, self.ELEMENT["delte_cancel"])
        self.opera.new_find_element(By.ID, self.ELEMENT["delte_cancel"]).click()
        confirm_tag = self.opera.isElementExist(By.ID, self.ELEMENT["delete_confirm"])
        point_tag = self.opera.isElementExist(By.XPATH, self.ELEMENT["relation_point"])
        self.opera.new_find_element(By.ID, self.ELEMENT["clear_all"]).click()
        self.opera.new_find_element(By.ID, self.ELEMENT["delete_confirm"]).click()
        cancel_tag = self.opera.isElementExist(By.ID, self.ELEMENT["delte_cancel"])
        empty_tag = self.opera.isElementExist(By.ID, self.ELEMENT["relation_empty"])
        return delte_tag, confirm_tag, point_tag, cancel_tag, empty_tag
