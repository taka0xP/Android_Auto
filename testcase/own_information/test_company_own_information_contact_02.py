from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import re
import time
import random

log = Logger("公司详情页-自主信息·联系企业02").getlog()

# 企业主：11099990160


class Company_own_information_contact_02(MyTest, Operation):
    """公司详情页-自主信息·联系企业02"""

    def search_result(self, company, index=0):
        """进入关键词搜索结果列表第一家公司详情页"""
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/txt_search_copy1").click()
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/search_input_et").send_keys(company)
        self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name']")[index].click()

    def contact_company(self, company_name):
        """滑动到自主信息-联系企业模块"""
        self.search_result(company_name, 0)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/radio_user_evaluate").click()
        count = 0
        while True:
            if not self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_contact_title"):
                if count <= 5:
                    self.swipeUp(x1=0.5, y1=0.70, y2=0.30, t=500)
                    count += 1
                else:
                    log.error("错误———未找到联系企业模块")
                    break
            else:
                break

        self.swipeUp(x1=0.5, y1=0.80, y2=0.20, t=500)

    def get_title_name(self):
        '''获取页面title名称'''
        text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_name').text
        return text

    @getimage
    def test_GSXQY_ZZXX_0005(self):
        """自主信息·联系企业5"""
        log.info(self.test_GSXQY_ZZXX_0005.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login(11099990160, "ef08beca")
        company_name = "北京天使筑梦大数据有限公司"
        self.contact_company(company_name)

        # 0315版本去掉此功能
        # goal_01 = "企业主账号查看所认证公司的「联系企业」模块无「去认证」入口，展示「查看联系信息」"
        # log.info(goal_01)
        # text_01 = self.new_find_element(
        #     By.ID, "com.tianyancha.skyeye:id/tv_auth_or_edit"
        # ).text
        # self.assertEqual(text_01, "查看联系信息", msg="错误———%s" % goal_01)
        #
        # goal_02 = "点击「查看联系信息」进入「收到的名片」页面"
        # log.info(goal_02)
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_auth_or_edit").click()
        # log.info(goal_02)
        # text_02 = self.new_find_element(
        #     By.ID, "com.tianyancha.skyeye:id/app_title_name"
        # ).text
        # self.assertIn("收到的名片", text_02, msg="错误————%s" % goal_02)
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()

        goal_03 = "点击「合作/投资/投诉意向」进入「收到的名片」页面，合作/投资/投诉意向被选中"
        log.info(goal_03)
        button_list = [
            "com.tianyancha.skyeye:id/btn_teamwork_intent",
            "com.tianyancha.skyeye:id/btn_invest_intent",
            "com.tianyancha.skyeye:id/btn_complain_intent"]
        #合作意向
        self.new_find_element(By.ID, button_list[0]).click()
        text_03 = self.get_title_name()
        self.assertIn("收到的名片", text_03, msg="进入收到的名片页面错误")
        result_03_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_teamwork").is_selected()
        self.assertTrue(result_03_01, "错误——合作意向被选中")
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()
        #投资意向
        self.new_find_element(By.ID, button_list[1]).click()
        result_03_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_invest").is_selected()
        self.assertTrue(result_03_02, "错误——投资意向被选中")
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()
        #投诉意见
        self.new_find_element(By.ID, button_list[2]).click()
        result_03_03 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_other").is_selected()
        self.assertTrue(result_03_03, "错误——投诉意见被选中")

        # 0315去掉此功能
        # goal_05 = "企业主账号查看非所认证公司的「联系企业」模块，展示「去认证」入口"
        # log.info(goal_05)
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_name_back").click()
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/search_back_iv").click()
        # company_name = "北京金堤科技有限公司"
        # self.contact_company(company_name)
        # text_04 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_auth_or_edit").text
        # self.assertEqual(text_04, "去认证", msg="错误————%s" % goal_05)
