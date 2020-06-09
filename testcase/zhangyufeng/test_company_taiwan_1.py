# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 11:16
# @Author  : ZYF
# @File    : test_company_taiwan_1.py
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger, error_format
from common.MyTest import MyTest
from common.operation import Operation, getimage
from common.ReadData import Read_Ex
import unittest
from common.check_rules import *
from common.CreditIdentifier import UnifiedSocialCreditIdentifier
from Providers.account.account import Account
log = Logger("台湾企业").getlog()

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文---基金会英文名称
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    if check_str == "-":
        return False
    else:
        for ch in check_str:
            if u"\u4e00" <= ch <= u"\u9fa5":
                return True
        return False

class Taiwan_01(MyTest, Operation):
    """台湾企业-企业背景"""
    a = Read_Ex()
    ELEMENT = a.read_excel("Company_taiwan")

    def enter_official_information(self, company_name):
        """
        首页搜索公司名进入到公司官方信息页
        company_name : 公司名称
        :return: company_name 官方信息页
        """
        self.company_name = company_name
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/home_tab1").click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/txt_search_copy1"
        ).click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/search_input_et"
        ).send_keys(self.company_name)
        self.new_find_elements(By.ID, "com.tianyancha.skyeye:id/tv_company_name")[
            0
        ].click()
        log.info("进入公司 {} 官方信息页".format(self.company_name))

    def get_elemengt_text(self, element):
        text = self.new_find_element(By.ID, element).text
        return text

    @getimage
    def test_001_taiwan_djxx_p0(self):
        """
        台湾企业-企业背景-登记信息
        """
        log.info(self.test_001_taiwan_djxx_p0.__doc__)
        try:
            self.enter_official_information('怡安医疗器材股份有限公司')
            # 进入登记信息模块
            self.new_find_element(By.XPATH, self.ELEMENT["registration"]).click()
            title_name = self.get_elemengt_text(self.ELEMENT['title_name'])
            log.info("页面title：{}".format(title_name))
            self.assertEqual(self.company_name, title_name, msg="登记信息跟所属公司不对应")
            # 登记信息
            # 英文名称
            eng_name = self.get_elemengt_text(self.ELEMENT['enname'])
            log.info("英文名称:{}".format(eng_name))
            self.assertFalse(is_contain_chinese(eng_name))
            # 资本总额（新台币）
            count_mn = self.get_elemengt_text(self.ELEMENT['count_mn'])
            log.info("资本总额（新台币）:{}".format(count_mn))
            self.assertTrue(is_bill_available(count_mn))
            # 实收资本额（新台币）
            count_mn_pt = self.get_elemengt_text(self.ELEMENT['count_mn_pt'])
            log.info("实收资本额（新台币）:{}".format(count_mn_pt))
            self.assertTrue(is_bill_available(count_mn_pt))
            # 代表人
            legel_person_name = self.get_elemengt_text(self.ELEMENT['legel_person_name'])
            log.info("代表人:{}".format(legel_person_name))

            # 公司状况
            tv_status = self.get_elemengt_text(self.ELEMENT['tv_status'])
            log.info("公司状况:{}".format(tv_status))

            # 股权状态
            tv_equity_status = self.get_elemengt_text(self.ELEMENT['tv_equity_status'])
            log.info("股权状态:{}".format(tv_equity_status))

            # 统一编号
            tv_code = self.get_elemengt_text(self.ELEMENT['tv_code'])
            log.info("统一编号:{}".format(tv_code))

            # 登记机关
            tv_reg_office = self.get_elemengt_text(self.ELEMENT['tv_reg_office'])
            log.info("登记机关:{}".format(tv_reg_office))

            # 标准设立日期
            tv_setdata = self.get_elemengt_text(self.ELEMENT['tv_setdata'])
            log.info("标准设立日期:{}".format(tv_setdata))
            self.assertTrue(check_time(tv_setdata))
            # 最后核准变更日期
            tv_final_change_data = self.get_elemengt_text(self.ELEMENT['tv_final_change_data'])
            log.info("最后核准变更日期:{}".format(tv_final_change_data))
            self.assertTrue(check_time(tv_final_change_data))
            # 公司所在地
            tv_address = self.get_elemengt_text(self.ELEMENT['tv_address'])
            log.info("公司所在地:{}".format(tv_address))
            # 经营范围
            tv_business = self.get_elemengt_text(self.ELEMENT['tv_business'])
            log.info("经营范围:{}".format(tv_business))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_taiwan_djs_p0(self):
        """
        台湾企业-企业背景-董监事
        """
        log.info(self.test_002_taiwan_djs_p0.__doc__)
        try:
            self.enter_official_information('怡安医疗器材股份有限公司')
            # 获取董监事公司详情页count
            targeting_count = self.new_find_element(By.XPATH, self.ELEMENT['targeting_count']).text
            targeting_count = int(targeting_count)
            log.info("董监事count：{}".format(targeting_count))
            # 进入董监事模块
            self.new_find_element(By.XPATH, self.ELEMENT["targeting"]).click()
            title_name = self.get_elemengt_text(self.ELEMENT['title_name'])
            log.info("页面title：{}".format(title_name))
            self.assertEqual("董监事", title_name, msg="页面title不对应")
            # 获取董监事列表页count
            targeting_count1 = self.all_count_compute_v1(By.ID, self.ELEMENT['tv_person_name'])
            log.info("统计董监事count：{}".format(targeting_count1))
            self.assertEqual(targeting_count1, targeting_count, msg="count数不对应")
            # 所代表法人
            tv_setdata = self.new_find_elements(By.ID, self.ELEMENT['tv_setdata'])[1].text
            log.info("所代表法人：{}".format(tv_setdata))
            # 持有股份数
            tv_final_change_data = self.new_find_elements(By.ID, self.ELEMENT['tv_final_change_data'])[1].text
            log.info("持有股份数：{}".format(tv_final_change_data))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_taiwan_jlr_p0(self):
        """
        台湾企业-企业背景-经理人
        """
        log.info(self.test_003_taiwan_jlr_p0.__doc__)
        try:
            self.enter_official_information('怡安医疗器材股份有限公司')
            # 获取经理人公司详情页count
            Managers_count = self.new_find_element(By.XPATH, self.ELEMENT['Managers_count']).text
            Managers_count = int(Managers_count)
            log.info("经理人count：{}".format(Managers_count))
            # 进入经理人模块
            self.new_find_element(By.XPATH, self.ELEMENT["Managers"]).click()
            title_name = self.get_elemengt_text(self.ELEMENT['title_name'])
            log.info("页面title：{}".format(title_name))
            self.assertEqual("经理人", title_name, msg="页面title不对应")
            # 获取经理人列表页count
            Managers_count1 = self.all_count_compute_v1(By.ID, self.ELEMENT['tv_person_name'])
            log.info("统计董监事count：{}".format(Managers_count1))
            self.assertEqual(Managers_count1, Managers_count, msg="count数不对应")
            # 到职日期
            tv_duty = self.new_find_elements(By.ID, self.ELEMENT['tv_duty'])[0].text
            log.info("到职日期：{}".format(tv_duty))
            self.assertTrue(check_time(tv_duty))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_004_taiwan_fgs_p0(self):
        """
        台湾企业-企业背景-分公司
        """
        log.info(self.test_004_taiwan_fgs_p0.__doc__)
        try:
            self.enter_official_information('明日世界电脑股份有限公司')
            # 获取分公司 公司详情页count
            branch_count = self.new_find_element(By.XPATH, self.ELEMENT['branch_count']).text
            branch_count = int(branch_count)
            log.info("经理人count：{}".format(branch_count))
            # 进入分公司模块
            self.new_find_element(By.XPATH, self.ELEMENT["branch"]).click()
            title_name = self.get_elemengt_text(self.ELEMENT['title_name'])
            log.info("页面title：{}".format(title_name))
            self.assertEqual("分公司", title_name, msg="页面title不对应")
            # 代表人
            tv_item_content_block_1_1 = self.new_find_elements(By.ID, self.ELEMENT['tv_item_content_block_1_1'])[1].text
            log.info("代表人：{}".format(tv_item_content_block_1_1))
            # 统一编号
            tv_item_content_block_1_2 = self.new_find_elements(By.ID, self.ELEMENT['tv_item_content_block_1_2'])[1].text
            log.info("统一编号：{}".format(tv_item_content_block_1_2))
            # 核准设立日期
            tv_item_content_block_2_1 = self.new_find_elements(By.ID, self.ELEMENT['tv_item_content_block_2_1'])[1].text
            log.info("核准设立日期：{}".format(tv_item_content_block_2_1))
            self.assertTrue(check_time(tv_item_content_block_2_1))
            # 最后核准变更日期
            tv_item_content_block_2_2 = self.new_find_elements(By.ID, self.ELEMENT['tv_item_content_block_2_2'])[1].text
            log.info("最后核准变更日期：{}".format(tv_item_content_block_2_2))
            self.assertTrue(check_time(tv_item_content_block_2_2))
            # 公司状态
            tv_status = self.new_find_elements(By.ID, self.ELEMENT['tv_status'])[1].text
            log.info("公司状态：{}".format(tv_status))
            # 公司详情页跳转
            company = self.new_find_elements(By.ID, self.ELEMENT['tv_item_header'])[1]
            companyname = company.text
            log.info("分公司页面-公司名称：{}".format(companyname))
            company.click()
            # 公司详情页-公司名称
            companyname1 = self.new_find_element(By.ID, self.ELEMENT['firm_detail_name_tv']).text
            log.info("公司详情页-公司名称：{}".format(companyname1))
            self.assertEqual(companyname1, companyname)
            self.driver.keyevent(4)
            # 分公司详情页count数统计
            branch_count1 = self.data_list_count(By.ID, self.ELEMENT['tv_item_content_block_1_2'])
            log.info("分公司详情页count数统计：{}".format(branch_count1))
            self.assertEqual(branch_count1, branch_count, msg="count数不对应")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_005_taiwan_dwtz_p0(self):
        """
        台湾企业-企业背景-对外投资
        """
        log.info(self.test_005_taiwan_dwtz_p0.__doc__)
        try:
            self.enter_official_information('怡安医疗器材股份有限公司')
            # 获取对外投资 公司详情页count
            foreign_investment_count = self.new_find_element(By.XPATH, self.ELEMENT['foreign_investment_count']).text
            foreign_investment_count = int(foreign_investment_count)
            log.info("对外投资count：{}".format(foreign_investment_count))
            # 进入对外投资模块
            self.new_find_element(By.XPATH, self.ELEMENT["foreign_investment"]).click()
            title_name = self.get_elemengt_text(self.ELEMENT['title_name'])
            log.info("页面title：{}".format(title_name))
            self.assertEqual("对外投资", title_name, msg="页面title不对应")
            # 对外投资 公司/公司跳转
            comp = self.new_find_elements(By.ID, self.ELEMENT['outinvest_company_name_tv'])
            comp_name = comp[0].text # 公司名称
            log.info('对外投资公司:{}'.format(comp_name))
            comp[0].click() # 进入公司详情页
            self.driver.keyevent(4) # 公司详情页回退到对外投资页
            # 法定代表人/人详情跳转
            outinvest_legal_tv = self.new_find_elements(By.ID, self.ELEMENT['outinvest_company_name_tv'])
            outinvest_legal_tv1 = outinvest_legal_tv[0].text
            log.info("法定代表人:{}".format(outinvest_legal_tv1))
            outinvest_legal_tv[0].click() # 进入人详情
            self.driver.keyevent(4)  # 人详情页回退到对外投资页
            # 经营状态
            outinvest_reg_capital_tv = self.new_find_elements(By.ID, self.ELEMENT['outinvest_reg_capital_tv'])
            outinvest_reg_capital_tv1 = outinvest_reg_capital_tv[0].text
            log.info("经营状态:{}".format(outinvest_reg_capital_tv1))
            self.assertTrue(operating_check(1, outinvest_reg_capital_tv1))
            # 投资数额
            tv_outinvest_amount = self.new_find_elements(By.ID, self.ELEMENT['tv_outinvest_amount'])
            tv_outinvest_amount1 = tv_outinvest_amount[0].text
            log.info("投资数额:{}".format(tv_outinvest_amount1))
            self.assertTrue(is_bill_available(tv_outinvest_amount1))
            # 投资比例
            tv_outinvest_ratio = self.new_find_elements(By.ID, self.ELEMENT['tv_outinvest_ratio'])
            tv_outinvest_ratio1 = tv_outinvest_ratio[0].text
            log.info("注册比例:{}".format(tv_outinvest_ratio1))
            self.assertTrue(is_percentage_available(tv_outinvest_ratio1))
            # 成立日期
            tv_outinverst_date = self.new_find_elements(By.ID, self.ELEMENT['tv_outinverst_date'])
            tv_outinverst_date1 = tv_outinverst_date[0].text
            log.info("成立日期:{}".format(tv_outinverst_date1))
            # 股权结构
            tv_outinvest_title_right = self.new_find_elements(By.ID, self.ELEMENT['tv_outinvest_title_right'])
            tv_outinvest_title_right[0].click()

            account = Account()
            acc_vip_name = account.get_account('vip')
            acc_pwd = account.get_pwd()
            log.info("登录VIP账号：{},密码为:{}".format(acc_vip_name, acc_pwd))
            self.login(acc_vip_name, acc_pwd)
            title_name = self.get_elemengt_text(self.ELEMENT['title_name'])
            log.info("页面title：{}".format(title_name))
            self.assertEqual("股权结构", title_name, msg="页面title不对应")
            self.driver.keyevent(4)
            # 对外投资列表页count统计
            foreign_investment_count1 = self.all_count_compute_v1(By.ID, self.ELEMENT['outinvest_company_name_tv'])
            self.assertEqual(foreign_investment_count1, foreign_investment_count)
            account.release_account(acc_vip_name, "vip")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == '__main__':
    unittest.main()

# @getimage
# def test_003_taiwan_jlr_p0(self):
#     """
#     台湾企业-企业背景-经理人
#     """
#     log.info(self.test_003_taiwan_jlr_p0.__doc__)
#     try:
#
#     except AssertionError:
#         raise self.failureException()
#     except Exception as e:
#         log.error(error_format(e))
#         raise Exception







