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

log = Logger("历史信息_10").getlog()


class Company_detail_Test_wlx_10(MyTest, Operation):
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
        """历史动产抵押维度"""
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.go_company_detail("邢台市九洲电缆厂")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            dcdy = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_dcdy"], check_cover=True)
            dcdy_count = int(self.new_find_element(By.XPATH, self.ELEMENT["his_dcdy_count"]).text)
            dcdy.click()

            list_type = self.new_find_elements(By.ID, self.ELEMENT['his_dcdy_list_type'])[0].text
            list_money = self.new_find_elements(By.ID, self.ELEMENT['his_dcdy_list_money'])[0].text
            list_date = self.new_find_elements(By.ID, self.ELEMENT['his_dcdy_list_date'])[0].text
            self.assertTrue(check_time(list_date, is_compare=True), '历史动产抵押列表页登记日期字段校验错误')
            # self.assertTrue(is_bill_available(list_money), '历史动产抵押列表页质押数额字段校验错误')

            self.new_find_elements(By.ID, self.ELEMENT['his_dcdy_list_item'])[0].click()
            detail_type = self.swipe_up_while_ele_located(By.ID, self.ELEMENT['his_dcdy_detail_type']).text
            detail_money = self.swipe_up_while_ele_located(By.ID, self.ELEMENT['his_dcdy_detail_money']).text
            detail_date = self.new_find_elements(By.ID, self.ELEMENT['his_dcdy_detail_date'])[0].text
            self.assertEqual(list_type, detail_type, '历史动产抵押列表页质押类型{}与详情页质押类型{}不一致'.format(list_type, detail_type))
            self.assertEqual(list_date, detail_date, '历史动产抵押列表页登记日期{}与详情页登记日期{}不一致'.format(list_date, detail_date))
            self.assertEqual(list_money, detail_money, '历史动产抵押列表页担保数额{}与详情页数额{}不一致'.format(list_money, detail_money))
            belong = self.new_find_element(By.ID, self.ELEMENT['his_dcdy_detail_belong'])
            belong_name = belong.text
            belong.click()
            jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(belong_name, jump_name, '历史动产抵押抵押人名称{}与跳转公司名{}不一致'.format(belong_name, jump_name))
            self.driver.keyevent(4)
            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_dcdy_list_item"])
            self.assertEqual(dcdy_count, real_num, "历史股权出质实际数量{}与维度count数量{}不相等".format(real_num, dcdy_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        """历史行政许可--信用中国维度"""
        log.info(self.test_002.__doc__)
        try:
            self.go_company_detail("一兆韦德健身管理有限公司上海浦东六分公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            xzxk = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_xzxk"], check_cover=True)
            xzxk_count = self.new_find_element(By.XPATH, self.ELEMENT["his_xzxk_count"]).text
            xzxk.click()

            gsj_count = self.count(self.new_find_elements(By.ID, self.ELEMENT['his_xzxk_list_count'])[0])
            xyzg_count = self.count(self.new_find_elements(By.ID, self.ELEMENT['his_xzxk_list_count'])[1])
            self.assertEqual(int(xzxk_count), gsj_count + xyzg_count, '历史行政许可列表页与详情页count数不相等')
            self.new_find_elements(By.ID, self.ELEMENT['his_xzcf_list_count'])[1].click()

            xyzg_list_case_num = self.new_find_elements(By.ID, self.ELEMENT['xzxk_xyzg_list_case'])[0].text
            xyzg_list_department = self.new_find_elements(By.ID, self.ELEMENT['xzxk_xyzg_list_department'])[0].text
            xyzg_list_date = self.new_find_elements(By.ID, self.ELEMENT['xzxk_xyzg_list_date'])[0].text
            self.assertTrue(check_time(xyzg_list_date, is_compare=True), '历史行政许可-信用中国列表页许可决定日期字段校验错误')

            self.new_find_elements(By.ID, self.ELEMENT['his_xzxk_list_item'])[0].click()
            legal_person = self.new_find_element(By.ID, self.ELEMENT['xzxk_xyzg_detail_legal_person'])
            name = legal_person.text
            legal_person.click()
            jump_name = self.human_detail_name()
            self.assertEqual(name, jump_name, '历史行政许可详情页法人字段{}跳转后名称{}不符'.format(name, jump_name))
            self.driver.keyevent(4)

            xyzg_detail_case_num = self.new_find_element(By.ID, self.ELEMENT['xzxk_xyzg_detail_case']).text
            self.assertEqual(xyzg_detail_case_num, xyzg_list_case_num, '历史行政许可-信用中国决定文书号字段详情页与列表页不符')

            xyzg_detail_date = self.new_find_element(By.ID, self.ELEMENT['xzxk_xyzg_detail_date']).text
            self.assertEqual(xyzg_detail_date, xyzg_list_date, '历史行政许可-信用中国许可决定日期字段详情页与列表页不符')

            xyzg_detail_department = self.new_find_element(By.ID, self.ELEMENT['xzxk_xyzg_detail_department']).text
            self.assertEqual(xyzg_detail_department, xyzg_list_department, '历史行政许可-信用中国决定机关字段详情页与列表页不符')

            self.driver.keyevent(4)

            xyzg_real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_xzxk_list_item"])
            self.assertEqual(xyzg_count, xyzg_real_num,
                             "历史行政许可-信用中国实际数量{}与顶部title  count数量{}不相等".format(xyzg_real_num, xyzg_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_003(self):
        """历史行政许可--工商局维度"""
        log.info(self.test_003.__doc__)
        try:
            self.go_company_detail("辽阳市金马旅行社有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            xzxk = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_xzxk"], check_cover=True)
            xzxk_count = self.new_find_element(By.XPATH, self.ELEMENT["his_xzxk_count"]).text
            xzxk.click()

            gsj_count = self.count(self.new_find_elements(By.ID, self.ELEMENT['his_xzxk_list_count'])[0])
            xyzg_count = self.count(self.new_find_elements(By.ID, self.ELEMENT['his_xzxk_list_count'])[1])
            self.assertEqual(int(xzxk_count), gsj_count + xyzg_count, '历史行政许可列表页与详情页count数不相等')

            gsj_list_case_name = self.new_find_elements(By.ID, self.ELEMENT['xzxk_gsj_list_case'])[0].text
            gsj_list_start_date = self.new_find_elements(By.ID, self.ELEMENT['xzxk_gsj_list_start_date'])[0].text
            gsj_list_end_date = self.new_find_elements(By.ID, self.ELEMENT['xzxk_gsj_list_end_date'])[0].text

            self.assertTrue(check_time(gsj_list_start_date, is_compare=True), '历史行政许可-工商局列表页有效期自日期字段校验错误')
            print(gsj_list_end_date)
            self.assertTrue(check_time(gsj_list_end_date), '历史行政许可-工商局列表页有效期至日期字段校验错误')
            self.new_find_elements(By.ID, self.ELEMENT['his_xzxk_list_item'])[0].click()

            gsj_detail_case_name = self.new_find_element(By.ID, self.ELEMENT['xzxk_gsj_detail_case']).text
            self.assertEqual(gsj_detail_case_name, gsj_list_case_name, '历史行政许可文件名字段详情页与列表页不符')

            gsj_detail_start_date = self.new_find_element(By.ID, self.ELEMENT['xzxk_gsj_detail_start_date']).text
            self.assertEqual(gsj_detail_start_date, gsj_list_start_date, '历史行政许可-工商局开始有效期日期字段详情页与列表页不符')

            gsj_detail_end_date = self.new_find_element(By.ID, self.ELEMENT['xzxk_gsj_detail_end_date']).text
            self.assertEqual(gsj_detail_end_date, gsj_list_end_date, '历史行政许可-工商局结束有效期日期字段详情页与列表页不符')

            self.driver.keyevent(4)

            gsj_real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_xzxk_list_item"])
            self.assertEqual(gsj_count, gsj_real_num,
                             "历史行政许可-工商局实际数量{}与顶部title  count数量{}不相等".format(gsj_real_num, gsj_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
