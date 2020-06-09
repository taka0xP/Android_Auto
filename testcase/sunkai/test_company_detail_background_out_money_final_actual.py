# -*- coding: utf-8 -*-
# @Time    : 2020-03-16 10:45
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : company_detail_out_money.py
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


# 企业背景-对外投资-最终受益人-实际控制权
class TestOutMoneyAndFinalHuman(MyTest, Operation):
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
    def test_1_out_money(self):
        """企业背景-对外投资-count"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("红杉资本顾问咨询（北京）有限公司")
        out_money = self.swipe_up_while_ele_located(
            By.XPATH, elements["out_money"], check_cover=True
        )
        out_money_count = self.new_find_element(
            By.XPATH, elements["out_money_count"]
        ).text
        print(out_money_count)
        out_money.click()
        real_num = self.data_list_count(By.ID, elements["out_money_item"])
        self.assertEqual(
            int(out_money_count),
            real_num,
            "对外投资实际数量{}与外侧count数量{}不相等".format(out_money_count, real_num),
        )

    @getimage
    def test_2_out_money_company_and_pic_jump(self):
        """企业背景-对外投资-公司和股权结构法定代表人跳转"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("红杉资本顾问咨询（北京）有限公司")
        self.swipe_up_while_ele_located(
            By.XPATH, elements["out_money"], click=True, check_cover=True
        )
        click_company = self.new_find_elements(By.ID, elements["out_money_company"])[0]
        click_name = click_company.text
        click_company.click()
        jump_name = self.new_find_element(By.ID, elements["detail_company_name"]).text
        self.assertEqual(
            click_name,
            jump_name,
            "对外投资公司展示名称{}和跳转详情页名称{}不一致".format(click_name, jump_name),
        )
        self.driver.keyevent(4)
        self.new_find_elements(By.ID, elements["out_money_pic"])[0].click()
        title = self.new_find_element(By.ID, elements["app_page_title"]).text
        self.assertEqual(title, "股权结构", "对外投资股权结构跳转失败")
        self.driver.keyevent(4)
        law_person = self.new_find_elements(By.ID, elements["out_money_law_person"])[0]
        law_name = law_person.text
        law_person.click()
        jump_law_name = self.new_find_element(By.ID, elements["detail_human_name"]).text
        self.assertEqual(
            law_name,
            jump_law_name,
            "对外投资法定代表人外侧名称{}和详情页名称{}不一致".format(law_name, jump_law_name),
        )

    @getimage
    def test_3_out_money_field_check(self):
        """对外投资字段合法校验"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("红杉资本顾问咨询（北京）有限公司")
        self.swipe_up_while_ele_located(
            By.XPATH, elements["out_money"], click=True, check_cover=True
        )
        # 经营状态
        operates = self.new_find_elements(By.ID, elements["out_money_operate"])
        for n in operates:
            self.assertTrue(operating_check(1, n.text), "对外投资中经营状态字段不合法")
        # 投资数额
        out_num = self.new_find_elements(By.ID, elements["out_money_num"])
        for t in out_num:
            self.assertTrue(is_bill_available(t.text), "对外投资中投资数额字段不合法")
        # 投资比例
        percentage = self.new_find_elements(By.ID, elements["out_money_percentage"])
        for p in percentage:
            self.assertTrue(is_percentage_available(p.text), "对外投资中投资比例字段不合法")
        # 成立日期
        create_time = self.new_find_elements(By.ID, elements["out_money_create_time"])
        for c in create_time:
            self.assertTrue(check_time(c.text, is_compare=True), "对外投资中成立日期字段不合法")

    @getimage
    def test_4_final_human_count(self):
        """企业背景-最终受益人-count校验"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("北京蚂蜂窝网络科技有限公司")
        final = self.swipe_up_while_ele_located(By.XPATH, elements["final_human"])
        final_count = self.new_find_element(
            By.XPATH, elements["final_human_count"]
        ).text
        final.click()
        real_num = self.all_count_compute_v1(By.XPATH, elements["final_human_item"])
        self.assertEqual(
            int(final_count),
            real_num,
            "最终受益人外侧count{}和实际数量{}不一致".format(final_count, real_num),
        )

    def test_5_final_human_jump(self):
        """最终受益人跳转"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("北京米未传媒有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["final_human"], click=True)
        jump_boss = self.new_find_elements(By.ID, elements["final_human_boss"])[0]
        jump_name = jump_boss.text
        jump_boss.click()
        detail_name = self.new_find_element(By.ID, elements["detail_human_name"]).text
        self.assertEqual(
            jump_name,
            detail_name,
            "最终受益人老板名称{}和跳转详情页名称{}不一致".format(jump_name, detail_name),
        )
        self.driver.keyevent(4)
        self.new_find_element(By.ID, elements["final_human_boss_has_company"]).click()
        title = self.new_find_element(By.ID, elements["person_detail_title"]).text
        self.assertEqual(title, "人员详情", "最终受益人他有xx家公司跳转错误")

    def test_6_actual_control_count(self):
        """实际控制权count校验"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("杭州网易云音乐科技有限公司")
        actual_control = self.swipe_up_while_ele_located(
            By.XPATH, elements["actual_control"], check_cover=True
        )
        actual_control_count = self.new_find_element(
            By.XPATH, elements["actual_control_count"]
        ).text
        actual_control.click()
        real_num = self.all_count_compute_v1(By.XPATH, elements["actual_control_item"])
        self.assertEqual(
            int(actual_control_count),
            real_num,
            "最终受益人外侧count{}和实际数量{}不一致".format(actual_control_count, real_num),
        )

    def test_7_actual_control_jump(self):
        """实际控制权公司跳转"""
        login_status = self.is_login()
        if not login_status:
            self.login(self.username, self.password)
        self.into_company_detail("杭州网易云音乐科技有限公司")
        self.swipe_up_while_ele_located(
            By.XPATH, elements["actual_control"], click=True, check_cover=True
        )
        names = self.new_find_elements(By.ID, elements["actual_control_name"])
        for n in names:
            jump_name = n.text
            n.click()
            act = self.new_find_element(By.ID, elements["detail_company_name"]).text
            self.assertEqual(
                jump_name, act, "实际控制权中控股企业名称{}和跳转详情页名称{}不一致".format(jump_name, act)
            )
            self.driver.keyevent(4)

    def test_8_release_account(self):
        self.account.release_account(self.username, 'vip')
