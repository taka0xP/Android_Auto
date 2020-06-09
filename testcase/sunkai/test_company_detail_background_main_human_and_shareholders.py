# -*- coding: utf-8 -*-
# @Time    : 2020-03-06 11:43
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : detail.py
# @Software: PyCharm
from common.MyTest import MyTest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.ReadData import Read_Ex
from Providers.logger import Logger
from common.check_rules import *
from Providers.account.account import Account


excel = Read_Ex()
elements = excel.read_excel("companydetailsunkai")
log = Logger("企业背景").getlog()


# 企业背景-主要人员和股东信息
class TestMainHuman(MyTest, Operation):
    account = Account()
    username = account.get_account('vip')
    password = account.get_pwd()

    def into_company_detail(self, company):
        """
        通过搜索进入公司详情页，搜索结果选择第一条
        :param company: 搜索公司名称
        :return: None
        """
        self.new_find_element(By.ID, elements["index_search_input"]).click()
        self.new_find_element(By.ID, elements["search_result_input"]).send_keys(company)
        self.new_find_elements(By.ID, elements["search_result_item"])[0].click()

    @getimage
    def test_1_main_human_count(self):
        """企业背景-主要人员-count"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("瓴盛科技有限公司")
        log.info("企业背景-主要人员-count-校验")
        main_human = self.swipe_up_while_ele_located(By.XPATH, elements["main_human"])
        main_human_count = self.new_find_element(
            By.XPATH, elements["main_human_count"]
        ).text
        main_human.click()
        real_num = self.data_list_count(By.ID, elements["main_human_item"])
        self.assertEqual(
            int(main_human_count),
            real_num,
            "主要人员实际数量{}与外侧count数量{}不相等".format(main_human_count, real_num),
        )

    @getimage
    def test_2_main_human_jump(self):
        """企业背景-主要人员-跳转"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("中信建投证券股份有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["main_human"], click=True)
        log.info("企业背景-主要人员-上市披露的高管信息跳转")
        self.new_find_element(By.ID, elements["main_human_ipo"]).click()
        page_title = self.new_find_element(By.ID, elements["app_page_title"]).text
        self.assertEqual(page_title, "高管信息", "企业背景-主要人员-上市披露的高管信息跳转失败")
        self.driver.keyevent(4)
        log.info("企业背景-主要人员-人员跳转")
        click_item = self.new_find_elements(By.ID, elements["main_human_item"])[0]
        click_human = click_item.text
        click_item.click()
        detail_human_name = self.new_find_element(
            By.ID, elements["detail_human_name"]
        ).text
        self.assertEqual(
            click_human,
            detail_human_name,
            "人员入口名称{}和详情页名称{}不一致".format(click_human, detail_human_name),
        )
        self.driver.keyevent(4)
        log.info("企业背景-主要人员-他有xx家公司跳转")
        self.new_find_elements(By.ID, elements["main_human_has_company"])[0].click()
        person_detail_title = self.new_find_element(
            By.ID, elements["person_detail_title"]
        ).text
        self.assertEqual(person_detail_title, "人员详情", "主要人员他有xx家公司跳转失败")

    @getimage
    def test_3_shareholders_count(self):
        """企业背景-股东信息-count校验"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("国安社区（北京）科技有限公司")
        shareholders = self.swipe_up_while_ele_located(
            By.XPATH, elements["shareholders"]
        )
        log.info("企业背景-股东信息-count校验")
        shareholders_count = self.new_find_element(
            By.XPATH, elements["shareholders_count"]
        ).text
        shareholders.click()
        shareholders_item = self.data_list_count(By.ID, elements["shareholders_item"])
        self.assertEqual(
            int(shareholders_count),
            shareholders_item,
            "股东信息实际数量{}和外侧count数{}不相等".format(shareholders_count, shareholders_item),
        )

    @getimage
    def test_4_shareholders_detail_history_jump(self):
        """企业背景-股东信息-历史股东跳转"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("思享时代（北京）科技有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["shareholders"], click=True)
        self.new_find_element(By.ID, elements["shareholders_detail_history"]).click()
        page_title = self.new_find_element(By.ID, elements["app_page_title"]).text
        self.assertEqual(page_title, "历史股东", "企业背景-股东信息-历史股东跳转失败")

    @getimage
    def test_5_shareholders_company_jump(self):
        """企业背景-股东信息-股东是公司跳转"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("智动时代（北京）科技有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["shareholders"], click=True)
        log.info("企业背景-股东信息-股东是公司跳转")
        jump_human = self.new_find_elements(By.ID, elements["shareholders_item"])[0]
        jump_text = jump_human.text
        jump_human.click()
        detail_human_name = self.new_find_element(
            By.ID, elements["detail_company_name"]
        ).text
        self.assertEqual(
            jump_text,
            detail_human_name,
            "股东信息股东是公司跳转入口名称{}和公司详情名称{}不一致".format(jump_text, detail_human_name),
        )
        self.driver.keyevent(4)
        log.info("企业背景-股东信息-股东是公司股权结构跳转")

    @getimage
    def test_6_shareholders_human_jump(self):
        """企业背景-股东信息-股东是人跳转"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("九湾（北京）科技有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["shareholders"], click=True)
        log.info("企业背景-股东信息-股东是人跳转")
        jump_human = self.new_find_elements(By.ID, elements["shareholders_item"])[0]
        jump_text = jump_human.text
        jump_human.click()
        detail_human_name = self.new_find_element(
            By.ID, elements["detail_human_name"]
        ).text
        self.assertEqual(
            jump_text,
            detail_human_name,
            "股东信息股东是人跳转入口名称{}和人详情名称{}不一致".format(jump_text, detail_human_name),
        )
        self.driver.keyevent(4)
        log.info("企业背景-股东信息-股东是人-他有xx家公司跳转")
        self.new_find_elements(By.ID, elements["has_company"])[0].click()
        detail_human_name_has = self.new_find_element(
            By.ID, elements["detail_human_name"]
        ).text
        self.assertEqual(
            jump_text,
            detail_human_name_has,
            "股东信息股东是人他有xx家公司名称{}和人详情名称{}不一致".format(jump_text, detail_human_name_has),
        )

    @getimage
    def test_7_shareholders_field_check(self):
        """股东信息字段合法校验"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("九湾（北京）科技有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["shareholders"], click=True)

        # 认缴出资额
        log.info("认缴出资额")
        money_num = self.new_find_elements(By.XPATH, elements["money_num"])[0].text
        print('认缴出资额--->', money_num)
        money_num_flag = is_bill_available(money_num)
        self.assertTrue(money_num_flag, "股东信息认缴出资额{}校验失败".format(money_num))

        # 认缴出资日期
        log.info("认缴出资日期")
        money_time = self.new_find_elements(By.XPATH, elements["money_time"])[0].text
        money_time_flag = check_time(money_time)
        self.assertTrue(money_time_flag, "股东信息认缴出资日期{}校验失败".format(money_time_flag))

        # 持股比例
        log.info("持股比例")
        holder_percent = self.new_find_elements(By.ID, elements["holder_percent"])[
            0
        ].text
        holder_percent_flag = is_percentage_available(holder_percent)
        self.assertTrue(holder_percent_flag, "股东信息持股比例{}校验失败".format(holder_percent))

    def test_8_release_account(self):
        self.account.release_account(self.username, 'vip')
