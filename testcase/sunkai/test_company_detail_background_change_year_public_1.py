# -*- coding: utf-8 -*-
# @Time    : 2020-03-19 10:56
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : test_company_detail_background_change_year_public_1.py
# @Software: PyCharm
from common.MyTest import MyTest
from common.operation import Operation, getimage
from common.CreditIdentifier import UnifiedSocialCreditIdentifier
from selenium.webdriver.common.by import By
from common.ReadData import Read_Ex
from Providers.logger import Logger
from common.check_rules import *
import random
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
    def test_1_change_count(self):
        """企业背景-变更记录-count校验"""
        if not self.is_login():
            self.login(self.username, self.password)
        self.into_company_detail("上海任意门科技有限公司")
        change = self.swipe_up_while_ele_located(By.XPATH, elements["change_list"])
        change_count = self.new_find_element(
            By.XPATH, elements["change_list_count"]
        ).text
        change.click()
        real_num = self.data_list_count(By.ID, elements["change_list_item"])
        self.assertEqual(
            int(change_count),
            real_num,
            "公司详情页变更记录count数{}和实际数量{}不一致".format(change_count, real_num),
        )

    @getimage
    def test_2_change_select_count(self):
        """企业背景-变更记录-筛选项count校验"""
        if not self.is_login():
            self.login(self.username, self.password)
        self.into_company_detail("大商股份有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["change_list"], click=True)
        self.new_find_element(By.ID, elements["change_list_select"]).click()
        select_list = self.new_find_elements(By.ID, elements["change_list_select_list"])
        select_item = random.choice(select_list[1:])
        select_text = select_item.text
        select_num = re.findall(r'(?<=\uff08)\d+(?=\uff09)', select_text)[0]
        select_item.click()
        real_num = self.data_list_count(By.ID, elements["change_list_item"])
        self.assertEqual(int(select_num), real_num,
                         '公司详情页变更记录筛选显示数量{}和实际数量{}不一致'.format(select_item, real_num))

    @getimage
    def test_3_change_field_check(self):
        """"企业背景-变更记录-内容字段校验"""
        if not self.is_login():
            self.login(self.username, self.password)
        self.into_company_detail("银亿股份有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["change_list"], click=True)
        change_names = self.new_find_elements(By.ID, elements['change_name'])
        for name in change_names:
            self.assertNotEqual(name.text, '', '公司详情页变更记录变更项目名称为空')
        change_times = self.new_find_elements(By.ID, elements['change_time'])
        for t in change_times:
            self.assertTrue(check_time(t.text, is_compare=True), '公司详情页变更记录变更时间校验失败')
        change_before = self.new_find_elements(By.ID, elements['change_before'])
        for b in change_before:
            self.assertNotEqual(b.text, '', '公司详情页变更记录变更前内容为空')
        change_after = self.new_find_elements(By.ID, elements['change_after'])
        for a in change_after:
            self.assertNotEqual(a.text, '', '公司详情页变更记录变更后内容为空')

    @getimage
    def test_4_year_count(self):
        """企业背景-企业年报count校验"""
        if not self.is_login():
            self.login(self.username, self.password)
        self.into_company_detail("国家电网有限公司")
        year = self.swipe_up_while_ele_located(By.XPATH, elements["year_log"])
        year_count = self.new_find_element(
            By.XPATH, elements["year_log_count"]
        ).text
        year.click()
        real_num = self.data_list_count(By.ID, elements["year_log_item"])
        self.assertEqual(
            int(year_count),
            real_num,
            "公司详情页企业年报count数{}和实际数量{}不一致".format(year_count, real_num),
        )

    @getimage
    def test_5_year_log_field_check_one(self):
        """企业背景-企业年报-字段校验-基本信息和网站或网店信息部分"""
        if not self.is_login():
            self.login(self.username, self.password)
        self.into_company_detail("阿迪达斯（中国）有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["year_log"], click=True, check_cover=True)
        c = UnifiedSocialCreditIdentifier()
        self.new_find_elements(By.ID, elements['year_log_item'])[0].click()
        # 社会统一信用代码
        year_code = self.new_find_element(By.ID, elements['year_code']).text
        self.assertTrue(c.check_social_credit_code(year_code), '企业年报统一信用代码字段校验失败')
        # 企业经营状态
        year_status = self.new_find_element(By.ID, elements['year_status']).text
        self.assertTrue(operating_check(1, year_status), '企业年报企业经营状态字段校验失败')
        # 从业人数
        worker_num = self.new_find_element(By.ID, elements['year_worker_num']).text
        self.assertEqual(worker_num, '企业选择不公示', '企业年报从业人数字段校验失败')
        # 是否有网店或网站
        has_shop = self.new_find_element(By.ID, elements['year_has_shop']).text
        self.assertIn(has_shop, ('是', '否'), '企业年报是否有网店字段校验失败')
        # 企业联系电话
        year_log_land_line = self.new_find_element(By.ID, elements['year_log_land_line']).text
        self.assertTrue(check_land_line(year_log_land_line), '企业年报企业联系电话字段校验失败')
        # 企业电子邮箱
        email = self.new_find_element(By.ID, elements['year_email']).text
        self.assertTrue(check_email(email), '企业年报企业电子邮箱字段校验失败')
        # 邮政编码
        postcode = self.new_find_element(By.ID, elements['year_postcode']).text
        self.assertTrue(check_postcode(postcode), '企业年报邮政编码字段校验失败')
        # 是否有投资信息或购买其他公司股份
        year_is_out = self.new_find_element(By.ID, elements['year_is_out']).text
        self.assertIn(year_is_out, ('是', '否'), '企业年报是否有投资信息或购买其他公司股份字段校验失败')
        # 网站或者网店类型
        web_type = self.swipe_up_while_ele_located(By.ID, elements['year_web_type']).text
        self.assertIn(web_type, ['网页'], '企业年报网站类型字段校验失败')
        # 网址
        website = self.swipe_up_while_ele_located(By.ID, elements['year_website']).text
        self.assertTrue(check_url(website), '企业年报网址字段校验失败')
        # 网站名称
        year_web_name = self.swipe_up_while_ele_located(By.ID, elements['year_web_name']).text
        self.assertNotEqual(year_web_name, '', '企业年报网站名称字段校验失败')
        # 企业通信地址
        self.new_find_element(By.ID, elements['year_address']).click()
        title = self.new_find_element(By.ID, elements['app_page_title']).text
        self.assertEqual(title, '公司地图', '企业年报企业通信地址跳转失败')

    @getimage
    def test_5_year_log_field_check_two(self):
        """企业背景-企业年报-字段校验-股东出资信息部分"""
        if not self.is_login():
            self.login(self.username, self.password)
        self.into_company_detail("耐克商业（中国）有限公司")
        self.swipe_up_while_ele_located(By.XPATH, elements["year_log"], click=True, check_cover=True)
        self.new_find_elements(By.ID, elements['year_log_item'])[0].click()
        # 股东出资信息名称跳转
        shareholder = self.swipe_up_while_ele_located(By.ID,
                                                      elements['year_shareholder_name'])
        name = shareholder.text
        shareholder.click()
        detail_name = self.new_find_element(By.ID, elements['detail_company_name']).text
        self.assertEqual(name, detail_name, '企业年报中股东及出资信息种股东跳转失败')
        self.driver.keyevent(4)
        # 股东出资信息股权结构跳转
        self.new_find_element(By.ID, elements['year_holder_map']).click()
        title = self.new_find_element(By.ID, elements['app_page_title']).text
        self.assertEqual(title, '股权结构', '企业年报股东及出资股权结构跳转失败')
        self.driver.keyevent(4)
        # 认缴出资日期
        out_time = self.swipe_up_while_ele_located(By.ID, elements['year_out_time']).text
        self.assertTrue(check_time(out_time), '企业年报股东出资认缴出资日期校验失败')
        # 实缴出资日期
        real_out_time = self.new_find_element(By.ID, elements['year_real_out_time']).text
        self.assertTrue(check_time(real_out_time), '企业年报股东出资实缴出资日期校验失败')
        # 认缴出资额
        out_num = self.swipe_up_while_ele_located(By.ID, elements['year_out_num']).text
        self.assertTrue(is_bill_available(out_num), '企业年报股东出资认缴出资额校验失败')
        # 实缴出资额
        real_out_num = self.new_find_element(By.ID, elements['year_real_out_num']).text
        self.assertTrue(is_bill_available(real_out_num), '企业年报股东出资实缴出资额校验失败')
        # 认缴出资方式
        out_way = self.swipe_up_while_ele_located(By.ID, elements['year_out_way']).text
        self.assertEqual(out_way, '货币', '企业年报股东出资认缴出资方式校验失败')
        # 实缴出资方式
        real_out_way = self.new_find_element(By.ID, elements['year_real_out_way']).text
        self.assertEqual(real_out_way, '货币', '企业年报股东出资实缴出资方式校验失败')

    def test_6_release_account(self):
        self.account.release_account(self.username, 'vip')
