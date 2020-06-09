from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
import re
import time
import random
import unittest

log = Logger("公司详情页-自主信息·联系企业01").getlog()

# 非vip：11099995054 无所属公司及姓名
# vip:11099990155 无所属公司及姓名


class Company_own_information_contact_01(MyTest, Operation):
    """公司详情页-自主信息·联系企业01"""

    def search_result(self, company, index=0):
        """进入关键词搜索结果列表第一家公司详情页"""
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/txt_search_copy1").click()
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/search_input_et").send_keys(company)
        self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name']")[index].click()
    def is_valid_date(self, str):
        """判断日期字符串格式是否为YYYY.MM.DD"""
        try:
            time.strptime(str, "%Y.%m.%d")
            return True
        except:
            return False
    def get_title_name(self):
        '''获取页面title名称'''
        text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_name').text
        return text
    def check_vip_page(self):
        '''判断是否在VIP会员页面'''
        result = self.isElementExist(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_tab_vip' and @text='VIP会员']")
        return result
    def page_back(self):
        '''点击页面返回'''
        self.new_find_element(By.ID,"com.tianyancha.skyeye:id/app_title_back").click()
    def login_page_check(self,way,element):
        '''判断是否在登录页面 way:id/xpath element:元素'''
        if way == 1:
            self.new_find_element(By.ID,element).click()
        elif way == 2:
            self.new_find_element(By.XPATH,element).click()
        result = self.isElementExist(By.ID,"com.tianyancha.skyeye:id/btv_title")
        text = self.new_find_element(By.ID,"com.tianyancha.skyeye:id/btv_title").text
        if text == '短信验证码登录':
            log.info('当前在短信验证码登录页面')
        elif text == '密码登录':
            log.info('当前在密码登录页面')
        return result
    def contact_company(self, company_name):
        """滑动到自主信息-联系企业模块"""
        self.search_result(company_name, 0)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/radio_user_evaluate").click()
        count = 0
        while True:
            if not self.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/tv_contact_title"):
                if count <= 5:
                    self.swipeUp(x1=0.5, y1=0.70, y2=0.30, t=500)
                    count += 1
                else:
                    log.error("错误———未找到联系企业模块")
                    break
            else:
                break

        self.swipeUp(x1=0.5, y1=0.80, y2=0.20, t=500)

    @getimage
    def test_GSXQY_ZZXX_0001(self):
        """自主信息·联系企业1"""
        log.info(self.test_GSXQY_ZZXX_0001.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()

        company_name = "上海钧正网络科技有限公司"
        self.contact_company(company_name)
        #联系企业六个模块：我要合作/我要投资/我要投诉/合作意向/投资意向/投诉意见
        button_list = [
            "com.tianyancha.skyeye:id/btn_teamwork",
            "com.tianyancha.skyeye:id/btn_invest",
            "com.tianyancha.skyeye:id/btn_complain",
            "com.tianyancha.skyeye:id/btn_teamwork_intent",
            "com.tianyancha.skyeye:id/btn_invest_intent",
            "com.tianyancha.skyeye:id/btn_complain_intent"]

        goal_01 = "「联系企业」模块包含六个选项"
        log.info(goal_01)
        result_01_01 = self.isElementExist(By.ID,button_list[0])
        self.assertTrue(result_01_01, msg="错误——我要合作")
        result_01_02 = self.isElementExist(By.ID,button_list[1])
        self.assertTrue(result_01_02, msg="错误——我要投资")
        result_01_03 = self.isElementExist(By.ID,button_list[2])
        self.assertTrue(result_01_03, msg="错误——我要投诉")
        result_01_04 = self.isElementExist(By.ID,button_list[3])
        self.assertTrue(result_01_04, msg="错误——合作意向")
        result_01_05 = self.isElementExist(By.ID,button_list[4])
        self.assertTrue(result_01_05, msg="错误——投资意向")
        result_01_06 = self.isElementExist(By.ID,button_list[5])
        self.assertTrue(result_01_06, msg="错误——投诉意见")

        # 0315版本去掉「去认证」入口
        # goal_02 = "未登录点击「去认证」进入登录页面"
        # log.info(goal_02)
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_auth_or_edit").click()
        # title_text = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btv_title").text
        # self.assertEqual(title_text, "短信验证码登录", msg="错误————%s" % goal_02)
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()

        goal_03 = "未登录点击「联系企业」模块任意选项进入登录页面"
        log.info(goal_03)
        i = random.randint(0,len(button_list)-1)
        log.info(button_list[i])
        result_03 = self.login_page_check(1,button_list[i])
        self.assertTrue(result_03,msg='错误——%s'%goal_03)

    #0426版本下掉普通用户批量联系3次功能
    # @getimage
    # def test_GSXQY_ZZXX_0002(self):
    #     """自主信息·联系企业2"""
    #     log.info(self.test_GSXQY_ZZXX_0002.__doc__)
    #
    #     login_status = self.is_login()
    #     if login_status == True:
    #         self.logout()
    #     self.login(11099995054, "ef08beca")
    #
    #     company_name = "上海钧正网络科技有限公司"
    #     self.contact_company(company_name)
    #     # 联系企业六个模块：我要合作/我要投资/我要投诉/合作意向/投资意向/投诉意见
    #     button_list = [
    #         "com.tianyancha.skyeye:id/btn_teamwork",
    #         "com.tianyancha.skyeye:id/btn_invest",
    #         "com.tianyancha.skyeye:id/btn_complain",
    #         "com.tianyancha.skyeye:id/btn_teamwork_intent",
    #         "com.tianyancha.skyeye:id/btn_invest_intent",
    #         "com.tianyancha.skyeye:id/btn_complain_intent"]
    #
    #     goal_01 = "非vip登陆点击「我要合作」进入「我要合作」页面"
    #     log.info(goal_01)
    #     self.new_find_element(By.ID,button_list[0]).click()
    #     page_result_02 = self.get_title_name()
    #     self.assertEqual(page_result_02,'我要合作',msg="错误———%s" % goal_01)
    #
    #     goal_02 = "「我要合作」页面"
    #     log.info(goal_02)
    #     result_02_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip")
    #     self.assertTrue(result_02_01, msg="错误———无充值VIP入口")
    #     text_02_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_company_title").text
    #     self.assertIn(company_name, text_02_01, msg="错误———公司名称带入")
    #     text_02_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_own_company").text
    #     self.assertEqual("请输入公司名称", text_02_02, msg="错误———公司名称输入框")
    #     text_02_03 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_name").text
    #     self.assertEqual("请输入姓名", text_02_03, msg="错误———姓名输入框")
    #     text_02_04 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_teamwork_intent").text
    #     self.assertEqual("请输入你的合作意向", text_02_04, msg="错误———意向输入框")
    #     text_02_05 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_number").text
    #     self.assertEqual("11099995054", text_02_05, msg="错误———联系方式")
    #     text_02_06 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_time").text
    #     result_02_02 = self.is_valid_date(text_02_06)
    #     self.assertTrue(result_02_02, msg="错误———日期格式")
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip").click()
    #     result_02_03 = self.check_vip_page()
    #     self.page_back()
    #     self.assertTrue(result_02_03, msg="错误——点击充值VIP未跳转VIP会员页面")
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tip_close_iv").click()
    #     time.sleep(0.5)
    #     result_02_04 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip")
    #     self.assertFalse(result_02_04, msg="错误——点击❎未关闭开通VIP提示")
    #     self.page_back()
    #
    #     goal_03 = "「我要投资」页面"
    #     log.info(goal_03)
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_invest").click()
    #     page_result_02 = self.get_title_name()
    #     self.assertEqual(page_result_02,'我要投资',msg="错误———%s" % goal_03)
    #     result_03_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip")
    #     self.assertTrue(result_03_01, msg="错误———无充值VIP入口")
    #     text_03_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_company_title").text
    #     self.assertIn(company_name, text_03_01, msg="错误———公司名称带入")
    #     text_03_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_own_company").text
    #     self.assertEqual("请输入公司名称", text_03_02, msg="错误———公司名称输入框")
    #     text_03_03 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_name").text
    #     self.assertEqual("请输入姓名", text_03_03, msg="错误———姓名输入框")
    #     text_03_04 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_teamwork_intent").text
    #     self.assertEqual("请输入你的投资意向", text_03_04, msg="错误———意向输入框")
    #     text_03_05 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_number").text
    #     self.assertEqual("11099995054", text_03_05, msg="错误———联系方式")
    #     text_03_06 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_time").text
    #     result_03_02 = self.is_valid_date(text_03_06)
    #     self.assertTrue(result_03_02, msg="错误———日期格式")
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip").click()
    #     result_03_03 = self.check_vip_page()
    #     self.page_back()
    #     self.assertTrue(result_03_03, msg="错误——点击充值VIP未跳转VIP会员页面")
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tip_close_iv").click()
    #     time.sleep(0.5)
    #     result_03_04 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip")
    #     self.assertFalse(result_03_04, msg="错误——点击❎未关闭开通VIP提示")
    #     self.page_back()
    #
    #     goal_04 = "「我要投诉」页面"
    #     log.info(goal_04)
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_complain").click()
    #     page_result_03 = self.get_title_name()
    #     self.assertEqual(page_result_03,'我要投诉',msg="错误———%s" % goal_04)
    #     result_04_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip")
    #     self.assertTrue(result_04_01, msg="错误———无充值VIP入口")
    #     text_04_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_company_title").text
    #     self.assertIn(company_name, text_04_01, msg="错误———公司名称带入")
    #     text_04_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_own_company").text
    #     self.assertEqual("请输入公司名称", text_04_02, msg="错误———公司名称输入框")
    #     text_04_03 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_name").text
    #     self.assertEqual("请输入姓名", text_04_03, msg="错误———姓名输入框")
    #     text_04_04 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_teamwork_intent").text
    #     self.assertEqual("请输入你的投诉意见", text_04_04, msg="错误———意向输入框")
    #     text_04_05 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_number").text
    #     self.assertEqual("11099995054", text_04_05, msg="错误———联系方式")
    #     text_04_06 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_time").text
    #     result_04_02 = self.is_valid_date(text_04_06)
    #     self.assertTrue(result_04_02, msg="错误———日期格式")
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip").click()
    #     result_04_03 = self.check_vip_page()
    #     self.page_back()
    #     self.assertTrue(result_04_03, msg="错误——点击充值VIP未跳转VIP会员页面")
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tip_close_iv").click()
    #     time.sleep(0.5)
    #     result_04_04 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_recharge_vip")
    #     self.assertFalse(result_04_04, msg="错误——点击❎未关闭开通VIP提示")
    #
    #     goal_05 = "合作/投资/投诉页面公司名称不填入点击发送toast提示「请填写公司名称」"
    #     log.info(goal_05)
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_send").click()
    #     text_05_01 = self.new_find_element(By.XPATH, "/hierarchy/android.widget.Toast").text
    #     self.assertEqual("请填写公司名称", text_05_01, msg="错误————%s" % goal_05)
    #
    #     goal_06 = "合作/投资/投诉页面公司填入、姓名不填入点击发送toast提示「请填写姓名」"
    #     log.info(goal_06)
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_own_company").click()
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_search_input").send_keys("北京金堤")
    #     self.new_find_element(By.XPATH,"//android.widget.RelativeLayout[2]/android.widget.ListView/android.widget.RelativeLayout[1]",).click()
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_send").click()
    #     text_06_01 = self.new_find_element(By.XPATH, "/hierarchy/android.widget.Toast").text
    #     self.assertEqual("请填写姓名", text_06_01, msg="错误————%s" % goal_06)
    #
    #     goal_07 = "合作/投资/投诉页面公司填入、姓名填入、意向不填入点击发送toast提示「请填写内容」"
    #     log.info(goal_07)
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_name").send_keys("天眼妹")
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_send").click()
    #     text_07_01 = self.new_find_element(By.XPATH, "/hierarchy/android.widget.Toast").text
    #     self.assertEqual("请填写内容", text_07_01, msg="错误————%s" % goal_07)
    #
    #     goal_08 = "合作/投资/投诉页面公司填入、姓名填入、意向填入、联系方式不填入点击发送toast提示「请填写联系电话」"
    #     log.info(goal_08)
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_teamwork_intent").send_keys("意向内容")
    #     self.adb_send_input(By.ID, "com.tianyancha.skyeye:id/et_person_number", " ", 112)
    #     self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_send").click()
    #     text_08_01 = self.new_find_element(By.XPATH, "/hierarchy/android.widget.Toast").text
    #     self.assertEqual("请填写联系电话", text_08_01, msg="错误————%s" % goal_08)

    @getimage
    def test_GSXQY_ZZXX_0003(self):
        """自主信息·联系企业3"""
        log.info(self.test_GSXQY_ZZXX_0003.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login(11099990155, "ef08beca")

        company_name = "上海钧正网络科技有限公司"
        self.contact_company(company_name)

        goal_01 = "vip账号点击「我要合作/我要投资/我要投诉」进入我要「合作/投资/投诉页面」，顶部提示今日剩余次数，3s后消失"
        log.info(goal_01)
        button_list = [
            "com.tianyancha.skyeye:id/btn_teamwork",
            "com.tianyancha.skyeye:id/btn_invest",
            "com.tianyancha.skyeye:id/btn_complain"]
        i = random.randint(0,len(button_list)-1)
        log.info(button_list[i])
        self.new_find_element(By.ID, button_list[i]).click()
        if i == 0:
            page_result = self.get_title_name()
            self.assertEqual(page_result,'我要合作',msg="未进入我要合作页面")
            result_01_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/limit_tip_tv")
            self.assertTrue(result_01_01, msg="未展示顶部提示")
            time.sleep(3)
            result_01_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/limit_tip_tv")
            self.assertFalse(result_01_02, msg="顶部提示未消失")
            text_01_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_company_title").text
            self.assertIn(company_name, text_01_01, msg="错误———公司名称带入")
            text_01_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_own_company").text
            self.assertEqual("请输入公司名称", text_01_02, msg="错误———公司名称输入框")
            text_01_03 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_name").text
            self.assertEqual("请输入姓名", text_01_03, msg="错误———姓名输入框")
            text_01_04 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_teamwork_intent").text
            self.assertEqual("请输入你的合作意向", text_01_04, msg="错误———意向输入框")
            text_01_05 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_number").text
            self.assertEqual("11099990155", text_01_05, msg="错误———联系方式")
            text_01_06 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_time").text
            result_01_03 = self.is_valid_date(text_01_06)
            self.assertTrue(result_01_03, msg="错误———日期格式")

        elif i == 1:
            page_result = self.get_title_name()
            self.assertEqual(page_result,'我要投资',msg="未进入我要投资页面")
            result_02_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/limit_tip_tv")
            self.assertTrue(result_02_01, msg="未展示顶部提示")
            time.sleep(3)
            result_02_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/limit_tip_tv")
            self.assertFalse(result_02_02, msg="顶部提示未消失")
            text_02_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_company_title").text
            self.assertIn(company_name, text_02_01, msg="错误———公司名称带入")
            text_02_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_own_company").text
            self.assertEqual("请输入你的公司名称", text_02_02, msg="错误———公司名称输入框")
            text_02_03 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_name").text
            self.assertEqual("请输入你的姓名", text_02_03, msg="错误———姓名输入框")
            text_02_04 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_teamwork_intent").text
            self.assertEqual("请输入你的投资意向", text_02_04, msg="错误———意向输入框")
            text_02_05 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_number").text
            self.assertEqual("11099990155", text_02_05, msg="错误———联系方式")
            text_02_06 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_time").text
            result_02_03 = self.is_valid_date(text_02_06)
            self.assertTrue(result_02_03, msg="错误———日期格式")
        elif i == 2:
            page_result = self.get_title_name()
            self.assertEqual(page_result,'我要投诉',msg="未进入我要投诉页面")
            result_03_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/limit_tip_tv")
            self.assertTrue(result_03_01, msg="未展示顶部提示")
            time.sleep(3)
            result_03_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/limit_tip_tv")
            self.assertFalse(result_03_02, msg="顶部提示未消失")
            text_03_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_company_title").text
            self.assertIn(company_name, text_03_01, msg="错误———公司名称带入")
            text_03_02 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_own_company").text
            self.assertEqual("请输入公司名称", text_03_02, msg="错误———公司名称输入框")
            text_03_03 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_name").text
            self.assertEqual("请输入姓名", text_03_03, msg="错误———姓名输入框")
            text_03_04 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_teamwork_intent").text
            self.assertEqual("请输入你的投诉意见", text_03_04, msg="错误———意向输入框")
            text_03_05 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_number").text
            self.assertEqual("11099990155", text_03_05, msg="错误———联系方式")
            text_03_06 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_time").text
            result_03_03 = self.is_valid_date(text_03_06)
            self.assertTrue(result_03_03, msg="错误———日期格式")

        goal_02 = "合作/投资/投诉页面公司名称不填入点击发送toast提示「请填写公司名称」"
        log.info(goal_02)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_send").click()
        text_02_01 = self.new_find_element(By.XPATH, "/hierarchy/android.widget.Toast").text
        self.assertEqual("请填写公司名称", text_02_01, msg="错误————%s" % goal_02)

        goal_03 = "合作/投资/投诉页面公司填入、姓名不填入点击发送toast提示「请填写姓名」"
        log.info(goal_03)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_own_company").click()
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_search_input").send_keys("北京金堤")
        self.new_find_element(By.XPATH,
                              "//android.widget.RelativeLayout[2]/android.widget.ListView/android.widget.RelativeLayout[1]", ).click()
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_send").click()
        text_03_01 = self.new_find_element(By.XPATH, "/hierarchy/android.widget.Toast").text
        self.assertEqual("请填写姓名", text_03_01, msg="错误————%s" % goal_03)

        goal_04 = "合作/投资/投诉页面公司填入、姓名填入、意向不填入点击发送toast提示「请填写内容」"
        log.info(goal_04)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_person_name").send_keys("天眼妹")
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_send").click()
        text_04_01 = self.new_find_element(By.XPATH, "/hierarchy/android.widget.Toast").text
        self.assertEqual("请填写内容", text_04_01, msg="错误————%s" % goal_04)

        goal_05 = "合作/投资/投诉页面公司填入、姓名填入、意向填入、联系方式不填入点击发送toast提示「请填写联系电话」"
        log.info(goal_05)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/et_teamwork_intent").send_keys("意向内容")
        self.adb_send_input(By.ID, "com.tianyancha.skyeye:id/et_person_number", " ", 112)
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_send").click()
        text_05 = self.new_find_element(By.XPATH, "/hierarchy/android.widget.Toast").text
        self.assertEqual("请填写联系电话", text_05, msg="错误————%s" % goal_05)

        self.page_back()

        # 0315版本去掉此功能
        # goal_02 = ["已登陆自主信息「联系企业」展示去认证入口", "点击跳转「企业实名认证」页面"]
        # log.info(goal_02)
        # text_02 = self.new_find_element(
        #     By.ID, "com.tianyancha.skyeye:id/tv_auth_or_edit"
        # ).text
        # self.assertEqual(text_02, "去认证", msg="错误————%s" % goal_02[0])
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_auth_or_edit").click()
        # result_02_02 = self.isElementExist(
        #     By.XPATH,
        #     "//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text='企业实名认证']",
        # )
        # self.assertTrue(result_02_02, msg="错误————%s" % goal_02[1])
        #
        # goal_03 = "「企业实名认证」页面点击返回弹出确认弹框"
        # log.info(goal_03)
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()
        # result_03_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/lLayout_bg")
        # self.assertTrue(result_03_01, msg="错误————%s" % goal_03)
        # result_03_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_neg")
        # result_03_03 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_pos")
        # self.assertTrue(result_03_02, msg="无「放弃」button")
        # self.assertTrue(result_03_03, msg="无「去认证」button")
        #
        # goal_04 = ["点击「去认证」留在当前页面", "点击「放弃」返回「自主信息」页面"]
        # log.info(goal_04)
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_pos").click()
        # result_04_01 = self.isElementExist(
        #     By.XPATH,
        #     "//*[@resource-id='com.tianyancha.skyeye:id/app_title_name' and @text='企业实名认证']",
        # )
        # self.assertTrue(result_04_01, msg="错误————%s" % goal_04[0])
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/app_title_back").click()
        # self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_neg").click()
        # result_04_02 = self.isElementExist(
        #     By.ID, "com.tianyancha.skyeye:id/tv_contact_title"
        # )
        # self.assertTrue(result_04_02, msg="错误————%s" % goal_04[1])

        goal_06 = "点击未认证公司的「合作意向/投资意向/投诉意见」提示去认证"
        button_list = [
            "com.tianyancha.skyeye:id/btn_teamwork_intent",
            "com.tianyancha.skyeye:id/btn_invest_intent",
            "com.tianyancha.skyeye:id/btn_complain_intent"]
        i = random.randint(0,len(button_list)-1)
        log.info(button_list[i])
        self.new_find_element(By.ID, button_list[i]).click()
        text_06 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/txt_msg").text
        self.assertEqual(text_06, "认证该家企业后，可查看所有信息！", msg="错误————%s" % goal_06)
        result_06_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_neg")
        result_06_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_pos")
        self.assertTrue(result_06_01, msg="无「取消」button")
        self.assertTrue(result_06_02, msg="无「去认证企业」button")

        goal_07 = "点击「取消」返回「自主信息」页面"
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_neg").click()
        result_07 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_contact_title")
        self.assertTrue(result_07, msg="错误————%s" % goal_07)

        goal_08 = "点击「去认证企业」跳转「选择认证套餐」页面"
        self.new_find_element(By.ID, button_list[i]).click()
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_pos").click()
        result_08 = self.get_title_name()
        self.page_back()
        self.assertEqual(result_08,'选择认证套餐', msg="错误————%s" % goal_08)

    @getimage
    def test_GSXQY_ZZXX_0004(self):
        """自主信息·联系企业4"""
        log.info(self.test_GSXQY_ZZXX_0004.__doc__)

        login_status = self.is_login()
        if login_status == True:
            company_name = "山东智慧译百信息技术有限公司"
            self.contact_company(company_name)

            goal_01 = "点击已认证公司的「合作意向/投资意向/投诉意见」提示该企业已认证"
            log.info(goal_01)
            button_list = [
                "com.tianyancha.skyeye:id/btn_teamwork_intent",
                "com.tianyancha.skyeye:id/btn_invest_intent",
                "com.tianyancha.skyeye:id/btn_complain_intent"]
            i = random.randint(0,len(button_list)-1)
            log.info(button_list[i])
            self.new_find_element(By.ID, button_list[i]).click()
            text_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/txt_msg").text
            self.assertEqual(text_01, "该企业已被认证，去认证自己的企业！", msg="错误————%s" % goal_01)
            result_01_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_neg")
            result_01_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_pos")
            self.assertTrue(result_01_01, msg="无「取消」button")
            self.assertTrue(result_01_02, msg="无「去认证企业」button")

            goal_02 = "点击「取消」返回「自主信息」页面"
            log.info(goal_02)
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_neg").click()
            result_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_contact_title")
            self.assertTrue(result_02, msg="错误————%s" % goal_02)

            goal_03 = "点击「去认证企业」跳转「选择认证套餐」页面"
            log.info(goal_03)
            self.new_find_element(By.ID, button_list[i]).click()
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_pos").click()
            result_03 = self.get_title_name()
            self.assertEqual(result_03,'选择认证套餐',msg="错误————%s" % goal_03)
        else:
            self.login(11099990155, "ef08beca")
            company_name = "山东智慧译百信息技术有限公司"
            self.contact_company(company_name)

            goal_01 = "点击已认证公司的「合作意向/投资意向/投诉意见」提示该企业已认证"
            log.info(goal_01)
            button_list = [
                "com.tianyancha.skyeye:id/btn_teamwork_intent",
                "com.tianyancha.skyeye:id/btn_invest_intent",
                "com.tianyancha.skyeye:id/btn_complain_intent"]
            i = random.randint(0, len(button_list) - 1)
            log.info(button_list[i])
            self.new_find_element(By.ID, button_list[i]).click()
            text_01 = self.new_find_element(By.ID, "com.tianyancha.skyeye:id/txt_msg").text
            self.assertEqual(text_01, "该企业已被认证，去认证自己的企业！", msg="错误————%s" % goal_01)
            result_01_01 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_neg")
            result_01_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_pos")
            self.assertTrue(result_01_01, msg="无「取消」button")
            self.assertTrue(result_01_02, msg="无「去认证企业」button")

            goal_02 = "点击「取消」返回「自主信息」页面"
            log.info(goal_02)
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_neg").click()
            result_02 = self.isElementExist(By.ID, "com.tianyancha.skyeye:id/tv_contact_title")
            self.assertTrue(result_02, msg="错误————%s" % goal_02)

            goal_03 = "点击「去认证企业」跳转「选择认证套餐」页面"
            log.info(goal_03)
            self.new_find_element(By.ID, button_list[i]).click()
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_pos").click()
            result_03 = self.get_title_name()
            self.assertEqual(result_03, '选择认证套餐', msg="错误————%s" % goal_03)

if __name__ == "__main__":
    unittest.main()