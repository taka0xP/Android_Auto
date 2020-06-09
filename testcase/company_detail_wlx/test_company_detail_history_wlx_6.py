# -*- coding: utf-8 -*-
# @Time    : 2020-03-20 16:00
# @Author  : wlx
# @File    : company_detail_history_info.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep
from Providers.logger import Logger, error_format
from common.check_rules import *

log = Logger("历史信息_06").getlog()


class Company_detail_Test_wlx_6(MyTest, Operation):
    """公司详情页历史信息校验"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 获取excel
        cls.ELEMENT = Read_Ex().read_excel("company_detail_wlx")
        cls.vip_user = cls.account.get_account("vip", "0")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.account.release_account(account=cls.vip_user, account_type="vip", account_special="0")

    def go_company_detail(self, company_name, index=0):
        self.search_company(company_name)
        self.new_find_elements(
            By.XPATH, self.ELEMENT["company_name_search_result_list"]
        )[index].click()

    @getimage
    def test_001(self):
        """历史法律诉讼维度"""
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.go_company_detail("京沈铁路客运专线京冀有限公司")
            # cname = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            flss = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_flss"])
            flss_count = self.new_find_element(By.XPATH, self.ELEMENT["his_flss_count"]).text
            flss.click()

            list_title = self.new_find_elements(By.ID, self.ELEMENT['his_flss_list_title'])
            # list_title_1 = list_title[0].text

            list_send_time = self.new_find_elements(By.ID, self.ELEMENT['his_flss_list_send_time'])
            for n in list_send_time:
                self.assertTrue(check_time(n.text, is_compare=True), '公司详情页-历史信息-开庭公告列表开庭日期日期字段校验错误')

            list_case_num = self.new_find_elements(By.ID, self.ELEMENT['his_flss_list_case_num'])[0].text

            list_title[0].click()

            # detail_title = self.new_find_element(By.XPATH, self.ELEMENT['his_flss_detail_title']).text
            # self.assertEqual(detail_title, list_title_1, '公司详情页-历史信息-法律诉讼title列表{}页与详情页内容{}不符'.format(list_title_1, detail_title))

            # relation_company = self.new_find_elements(By.XPATH, self.ELEMENT['his_flss_detail_relation_company'])
            #
            # l = []
            #
            # for i in relation_company:
            #     company_name = i.text
            #     l.append(company_name)
            # if cname in l:
            #     result = True
            # else:
            #     result = False
            # self.assertTrue(result, '公司详情页-历史信息-法律诉讼详情页关联公司无当前公司')
            #
            # click_name = relation_company[0].text
            # relation_company[0].click()
            # jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            # self.assertEqual(
            #     click_name,
            #     jump_name,
            #     "历史法律诉讼详情页公司展示名称{}和跳转详情页名称{}不一致".format(click_name, jump_name)
            # )
            #
            # self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT['his_flss_detail_case_num'])
            detail_case_num = self.new_find_element(By.XPATH, self.ELEMENT['his_flss_detail_case_num']).text
            self.assertEqual(detail_case_num, list_case_num, '公司详情页-历史信息-法律诉讼案号列表页与详情页内容不符')

            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_flss_list_item"])
            self.assertEqual(int(flss_count), real_num, "历史法律诉讼实际数量{}与外侧count数量{}不相等".format(real_num, flss_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        """历史法院公告维度"""
        log.info(self.test_002.__doc__)
        try:
            self.go_company_detail("宁夏天元锰业")
            cname = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            fygg = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_fygg"])
            fygg_count = self.new_find_element(By.XPATH, self.ELEMENT["his_fygg_count"]).text

            fygg.click()

            # list_client = self.new_find_elements(By.ID,self.ELEMENT['his_fygg_list_client'])[0].text
            # list_client_list = list_client.split('、')

            list_publisher = self.new_find_elements(By.ID, self.ELEMENT['his_fygg_list_publisher'])[0].text
            list_publish_type = self.new_find_elements(By.ID, self.ELEMENT['his_fygg_list_publish_type'])[0].text
            list_publish_date = self.new_find_elements(By.ID, self.ELEMENT['his_fygg_list_publish_date'])
            for n in list_publish_date:
                self.assertTrue(check_time(n.text, is_compare=True), '历史法院公告刊登日期校验错误')
            list_publish_date_1 = list_publish_date[0].text

            self.new_find_elements(By.ID, self.ELEMENT['his_fygg_list_item'])[0].click()

            drtail_relation_company = self.new_find_elements(By.XPATH, self.ELEMENT['his_fygg_detail_relation_company'])
            l = []

            for i in drtail_relation_company:
                company_name = i.text
                l.append(company_name)
            if cname in l:
                result = True
            else:
                result = False
            self.assertFalse(result, '公司详情页-历史信息-法院公告详情页关联公司无当前公司')

            detail_court = self.new_find_element(By.ID, self.ELEMENT['his_fygg_detail_court']).text
            self.assertEqual(detail_court, list_publisher, '历史法院公告列表页公告人和详情页法院字段内容不一致')

            detail_publish_date = self.new_find_element(By.ID, self.ELEMENT['his_fygg_detail_publish_date']).text
            self.assertEqual(detail_publish_date, list_publish_date_1, '历史法院公告列表页发布日期和详情页发布日期字段内容不一致')

            detail_punlish_type = self.new_find_element(By.ID, self.ELEMENT['his_fygg_detail_publish_type']).text
            self.assertEqual(detail_punlish_type, list_publish_type, '历史法院公告列表页公告类型和详情页公告类型字段内容不一致')

            plaintiff = self.new_find_elements(By.XPATH, self.ELEMENT['his_fygg_detail_plaintiff'])[0]
            plaintiff_click = plaintiff.get_attribute("clickable")
            if plaintiff_click == 'true':
                click_name = plaintiff.text
                plaintiff.click()
                jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
                self.assertNotEqual(click_name, jump_name,
                                    "历史法院公告详情页上诉方公司展示名称{}和跳转详情页名称{}不一致".format(click_name, jump_name))
                self.driver.keyevent(4)

            defendant = self.new_find_elements(By.XPATH, self.ELEMENT['his_fygg_detail_defendant'])[0]
            defendant_click = defendant.get_attribute("clickable")
            if defendant_click == 'true':
                click_name = defendant.text
                defendant.click()
                jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
                self.assertNotEqual(click_name, jump_name,
                                    "历史法律诉讼详情页被诉方公司展示名称{}和跳转详情页名称{}不一致".format(click_name, jump_name))
                self.driver.keyevent(4)

            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_fygg_list_item"])
            self.assertEqual(int(fygg_count), real_num, "历史法院公告实际数量{}与外侧count数量{}不相等".format(real_num, fygg_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_003(self):
        """历史失信信息维度"""
        log.info(self.test_003.__doc__)
        try:
            self.go_company_detail("乐视控股（北京）有限公司")
            cname = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            legal_name = self.new_find_element(By.ID, self.ELEMENT["legal_name"]).text
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            sxxx = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sxxx"])
            sxxx_count = self.new_find_element(By.XPATH, self.ELEMENT["his_sxxx_count"]).text
            sxxx.click()

            list_case_num = self.new_find_elements(By.ID, self.ELEMENT['his_sxxx_list_case_num'])[0].text
            list_court = self.new_find_elements(By.ID, self.ELEMENT['his_sxxx_list_court'])[0].text
            list_performance = self.new_find_elements(By.ID, self.ELEMENT['his_sxxx_list_performance'])[0].text
            list_regdate = self.new_find_elements(By.ID, self.ELEMENT['his_sxxx_list_regdate'])[0].text
            list_publishdate = self.new_find_elements(By.ID, self.ELEMENT['his_sxxx_list_publishdate'])[0].text

            self.new_find_elements(By.ID, self.ELEMENT["his_sxxx_list_item"])[0].click()

            detail_company = self.new_find_element(By.ID, self.ELEMENT['his_sxxx_detail_company'])
            sxxx_detail_company = detail_company.text
            self.assertEqual(cname, sxxx_detail_company, '历史失信详情被执行人名称与当前公司名不符')
            detail_company.click()
            jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(jump_name, sxxx_detail_company, '历史失信信息跳转公司详情页公司名称不对应')
            self.driver.keyevent(4)

            detail_legal_name = self.new_find_element(By.ID, self.ELEMENT["his_sxxx_legal_name"])
            self.assertEqual(legal_name, detail_legal_name.text, '历史失信详情页法人名称与公司基础信息不符')
            sxxx_detail_legal_name = detail_legal_name.text
            detail_legal_name.click()
            hname = self.human_detail_name()
            self.assertEqual(hname, sxxx_detail_legal_name, '历史失信详情页法人名称跳转错误')
            self.driver.keyevent(4)

            detail_court = self.new_find_element(By.ID, self.ELEMENT['his_sxxx_detail_court']).text
            self.assertEqual(detail_court, list_court, '历史失信信息详情执行法院字段与列表页不匹配')

            detail_case_num = self.new_find_element(By.ID, self.ELEMENT['his_sxxx_detail_case_num']).text
            self.assertEqual(detail_case_num, list_case_num, '历史失信信息详情案号字段与列表页不匹配')

            detail_regdate = self.new_find_element(By.ID, self.ELEMENT['his_sxxx_detail_regdate']).text
            self.assertEqual(detail_regdate, list_regdate, '历史失信信息详情立案日期字段与列表页不匹配')
            self.assertTrue(check_time(detail_regdate, is_compare=True), '历史信息详情页立案日期字段校验错误')

            self.swipe_up_while_ele_located(By.ID, self.ELEMENT['his_sxxx_detail_performance'])
            detail_performance = self.new_find_element(By.ID, self.ELEMENT['his_sxxx_detail_performance']).text
            self.assertEqual(detail_performance, list_performance, '历史失信信息详情执行情况字段与列表页不匹配')

            self.swipe_up_while_ele_located(By.ID, self.ELEMENT['his_sxxx_detail_publishdate'])
            detail_publishdate = self.new_find_element(By.ID, self.ELEMENT['his_sxxx_detail_publishdate']).text
            self.assertEqual(detail_publishdate, list_publishdate, '历史失信信息详情发布日期字段与列表页不匹配')
            self.assertTrue(check_time(detail_publishdate, is_compare=True), '历史信息详情页发布日期字段校验错误')
            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_sxxx_list_item"])
            self.assertEqual(int(sxxx_count), real_num, "历史失信信息实际数量{}与外侧count数量{}不相等".format(real_num, sxxx_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
