# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 15:10
# @Author  : wlx
# @File    : company_detail_history_info.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep, time
from Providers.logger import Logger, error_format
from common.check_rules import *

log = Logger("历史信息_11").getlog()


class Company_detail_Test_wlx_11(MyTest, Operation):
    """VIP用户进入公司详情页历史信息校验"""
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
        """历史商标信息维度"""
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.go_company_detail("上海毛巾十五厂")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_sbxx"])
            sbxx = self.new_find_element(By.XPATH, self.ELEMENT["his_sbxx"])
            sbxx_count = int(self.new_find_element(By.XPATH, self.ELEMENT['his_sbxx_count']).text)
            sbxx.click()
            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_sbxx_list_item"])
            self.assertEqual(sbxx_count, real_num, "历史网站备案实际数量{}与维度count数量{}不相等".format(real_num, sbxx_count))

            list_logo_name = self.new_find_elements(By.ID, self.ELEMENT['his_sbxx_list_logo_name'])[0].text
            list_logo_num = self.new_find_elements(By.ID, self.ELEMENT['his_sbxx_list_logo_num'])[0].text
            list_date = self.new_find_elements(By.ID, self.ELEMENT['his_sbxx_list_date'])[0].text
            list_type = self.new_find_elements(By.ID, self.ELEMENT['his_sbxx_list_type'])[0].text
            list_status = self.new_find_elements(By.ID, self.ELEMENT['his_sbxx_list_status'])[0].text

            self.new_find_elements(By.ID, self.ELEMENT['his_sbxx_list_item'])[0].click()

            detail_logo_name = self.new_find_element(By.ID, self.ELEMENT['his_sbxx_detail_logo_name']).text
            self.assertEqual(list_logo_name, detail_logo_name,
                             '历史商标列表页商标名称{}与详情页商标名称{}不符'.format(list_logo_name, detail_logo_name))

            detail_logo_num = self.new_find_element(By.ID, self.ELEMENT['his_sbxx_detail_logo_num']).text
            self.assertEqual(list_logo_num, detail_logo_num,
                             '历史商标列表页商标注册号{}与详情页商标注册号{}不符'.format(list_logo_num, detail_logo_num))

            detail_date = self.new_find_element(By.ID, self.ELEMENT['his_sbxx_detail_date']).text
            self.assertEqual(list_date, detail_date, '历史商标列表页商标申请日期{}与详情页商标申请日期{}不符'.format(list_date, detail_date))

            type1 = self.new_find_element(By.ID, self.ELEMENT['his_sbxx_detail_type']).text
            detail_type = type1.replace('类', '')
            self.assertEqual(list_type, detail_type, '历史商标列表页商标分类{}与详情页商标分类{}不符'.format(list_type, detail_type))

            detail_status = self.new_find_element(By.ID, self.ELEMENT['his_sbxx_detail_status']).text
            self.assertEqual(list_status, detail_status, '历史商标列表页商标状态{}与详情页商标状态{}不符'.format(list_status, detail_status))

            self.swipe_up_while_ele_located(By.ID, self.ELEMENT['trademark_registration'], click=True)
            self.assertTrue(self.isElementExist(By.XPATH, self.ELEMENT['logo_trade_name']), '历史商标页进图顾问商标注册h5页面错误')
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.ID, self.ELEMENT['detail_register_name_cn'])
            register = self.new_find_element(By.ID, self.ELEMENT['detail_register_name_cn'])
            register_name = register.text
            register.click()
            jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(register_name, jump_name, '申请人名称{}与跳转的名称{}不一致'.format(register_name, jump_name))
            self.driver.keyevent(4)

            self.swipe_up_while_ele_located(By.ID, self.ELEMENT['detail_register_address'])
            register_address = self.new_find_element(By.ID, self.ELEMENT['detail_register_address'])
            address = register_address.text
            register_address.click()
            jump_address = self.new_find_element(By.ID, self.ELEMENT['map_address']).text
            self.assertEqual(address, jump_address, '历史商标信息详情页申请人地址跳转外部地址{}与内部地址{}不一致'.format(address, jump_address))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        """历史网站备案维度"""
        log.info(self.test_002.__doc__)
        try:
            self.go_company_detail("乐视控股（北京）有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_wzba"])
            wzba = self.new_find_element(By.XPATH, self.ELEMENT["his_wzba"])
            wzba_count = int(self.new_find_element(By.XPATH, self.ELEMENT["his_wzba_count"]).text)
            wzba.click()

            domain_name = self.new_find_elements(By.ID, self.ELEMENT['his_wzba_domain_name'])[0].text
            web_address = self.new_find_elements(By.XPATH, self.ELEMENT['his_wzba_web_address'])[0].text
            self.assertIn(domain_name, web_address, '网址{}不包含域名{}'.format(domain_name, web_address))

            date = self.new_find_elements(By.ID, self.ELEMENT['his_wzba_date'])[0].text
            self.assertTrue(check_time(date, is_compare=True), '历史网站备案审核日期字段校验错误')

            real_num = self.all_count_compute_v1(By.XPATH, self.ELEMENT["his_wzba_list_item"])
            self.assertEqual(wzba_count, real_num, "历史网站备案实际数量{}与维度count数量{}不相等".format(real_num, wzba_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_003(self):
        """邀请认证"""
        log.info(self.test_003.__doc__)
        try:
            self.go_company_detail("乐视控股（北京）有限公司")
            cname = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.new_find_element(By.ID, self.ELEMENT['self_info']).click()
            self.swipe_up_while_ele_located(By.ID, self.ELEMENT['invite_claim_icon'], click=True)
            invite_company_name = self.new_find_element(By.XPATH, self.ELEMENT['invite_claim_detail_company_name']).text
            self.assertEqual(cname, invite_company_name, '邀请认证页公司名{}与公司详情页名称{}不一样'.format(invite_company_name, cname))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_004(self):
        """"有关问答"""
        log.info(self.test_004.__doc__)
        try:
            self.go_company_detail("乐视控股（北京）有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT['allabout_question'], check_cover=True)
            about_question = self.new_find_element(By.XPATH, self.ELEMENT['about_question'])
            about_question_count = self.count(about_question)
            self.new_find_element(By.XPATH, self.ELEMENT['allabout_question']).click()
            real_num = self.all_count_compute_v1(By.XPATH, self.ELEMENT["about_question_list_item"])
            self.assertEqual(about_question_count, real_num,
                             "有关问题实际数量{}与维度count数量{}不相等".format(real_num, about_question_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
