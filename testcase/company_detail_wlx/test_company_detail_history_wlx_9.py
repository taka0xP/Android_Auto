# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 09:30
# @Author  : wlx
# @File    : company_detail_history_info.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep, time
from Providers.logger import Logger, error_format
from common.check_rules import *

log = Logger("历史信息_09").getlog()


class Company_detail_Test_wlx_9(MyTest, Operation):
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
        """历史行政处罚维度"""
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.go_company_detail("上海真北乐购生活购物有限公司")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            xzcf = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_xzcf"], check_cover=True)
            xzcf_count = self.new_find_element(By.XPATH, self.ELEMENT["his_xzcf_count"]).text
            xzcf.click()
            gsj_count = self.count(self.new_find_elements(By.ID, self.ELEMENT['his_xzcf_list_count'])[0])
            xyzg_count = self.count(self.new_find_elements(By.ID, self.ELEMENT['his_xzcf_list_count'])[1])
            self.assertEqual(int(xzcf_count), gsj_count + xyzg_count, '历史行政处罚列表页与详情页count数不相等')

            gsj_list_case_num = self.new_find_elements(By.ID, self.ELEMENT['gsj_list_case'])[0].text
            gsj_list_type = self.new_find_elements(By.ID, self.ELEMENT['gsj_list_type'])[0].text
            gsj_list_department = self.new_find_elements(By.ID, self.ELEMENT['gsj_list_department'])[0].text
            gsj_list_date = self.new_find_elements(By.ID, self.ELEMENT['gsj_list_date'])[0].text
            self.assertTrue(check_time(gsj_list_date, is_compare=True), '历史行政处罚-工商局列表页处罚决定日期字段校验错误')

            self.new_find_elements(By.ID, self.ELEMENT['his_xzcf_list_item'])[0].click()

            gsj_detail_case_num = self.new_find_element(By.ID, self.ELEMENT['gsj_detail_case']).text
            self.assertEqual(gsj_detail_case_num, gsj_list_case_num, '历史行政处罚-工商局案号字段详情页与列表页不符')
            gsj_detail_type = self.new_find_element(By.ID, self.ELEMENT['gsj_detail_type']).text
            self.assertEqual(gsj_detail_type, gsj_list_type, '历史行政处罚-工商局处罚类型字段详情页与列表页不符')

            gsj_detail_date = self.new_find_element(By.ID, self.ELEMENT['gsj_detail_date']).text
            self.assertEqual(gsj_detail_date, gsj_list_date, '历史行政处罚-工商局处罚日期字段详情页与列表页不符')

            gsj_detail_department = self.new_find_element(By.ID, self.ELEMENT['gsj_detail_department']).text
            self.assertEqual(gsj_detail_department, gsj_list_department, '历史行政处罚-工商局决定机关字段详情页与列表页不符')

            self.driver.keyevent(4)

            gsj_real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_xzcf_list_item"])
            self.assertEqual(gsj_count, gsj_real_num,
                             "历史行政处罚-工商局实际数量{}与顶部title  count数量{}不相等".format(gsj_real_num, gsj_count))

            self.new_find_elements(By.ID, self.ELEMENT['his_xzcf_list_count'])[1].click()

            xyzg_list_case_num = self.new_find_elements(By.ID, self.ELEMENT['xyzg_list_case'])[0].text
            xyzg_list_department = self.new_find_elements(By.ID, self.ELEMENT['xyzg_list_department'])[0].text
            xyzg_list_date = self.new_find_elements(By.ID, self.ELEMENT['xyzg_list_date'])[0].text
            self.assertTrue(check_time(xyzg_list_date, is_compare=True), '历史行政处罚-信用中国列表页处罚决定日期字段校验错误')

            self.new_find_elements(By.ID, self.ELEMENT['his_xzcf_list_item'])[0].click()

            xyzg_detail_case_num = self.new_find_element(By.ID, self.ELEMENT['xyzg_detail_case']).text
            self.assertEqual(xyzg_detail_case_num, xyzg_list_case_num, '历史行政处罚-信用中国案号字段详情页与列表页不符')

            xyzg_detail_date = self.new_find_element(By.ID, self.ELEMENT['xyzg_detail_date']).text
            self.assertEqual(xyzg_detail_date, xyzg_list_date, '历史行政处罚-信用中国处罚日期字段详情页与列表页不符')

            self.swipe_up_while_ele_located(By.ID, self.ELEMENT['xyzg_detail_department'])
            xyzg_detail_department = self.new_find_element(By.ID, self.ELEMENT['xyzg_detail_department']).text
            self.assertEqual(xyzg_detail_department, xyzg_list_department, '历史行政处罚-信用中国决定机关字段详情页与列表页不符')

            self.driver.keyevent(4)

            xyzg_real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_xzcf_list_item"])
            self.assertEqual(xyzg_count, xyzg_real_num,
                             "历史行政处罚-信用中国实际数量{}与顶部title  count数量{}不相等".format(xyzg_real_num, xyzg_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        """历史股权出质维度"""
        log.info(self.test_002.__doc__)
        try:
            self.go_company_detail("宁夏天元锰业")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["history_moduel"])
            gqcz = self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT["his_gqcz"], check_cover=True)
            gqcz_count = int(self.new_find_element(By.XPATH, self.ELEMENT["his_gqcz_count"]).text)
            gqcz.click()

            list_hname = self.new_find_elements(By.ID, self.ELEMENT['his_gqcz_list_hanme'])[0].text
            list_cname = self.new_find_elements(By.ID, self.ELEMENT['his_gqcz_list_cname'])[0].text
            list_money = self.new_find_elements(By.ID, self.ELEMENT['his_gqcz_list_money'])[0].text
            list_date = self.new_find_elements(By.ID, self.ELEMENT['his_gqcz_list_date'])[0].text
            list_status = self.new_find_elements(By.ID, self.ELEMENT['his_gqcz_list_status'])[0].text

            self.new_find_elements(By.ID, self.ELEMENT['his_gqcz_list_item'])[0].click()
            detail_relation_company = self.new_find_element(By.XPATH, self.ELEMENT['his_gqcz_relation_company'])
            relation_cname = detail_relation_company.text
            detail_relation_company.click()
            jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(relation_cname, jump_name, '关联企业名称{}与跳转企业名称{}不相符'.format(relation_cname, jump_name))
            self.driver.keyevent(4)

            detail_hname = self.new_find_element(By.XPATH, self.ELEMENT['his_gqcz_detail_hanme'])
            hname = detail_hname.text
            self.assertEqual(hname, list_hname, '历史股权出质详情页出质人列表页{}与详情页{}不符'.format(hname, list_hname))
            detail_hname.click()
            jump_name = self.human_detail_name()
            self.assertEqual(hname, jump_name, '历史股权出质详情页出质人名称{}与跳转人员名称{}不相符'.format(hname, jump_name))
            self.driver.keyevent(4)

            detail_cname = self.new_find_element(By.XPATH, self.ELEMENT['his_gqcz_detail_cname'])
            cname = detail_cname.text
            self.assertEqual(cname, list_cname, '历史股权出质详情页质权人列表页{}与详情页{}不符'.format(cname, list_cname))
            detail_cname.click()
            jump_name = self.new_find_element(By.ID, self.ELEMENT["detail_company_name"]).text
            self.assertEqual(cname, jump_name, '历史股权出质详情页出质人名称{}与跳转人员名称{}不相符'.format(cname, jump_name))
            self.driver.keyevent(4)

            detail_money = self.new_find_element(By.ID, self.ELEMENT['his_gqcz_detail_money']).text
            print(detail_money)
            # self.assertTrue(is_bill_available(detail_money), '历史股权出质股权数额单位校验错误')
            self.assertEqual(detail_money, list_money, '历史股权出质列表页股权数额{}与详情页股权数额{}不符'.format(list_money, detail_money))

            detail_date = self.new_find_element(By.ID, self.ELEMENT['his_gqcz_detail_date']).text
            self.assertTrue(check_time(detail_date, is_compare=True), '历史股权出质出质登记日期格式校验错误')
            self.assertEqual(detail_date, list_date, '历史股权出质列表页出质登记日期{}与详情页出质登记日期{}不符'.format(list_date, detail_date))

            detail_status = self.new_find_element(By.ID, self.ELEMENT['his_gqcz_detail_status']).text
            self.assertEqual(detail_status, list_status, '历史股权出质列表页状态{}与详情页状态{}不符'.format(list_status, detail_status))
            self.driver.keyevent(4)

            real_num = self.all_count_compute_v1(By.ID, self.ELEMENT["his_gqcz_list_item"])
            self.assertEqual(gqcz_count, real_num, "历史股权出质实际数量{}与维度count数量{}不相等".format(real_num, gqcz_count))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
