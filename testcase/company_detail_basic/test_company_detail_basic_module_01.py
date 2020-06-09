# -*- coding: utf-8 -*-
# @Time    : 2020-03-06 13:42
# @Author  : XU
# @File    : test_company_detail_basic_module_01.py
# @Software: PyCharm

from common.operation import Operation, getimage
from Providers.sift.sift_opera import SiftOperation
from common.CreditIdentifier import UnifiedSocialCreditIdentifier
import unittest
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger, error_format
from Providers.account.account import Account

log = Logger("公司详情页-基本信息").getlog()
msg = {"开业": "企业依法存在并继续正常运营。",
       "在业": "企业正常开工生产、新建企业、包括部分投产或试营业。",
       "存续": "企业依法存在并继续正常运营。",
       "吊销": "吊销企业营业执照，是工商局对违法企业作出的行政处罚。",
       "吊销，已注销": "企业被吊销营业执照后，办理企业的注销登记手续。",
       "吊销，未注销": "企业被吊销营业执照实质上是被剥夺企业的经营资格，而其主体资格依然存在。",
       "注销": "企业已依法注销营业执照，丧失法人资格。",
       "迁出": "该企业的注册地址已经变更，并且在工商局办理了企业注册地址变更。",
       "废止": "该企业已被依法废止。",
       "核准设立": "该企业已被核准设立。"}


class Company_detail_baseinfo(MyTest, Operation):
    """公司详情页_基本信息"""

    a = Read_Ex()
    ELEMENT = a.read_excel("company_detail_xu")
    account = Account()
    phone_vip = account.get_account("vip")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sift_opera = SiftOperation(cls.driver, cls.ELEMENT)

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.phone_vip, 'vip')
        super().tearDownClass()

    @getimage
    def test_gsxx_jcxx_001_p0(self):
        """企业状态标签"""
        log.info(self.test_gsxx_jcxx_001_p0.__doc__)
        company_name = self.sift_opera.into_company()
        tag = self.new_find_element(By.XPATH, self.ELEMENT["tag_firm_1"])
        tag_text = tag.text
        log.info("===企业状态：「{}」===".format(tag_text))
        tag.click()
        txt_msg = self.new_find_element(By.ID, self.ELEMENT["txt_msg"]).text
        self.assertIn(msg[tag_text], txt_msg, "==={}，标签错误「{}」===".format(company_name, tag_text))
        self.new_find_element(By.ID, self.ELEMENT["delete_confirm"]).click()

    @getimage
    def test_gsxx_jcxx_002_p0(self):
        """发票抬头标签"""
        log.info(self.test_gsxx_jcxx_002_p0.__doc__)
        company_name = self.sift_opera.into_company()
        self.new_find_element(By.XPATH, self.ELEMENT["bill_title"]).click()
        title = self.new_find_element(By.ID, self.ELEMENT["txt_title"]).text
        self.assertEqual("发票抬头", title, "===失败-「发票抬头」弹窗===")
        name = self.new_find_element(By.ID, self.ELEMENT["txt_name"]).text
        tax = self.new_find_element(By.ID, self.ELEMENT["txt_tax"]).text
        tax_check = UnifiedSocialCreditIdentifier()
        if tax != "-":
            tax_check.check_tax_code(tax)
        phone = self.new_find_element(By.ID, self.ELEMENT["txt_phone"]).text
        address = self.new_find_element(By.ID, self.ELEMENT["txt_address"]).text
        log.info("发票抬头信息：「名称：{}」「税号：{}」「电话：{}」「地址：{}」".format(name, tax, phone, address))
        self.new_find_element(By.ID, self.ELEMENT["delte_cancel"]).click()
        self.assertFalse(self.isElementExist(By.ID, self.ELEMENT["txt_title"]))
        self.new_find_element(By.XPATH, self.ELEMENT["bill_title"]).click()
        self.new_find_element(By.ID, self.ELEMENT["delete_confirm"]).click()
        bottom2 = self.isElementExist(By.ID, self.ELEMENT["login_bottom2"])
        self.assertTrue(bottom2, "===保存发票，登陆校验失败===")
        self.new_find_element(By.XPATH, self.ELEMENT["passwd_login"]).click()
        self.new_find_element(By.ID, self.ELEMENT["et_phone"]).send_keys(self.phone_vip)
        self.new_find_element(By.ID, self.ELEMENT["input_password"]).send_keys(self.account.get_pwd())
        # 判断隐私弹窗是否勾选
        a = self.new_find_element(By.ID, self.ELEMENT["cb_login_check"]).get_attribute("checked")
        if a != "true":
            self.new_find_element(By.ID, self.ELEMENT["cb_login_check"]).click()
        self.new_find_element(By.ID, self.ELEMENT["tv_login"]).click()
        # 判断日报弹窗
        if self.new_find_element(By.XPATH, self.ELEMENT["monitor_pop"]):
            self.new_find_element(By.ID, self.ELEMENT["btn_finish"]).click()
        self.new_find_element(By.XPATH, self.ELEMENT["bill_title"]).click()
        self.new_find_element(By.ID, self.ELEMENT["delete_confirm"]).click()
        for i in range(10):
            if self.isElementExist(By.ID, self.ELEMENT["tab_iv_5"]):
                self.new_find_element(By.ID, self.ELEMENT["tab_iv_5"]).click()
                break
            else:
                self.driver.keyevent(4)
        self.new_find_element(By.XPATH, self.ELEMENT["bill_title"]).click()
        bill_title = self.new_find_element(By.XPATH, self.ELEMENT["bill_title_list_1"]).text
        self.assertEqual(company_name, bill_title)

    @getimage
    def test_gsxx_jcxx_003_p0(self):
        """融资轮次标签"""
        log.info(self.test_gsxx_jcxx_003_p0.__doc__)
        self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
        self.new_find_element(By.ID, self.ELEMENT["search_company"]).click()
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
        self.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).send_keys("北京百度网讯科技有限公司")
        self.new_find_element(By.XPATH, self.ELEMENT['company_rzlc']).click()
        if self.new_find_element(By.XPATH, self.ELEMENT["tag_firm_2"]).text == "发票抬头":
            round_tag = self.new_find_element(By.XPATH, self.ELEMENT["tag_firm_3"]).text
            self.new_find_element(By.XPATH, self.ELEMENT["tag_firm_3"]).click()
            round_name = self.new_find_element(By.ID, self.ELEMENT["txt_round"]).text
            round_date = self.new_find_element(By.ID, self.ELEMENT["txt_date"]).text
            round_money = self.new_find_element(By.ID, self.ELEMENT["txt_money"]).text
            round_valuation = self.new_find_element(By.ID, self.ELEMENT["txt_valuation"]).text
            self.assertEqual(round_tag, round_name, "===当前融资轮次错误===")
            self.new_find_element(By.ID, self.ELEMENT["delete_confirm"]).click()

            for i in range(20):
                if self.isElementExist(By.XPATH, '//*[@class="android.widget.TextView" and @text="融资历程"]'):
                    self.new_find_element(By.XPATH, '//*[@class="android.widget.TextView" and @text="融资历程"]').click()
                    round_ = self.new_find_element(By.XPATH, self.ELEMENT["detail_txt_round"]).text
                    date_ = self.new_find_element(By.XPATH, self.ELEMENT["detail_txt_date"]).text
                    money_ = self.new_find_element(By.XPATH, self.ELEMENT["detail_txt_money"]).text
                    valuation_ = self.new_find_element(By.XPATH, self.ELEMENT["detail_txt_valuation"]).text
                    self.assertEqual(round_name, round_)
                    self.assertEqual(round_date, date_)
                    self.assertIn(round_money, money_)
                    self.assertIn(round_valuation, valuation_)
                    break
                else:
                    self.swipeUp(0.5, 0.85, 0.15, 2500)

    @getimage
    def test_gsxx_jcxx_004_p0(self):
        """高新技术企业标签"""
        log.info(self.test_gsxx_jcxx_004_p0.__doc__)
        try:
            self.sift_opera.into_company(company="北京金堤科技有限公司")
            # 对logo进行校验
            portrait = self.isElementExist(By.XPATH, self.ELEMENT["iv_portrait_img"])
            self.assertTrue(portrait, "===公司logo未展示===")
            self.new_find_element(By.XPATH, self.ELEMENT["iv_portrait_img"]).click()
            logo = self.isElementExist(By.ID, self.ELEMENT["preview_photo_root"])
            self.assertTrue(logo, "===点击logo，放大查看失败===")
            if logo:
                self.driver.keyevent(4)
            self.new_find_element(By.XPATH, self.ELEMENT["tag_firm_4"]).click()
            txt_msg = self.new_find_element(By.ID, self.ELEMENT["txt_msg"]).text
            self.assertIn("高新技术企业", txt_msg, "===「高新技术企业」标签，弹窗文案错误==")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_gsxx_jcxx_005_p0(self):
        """小微企业标签"""
        log.info(self.test_gsxx_jcxx_005_p0.__doc__)
        try:
            self.sift_opera.into_company(company="盐城金堤科技有限公司")
            self.new_find_element(By.XPATH, self.ELEMENT["tag_firm_3"]).click()
            txt_msg = self.new_find_element(By.ID, self.ELEMENT["txt_msg"]).text
            self.assertIn("小型微型企业", txt_msg, "===「小微企业」标签，弹窗文案错误==")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_gsxx_jcxx_006_p0(self):
        """公司logo"""
        log.info(self.test_gsxx_jcxx_006_p0.__doc__)
        try:
            self.sift_opera.into_company(company="阜新高新技术建设开发有限责任公司")
            portrait = self.new_find_element(By.XPATH, self.ELEMENT["iv_portrait_text"]).text
            self.assertEqual("高新\n技术", portrait, "===无公司logo，展示4个字文案失败===")
            while True:
                if self.isElementExist(By.ID, self.ELEMENT["search_input_edit"]):
                    self.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).send_keys("贵安新区东旗高新技术有限公司")
                    self.new_find_element(By.XPATH,
                                          '//*[@class="android.widget.TextView" and @text="贵安新区东旗高新技术有限公司"]').click()
                    iv_portrait = self.new_find_element(By.XPATH, self.ELEMENT["iv_portrait_text"]).text
                    self.assertEqual("东旗", iv_portrait, "===无公司logo，展示2个字文案失败===")
                    break
                else:
                    self.driver.keyevent(4)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
