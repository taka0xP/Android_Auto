# -*- coding: utf-8 -*-
# @Time    : 2020-04-01 16:10
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : test_company_detail_background_change_year_public_2.py.py
# @Software: PyCharm
from common.MyTest import MyTest
from common.operation import Operation, getimage
from common.CreditIdentifier import UnifiedSocialCreditIdentifier
from selenium.webdriver.common.by import By
from common.ReadData import Read_Ex
from Providers.logger import Logger
from common.check_rules import *
from Providers.account.account import Account

excel = Read_Ex()
elements = excel.read_excel("companydetailsunkai")
log = Logger("企业背景").getlog()


# 企业背景-变更记录-企业年报-企业公示
class TestChangeYearPublic(MyTest, Operation):
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
    def test_1_year_log_field_check_three(self):
        """企业背景-企业年报-字段校验-企业资产状况信息部分"""
        if not self.is_login():
            self.login(self.username, self.password)
        self.into_company_detail("敦煌鼎丰建设工程有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["year_log"], click=True, check_cover=True)
        # 企业资产状况信息
        self.new_find_elements(By.ID, elements['year_log_item'])[-2].click()
        all_field = ['资产总额', '所有者权益合计', '销售总额', '利润总额',
                     '营业总收入中主营业务收入', '净利润', '纳税总额', '负债总额']
        for f, n in zip(all_field, range(1, len(all_field) + 1)):
            xpath = elements['year_company_money'].format(str(n))
            text = self.swipe_up_while_ele_located(By.XPATH, xpath).text
            self.assertTrue(is_bill_available(text), '企业年报企业资产状况{}校验失败'.format(f))
        # 对外提供保证担保信息

    def test_2_release_account(self):
        self.account.release_account(self.username, 'vip')
