# -*- coding: utf-8 -*-
# @Time    : 2019-12-25 13:47
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : skyeye_server.py
# @Software: PyCharm
from common.MyTest import MyTest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.ReadData import DB
import time

db = DB()
elements = db.get_element("elements_v11.8.0", "8")
print(elements)


class TestSkyeyeServer(MyTest, Operation):
    def get_page_title_text(self):
        """
        获取页面title
        :return: 存在返回title文本不存在返回None
        """
        title = self.new_find_element(By.ID, elements["service_detail_page_title"])
        if title:
            return title.text
        else:
            return None

    def index_page_rollback(self):
        """恢复首页到初始状态"""
        for i in range(3):
            self.driver.swipe(400, 500, 400, 1200, 1000)

    def test_01_create_company_need_six_step(self):
        """首页天眼服务开公司仅需6步流程"""
        ele = self.new_find_element(By.XPATH, elements["create_company_need_six"])
        ele_text = ele.text
        ele.click()
        title = self.get_page_title_text()
        self.assertEqual(ele_text, title)

    def test_02_create_company_all(self):
        """首页天眼服务开办公司全部入口"""
        self.new_find_element(By.XPATH, elements["create_company_all"]).click()
        title = self.get_page_title_text()
        selected_item = self.new_find_element(
            By.XPATH, elements["all_server_page_selected_item"]
        ).text
        self.assertEqual(title, "天眼服务")
        self.assertEqual(selected_item, "工商注册")

    def test_03_index_create_company_slide_items(self):
        """首页天眼服务开办公司滑动区域item"""
        screen_width = self.driver.get_window_size()["width"]
        slide_location = self.new_find_element(
            By.XPATH, elements["create_company_slide"]
        ).location["y"]
        all_item = [
            "公司注册",
            "公司地址注册",
            "银行开户",
            "代理记账",
            "税务报到",
            "税控代办",
            "股权变更",
            "注册地址变更",
            "法人",
        ]
        for item in all_item:
            xpath = elements["create_company_item"].format(item)
            print(xpath)
            while True:
                one = self.new_find_element(By.XPATH, xpath)
                if one:
                    one.click()
                    title = self.get_page_title_text()
                    self.assertIn(item, title, msg="首页天眼服务滑动区域" + item + "跳转错误")
                    self.driver.keyevent(4)
                    break
                else:
                    self.driver.swipe(
                        0.5 * screen_width,
                        slide_location + 100,
                        0.2 * screen_width,
                        slide_location + 100,
                        800,
                    )

    def test_04_trade_mark_so_easy(self):
        """首页天眼服务注册商标竟然这么简单"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 1200, 500)
        ele = self.new_find_element(By.XPATH, elements["trade_mark_so_easy"])
        ele_text = ele.text
        ele.click()
        title = self.get_page_title_text()
        self.assertEqual(ele_text, title)

    def test_05_trade_mark_all(self):
        """首页天眼服务商标服务全部入口"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 1200, 500)
        self.new_find_element(By.XPATH, elements["trade_mark_all"]).click()
        title = self.get_page_title_text()
        selected_item = self.new_find_element(
            By.XPATH, elements["all_server_page_selected_item"]
        ).text
        self.assertEqual(title, "天眼服务")
        self.assertEqual(selected_item, "商标服务")

    def test_06_trade_mark_items_slide(self):
        """首页商标服务滑动区域item"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 1200, 500)
        screen_width = self.driver.get_window_size()["width"]
        slide_location = self.new_find_element(
            By.XPATH, elements["trade_mark_slide"]
        ).location["y"]
        all_item = [
            "自助商标注册",
            "顾问商标注册",
            "担保商标注册",
            "商标续展",
            "商标驳回复审",
            "商标异议申请",
            "商标异议答辩",
            "商标变更",
            "商标撤三申请",
            "商标撤三答辩",
            "无效宣告申请",
            "无效宣告答辩",
            "商标宽展",
            "商标许可备案",
            "商标转让",
        ]
        for item in all_item:
            xpath = elements["trade_mark_item"].format(item)
            print(xpath)
            while True:
                one = self.new_find_element(By.XPATH, xpath)
                if one:
                    one.click()
                    title = self.get_page_title_text()
                    self.assertIn(item, title, msg="首页天眼服务滑动区域" + item + "跳转错误")
                    self.driver.keyevent(4)
                    break
                else:
                    self.driver.swipe(
                        0.5 * screen_width,
                        slide_location + 100,
                        0.2 * screen_width,
                        slide_location + 100,
                        800,
                    )

    def test_07_copyright_so_much_good(self):
        """首页版权服务申请版权居然这么多好处"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 900, 500)
        ele = self.new_find_element(By.XPATH, elements["copyright_so_much_good"])
        ele_text = ele.text
        ele.click()
        title = self.get_page_title_text()
        self.assertEqual(ele_text, title)

    def test_08_copyright_all(self):
        """首页版权服务全部入口"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 900, 500)
        self.new_find_element(By.XPATH, elements["copyright_all"]).click()
        title = self.get_page_title_text()
        selected_item = self.new_find_element(
            By.XPATH, elements["all_server_page_selected_item"]
        ).text
        self.assertEqual(title, "天眼服务")
        self.assertEqual(selected_item, "版权服务")

    def test_09_copyright_item_slide(self):
        """首页版权服务滑动item"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 900, 500)
        screen_width = self.driver.get_window_size()["width"]
        slide_location = self.new_find_element(
            By.XPATH, elements["copy_right_slide"]
        ).location["y"]
        all_item = ["软件著作权登记", "美术作品版权登记", "文字作品版权"]
        for item in all_item:
            xpath = elements["copy_right_slide_item"].format(item)
            print(xpath)
            while True:
                one = self.new_find_element(By.XPATH, xpath)
                if one:
                    one.click()
                    title = self.get_page_title_text()
                    self.assertIn(item, title, msg="首页天眼服务滑动区域" + item + "跳转错误")
                    self.driver.keyevent(4)
                    break
                else:
                    self.driver.swipe(
                        0.5 * screen_width,
                        slide_location + 100,
                        0.2 * screen_width,
                        slide_location + 100,
                        800,
                    )

    def test_10_law_service_see_trouble(self):
        """首页法律服务创业遇到哪些法律问题"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 800, 500)
        ele = self.new_find_element(By.XPATH, elements["law_service_see_trouble"])
        ele_text = ele.text
        ele.click()
        title = self.get_page_title_text()
        self.assertEqual(ele_text, title)

    def test_11_law_service_all(self):
        """首页法律服务全部入口"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 800, 500)
        self.new_find_element(By.XPATH, elements["law_service_all"]).click()
        title = self.get_page_title_text()
        selected_item = self.new_find_element(
            By.XPATH, elements["all_server_page_selected_item"]
        ).text
        self.assertEqual(title, "天眼服务")
        self.assertEqual(selected_item, "法律服务")

    def test_12_law_service_items_slide(self):
        """首页法律服务滑动item"""
        self.index_page_rollback()
        self.driver.swipe(450, 1600, 450, 600, 500)
        screen_width = self.driver.get_window_size()["width"]
        slide_location = self.new_find_element(
            By.XPATH, elements["law_service_slide"]
        ).location["y"]
        all_item = ["电话咨询律师", "合同代写/审核", "代发律师函", "线上法律顾问", "见面咨询律师"]
        for item in all_item:
            xpath = elements["law_service_slide_item"].format(item)
            print(xpath)
            while True:
                one = self.new_find_element(By.XPATH, xpath)
                if one:
                    one.click()
                    title = self.get_page_title_text()
                    self.assertIn(item, title, msg="首页天眼服务滑动区域" + item + "跳转错误")
                    self.driver.keyevent(4)
                    break
                else:
                    self.driver.swipe(
                        0.5 * screen_width,
                        slide_location + 100,
                        0.2 * screen_width,
                        slide_location + 100,
                        800,
                    )

    def test_13_tyc_service_page_banner(self):
        """天眼服务页面顶部banner"""
        self.new_find_element(By.ID, elements["bottom_tyc_service_button"]).click()
