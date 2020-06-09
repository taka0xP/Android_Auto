# -*- coding: utf-8 -*-
# @Time    : 2020-03-17 16:39
# @Author  : XU
# @File    : test_company_detail_basic_module_02.py
# @Software: PyCharm

from common.operation import Operation, getimage
from Providers.sift.sift_opera import SiftOperation
import unittest
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger, error_format
from Providers.account.account import Account
import random

log = Logger("公司详情页-天眼风险").getlog()


class Company_detail_baseinfo(MyTest, Operation):
    """公司详情页_天眼风险"""

    a = Read_Ex()
    ELEMENT = a.read_excel("company_detail_xu")
    account = Account()
    account.init_account()
    phone_vip = account.get_account("vip")
    contents = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sift_opera = SiftOperation(cls.driver, cls.ELEMENT)

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.phone_vip, 'vip')
        super().tearDownClass()

    def get_content(self, risk_detail_list, number):
        self.contents = []
        if risk_detail_list == 1:
            risk_detail_list = 2
        for i in range(number):
            content = self.new_find_element(
                By.XPATH,
                self.ELEMENT['riskinfo_item_detail_list'] +
                '[' +
                str(
                    risk_detail_list -
                    1) +
                ']//*[@resource-id="com.tianyancha.skyeye:id/tv_item_content' +
                str(i + 1) +
                '"]').text
            self.contents.append(content)

    def riskinfo_detail_list(self, dimension, tag=None, swip=None):
        ele_risk_item1 = '//*[@class="android.widget.TextView" and @text="' + \
            dimension + '"]/../../following-sibling::android.widget.LinearLayout[1]'
        while True:
            if self.isElementExist(By.XPATH, ele_risk_item1):
                self.new_find_element(By.XPATH, ele_risk_item1).click()
                if tag == 1:
                    for i in range(random.randint(1, 3)):
                        self.swipeUp()
                    risk_detail_list = len(
                        self.new_find_elements(
                            By.XPATH,
                            self.ELEMENT['riskinfo_item_detail_list']))
                    return risk_detail_list
                break
            else:
                if swip == "down":
                    self.swipeDown(0.5, 0.3, 0.7, t=2000)
                else:
                    self.swipeUp(0.5, 0.7, 0.3, t=2000)

    @getimage
    def test_001_gsxx_tyfx_p0(self):
        """公司基本信息-天眼风险，登录态校验"""
        log.info(self.test_001_gsxx_tyfx_p0.__doc__)
        try:
            self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
            self.sift_opera.into_company(company="乐视控股（北京）有限公司")
            self.new_find_element(
                By.XPATH, self.ELEMENT['rv_riskinfo_item1']).click()
            self.assertEqual(
                "乐视控股（北京）有限公司",
                self.new_find_element(
                    By.ID,
                    self.ELEMENT['tv_companyname']).text,
                "===天眼风险详情页，关联公司名称错误===")

            log.info("天眼风险-失信被执行人")
            risk_detail_list = self.riskinfo_detail_list("失信被执行人", 1)
            self.get_content(risk_detail_list, 5)
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            self.swipeUp(0.5, 0.55, 0.45, t=500)
            detail_gistid = self.new_find_element(
                By.ID, self.ELEMENT['dishonest_detail_gistid_tv']).text
            detail_courtname = self.new_find_element(
                By.ID, self.ELEMENT['dishonest_detail_courtname_tv']).text
            detail_performance = self.new_find_element(
                By.ID, self.ELEMENT['dishonest_detail_performance_tv']).text
            detail_regdate = self.new_find_element(
                By.ID, self.ELEMENT['dishonest_detail_regdate_tv']).text
            detail_publishdate = self.new_find_element(
                By.ID, self.ELEMENT['dishonest_detail_publishdate_tv']).text
            self.assertEqual(
                self.contents[0],
                detail_gistid,
                "===天眼风险，失信被执行人，详情页「案号」错误===")
            self.assertEqual(
                self.contents[1],
                detail_courtname,
                "===天眼风险，失信被执行人，详情页「执行法院」错误===")
            self.assertEqual(
                self.contents[2],
                detail_performance,
                "===天眼风险，失信被执行人，详情页「履行情况」错误===")
            self.assertEqual(
                self.contents[3],
                detail_regdate,
                "===天眼风险，失信被执行人，详情页「立案日期」错误===")
            self.assertEqual(
                self.contents[4],
                detail_publishdate,
                "===天眼风险，失信被执行人，详情页「发布日期」错误===")
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-限制消费令")
            risk_detail_list = self.riskinfo_detail_list("限制消费令", 1)
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            # todo pdf页校验
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-被执行人")
            risk_detail_list = self.riskinfo_detail_list("被执行人", 1)
            self.get_content(risk_detail_list, 4)
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            casecode = self.new_find_element(
                By.ID, self.ELEMENT['tv_executed_person_detial_casecode']).text
            court_name = self.new_find_element(
                By.ID, self.ELEMENT['tv_executed_person_detial_exec_court_name']).text
            money = self.new_find_element(
                By.ID, self.ELEMENT['tv_executed_person_detial_exec_money']).text
            create_time = self.new_find_element(
                By.ID, self.ELEMENT['executed_person_detial_case_create_time']).text
            self.assertEqual(
                self.contents[0],
                casecode,
                "===天眼风险，被执行人，详情页「案号」错误===")
            self.assertEqual(
                self.contents[1],
                court_name,
                "===天眼风险，被执行人，详情页「执行法院」错误===")
            self.assertEqual(
                self.contents[2],
                money,
                "===天眼风险，被执行人，详情页「执行标的」错误===")
            self.assertEqual(
                self.contents[3],
                create_time,
                "===天眼风险，被执行人，详情页「立案日期」错误===")
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-终本案件")
            risk_detail_list = self.riskinfo_detail_list("终本案件", 1)
            self.get_content(risk_detail_list, 3)
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            tv_name = self.new_find_element(
                By.ID, self.ELEMENT['tv_name']).text
            tv_case_code = self.new_find_element(
                By.ID, self.ELEMENT['tv_case_code']).text
            tv_create_date = self.new_find_element(
                By.ID, self.ELEMENT['tv_create_date']).text
            self.assertEqual(
                self.contents[0],
                tv_name,
                "===天眼风险，终本案件，详情页「姓名」错误===")
            self.assertEqual(
                self.contents[1],
                tv_case_code,
                "===天眼风险，终本案件，详情页「案号」错误===")
            self.assertEqual(
                self.contents[2],
                tv_create_date,
                "===天眼风险，终本案件，详情页「立案时间」错误===")
            # todo 终本案件，「关联失信被执行人」「关联被执行人」校验
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-经营异常")
            self.riskinfo_detail_list("经营异常")
            self.assertEqual(
                "乐视控股（北京）有限公司", self.new_find_element(
                    By.ID, self.ELEMENT['company_name_tv']).text)
            # todo 字段校验
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-司法协助")
            risk_detail_list = self.riskinfo_detail_list("司法协助", 1)
            self.get_content(risk_detail_list, 4)
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            if self.contents[3] == "股权冻结|失效":
                sfxz_detail_tv1 = self.new_find_element(
                    By.ID, self.ELEMENT['sfxz_detail_tv1']).text
                sfxz_detail_tv2 = self.new_find_element(
                    By.ID, self.ELEMENT['sfxz_detail_tv2']).text
                sfxz_detail_tv3 = self.new_find_element(
                    By.ID, self.ELEMENT['sfxz_detail_tv3']).text
                sfxz_detail_tv4 = self.new_find_element(
                    By.ID, self.ELEMENT['sfxz_detail_tv4']).text
                self.assertEqual(
                    self.contents[0],
                    sfxz_detail_tv2,
                    "===天眼风险，司法协助，详情页「被执行人」错误===")
                self.assertEqual(
                    self.contents[1],
                    sfxz_detail_tv3,
                    "===天眼风险，司法协助，详情页「股权数额」错误===")
                self.assertEqual(
                    self.contents[2],
                    sfxz_detail_tv1,
                    "===天眼风险，司法协助，详情页「执行通知书文号」错误===")
                self.assertEqual(
                    self.contents[3],
                    sfxz_detail_tv4,
                    "===天眼风险，司法协助，详情页「类型|状态」错误===")
            else:
                sfxz_detail_tv3 = self.new_find_element(
                    By.ID, self.ELEMENT['sfxz_detail_tv3']).text
                sfxz_detail_tv6 = self.new_find_element(
                    By.ID, self.ELEMENT['sfxz_detail_tv6']).text
                sfxz_detail_tv8 = self.new_find_element(
                    By.ID, self.ELEMENT['sfxz_detail_tv8']).text
                self.assertEqual(
                    self.contents[0],
                    sfxz_detail_tv6,
                    "===天眼风险，司法协助，详情页「被执行人」错误===")
                self.assertEqual(
                    self.contents[1],
                    sfxz_detail_tv8,
                    "===天眼风险，司法协助，详情页「股权数额」错误===")
                self.assertEqual(
                    self.contents[2],
                    sfxz_detail_tv3,
                    "===天眼风险，司法协助，详情页「执行通知书文号」错误===")
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-开庭公告")
            risk_detail_list = self.riskinfo_detail_list("开庭公告", 1)
            self.get_content(risk_detail_list, 4)
            ktgg_header = self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']' + self.ELEMENT['ktgg_list_header']).text
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            ann_case_reason = self.new_find_element(
                By.ID, self.ELEMENT['ann_case_reason']).text
            ann_case_num = self.new_find_element(
                By.ID, self.ELEMENT['ann_case_num']).text
            ann_law_date = self.new_find_element(
                By.ID, self.ELEMENT['ann_law_date']).text
            self.assertEqual(
                ktgg_header,
                ann_case_reason,
                "===天眼风险，开庭公告，详情页「案由」错误===")
            self.assertEqual(
                self.contents[0],
                ann_case_num,
                "===天眼风险，开庭公告，详情页「案号」错误===")
            self.assertEqual(
                self.contents[3],
                ann_law_date,
                "===天眼风险，开庭公告，详情页「开庭时间」错误===")
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼服务-法律诉讼")
            risk_detail_list = self.riskinfo_detail_list("法律诉讼", 1)
            self.get_content(risk_detail_list, 4)
            flss_header = self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']' + self.ELEMENT['ktgg_list_header']).text
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            flss_detail = self.new_find_element(
                By.XPATH, self.ELEMENT['flss_detail']).text
            self.assertIn(
                flss_header,
                flss_detail,
                "===天眼风险，法律诉讼，详情页「案件名称」错误===")
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-司法拍卖")
            self.new_find_element(
                By.ID, self.ELEMENT['riskinfo_title_2']).click()
            risk_detail_list = self.riskinfo_detail_list(
                "司法拍卖", 1, swip="down")
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            self.assertTrue(
                self.isElementExist(
                    By.XPATH,
                    self.ELEMENT['bid_sale_wv']),
                "===司法拍卖-Webview展示失败===")
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-立案信息")
            risk_detail_list = self.riskinfo_detail_list(
                "立案信息", 1, swip="down")
            self.get_content(risk_detail_list, 2)
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            tv_court_num = self.new_find_element(
                By.ID, self.ELEMENT['tv_court_num']).text
            tv_filing_date = self.new_find_element(
                By.ID, self.ELEMENT['tv_filing_date']).text
            self.assertEqual(
                self.contents[0],
                tv_court_num,
                "===天眼风险，立案信息，详情页「案号」错误===")
            self.assertEqual(
                self.contents[1],
                tv_filing_date,
                "===天眼风险，立案信息，详情页「立案日期」错误===")
            while not self.isElementExist(
                    By.ID, self.ELEMENT['tv_companyname']):
                self.driver.keyevent(4)

            log.info("天眼风险-法院公告")
            risk_detail_list = self.riskinfo_detail_list(
                "法院公告", 1, swip="down")
            self.get_content(risk_detail_list, 4)
            self.new_find_element(
                By.XPATH, self.ELEMENT['riskinfo_item_detail_list'] + '[' + str(
                    risk_detail_list - 1) + ']/android.widget.ImageView').click()
            tv_court_item_court = self.new_find_element(
                By.ID, self.ELEMENT['tv_court_item_court']).text
            tv_court_item_st = self.new_find_element(
                By.ID, self.ELEMENT['tv_court_item_st']).text
            tv_court_item_tm = self.new_find_element(
                By.ID, self.ELEMENT['tv_court_item_tm']).text
            self.assertEqual(
                self.contents[1],
                tv_court_item_court,
                "===天眼风险，法院公告，详情页「公告人」错误===")
            self.assertEqual(
                self.contents[2],
                tv_court_item_st,
                "===天眼风险，法院公告，详情页「公告类型」错误===")
            self.assertEqual(
                self.contents[3],
                tv_court_item_tm,
                "===天眼风险，法院公告，详情页「刊登日期」错误===")
            court_sued_len = len(
                self.new_find_elements(
                    By.XPATH,
                    self.ELEMENT['ll_court_sued']))
            for i in range(court_sued_len):
                item = self.new_find_element(
                    By.XPATH, self.ELEMENT['ll_court_sued'] + '[' + str(
                        i + 1) + ']/android.widget.TextView').text
                self.assertIn(
                    item,
                    self.contents[0],
                    "===天眼风险，法院公告，详情页「当事人」错误===")

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))


if __name__ == "__main__":
    unittest.main()
