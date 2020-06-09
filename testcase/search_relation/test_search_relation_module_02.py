# -*- coding: utf-8 -*-
# @Time    : 2019-11-19 16:45
# @Author  : XU
# @File    : Search_relationTest.py
# @Software: PyCharm

from common.operation import Operation, getimage
import unittest
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger, error_format
from Providers.sift.sift_opera import SiftOperation
from Providers.account.account import Account

log = Logger("查关系_02").getlog()


class Search_relationTest(MyTest, Operation):
    """查关系_02"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_relation")
    account = Account()
    phone_vip = account.get_account("vip")
    phone_normal = account.get_account()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sift_opera = SiftOperation(cls.driver, cls.ELEMENT)

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.phone_vip, "vip")
        cls.account.release_account(cls.phone_normal)
        super().tearDownClass()

    def check_vip_normal(self, index=None):
        """
        校验非vip态、登陆态
        :param index: 1:未登陆态; 2:非VIP
        :return:
        """
        Key = ["passwd_login", "tv_top_title"]
        Value = ["passwd_login_text", "tv_top_title_text"]
        self.sift_opera.search_key(2)
        self.new_find_element(By.ID, self.ELEMENT["select_more"]).click()
        result1 = self.ELEMENT["open_vip_ll_text"] == self.new_find_element(By.ID, self.ELEMENT["open_vip_ll"]).text
        self.new_find_element(By.ID, self.ELEMENT["open_vip_ll"]).click()
        if index == 1:
            log.info("校验-未登陆态")
            result2 = self.ELEMENT[Value[index - 1]] == self.new_find_element(By.XPATH, self.ELEMENT[Key[index - 1]]).text
        else:
            log.info("校验-非VIP")
            result2 = self.ELEMENT[Value[index - 1]] == self.new_find_element(By.ID, self.ELEMENT[Key[index - 1]]).text
        self.driver.keyevent(4)
        selectTarget, selectText = self.sift_opera.get_key("more_ssfw_title", "more_ssfw", 1)
        if index == 1:
            result3 = self.isElementExist(By.XPATH, self.ELEMENT[Key[index - 1]])
        else:
            result3 = self.isElementExist(By.XPATH, self.ELEMENT[Key[index - 1]])
        self.sift_opera.reset(selectTarget)
        self.sift_opera.get_key("more_lxfs_title", "more_lxfs", 1)
        if index == 1:
            passwd_login = self.new_find_element(By.XPATH, self.ELEMENT["passwd_login"]).text
            result4 = self.ELEMENT["passwd_login_text"] == passwd_login
            self.new_find_element(By.ID, self.ELEMENT["title_back"]).click()
        else:
            middle_title = self.new_find_element(By.ID, self.ELEMENT["tv_middle_title"]).text
            result4 = self.ELEMENT["tv_middle_title_text"] == middle_title
            self.driver.keyevent(4)
        back_max = 30
        back_cnt = 0
        while not self.isElementExist(By.ID, self.ELEMENT["search_relation"]):
            self.driver.keyevent(4)
            back_cnt += 1
            if back_cnt > back_max:
                break
        return result1, result2, result3, result4

    def rel_detail(self):
        self.sift_opera.search_key(2)
        result1 = self.isElementExist(By.ID, self.ELEMENT["select_more"])
        self.new_find_element(By.ID, self.ELEMENT["select_more"]).click()
        result2 = self.isElementExist(By.ID, self.ELEMENT["open_vip_ll"])
        result3 = self.isElementExist(By.ID, self.ELEMENT["bt_reset"])
        self.new_find_element(By.ID, self.ELEMENT["select_more"]).click()
        t_xpath = "{}/android.widget.RelativeLayout/android.widget.TextView".format(self.ELEMENT["from_target_item"])
        company_name = self.new_find_element(By.XPATH, t_xpath).text
        self.new_find_element(By.XPATH, self.ELEMENT["from_target_item"]).click()
        title_tag = self.new_find_element(By.ID, self.ELEMENT["app_title_name"]).text
        result4 = title_tag == "企业详情"
        d_xpath = "{}/android.widget.TextView".format(self.ELEMENT["lv_firm_detail"])
        tarName = self.new_find_element(By.XPATH, d_xpath).text
        result5 = tarName == company_name
        f_xpath = "{}/android.widget.ImageView".format(self.ELEMENT["lv_firm_detail"])
        self.new_find_element(By.XPATH, f_xpath).click()
        s_xpath = "{}/android.widget.RelativeLayout/android.widget.TextView".format(self.ELEMENT["sky_canvas"])
        comName = self.new_find_element(By.XPATH, s_xpath).text
        result6 = comName == company_name
        back_max = 30
        back_cnt = 0
        while not self.isElementExist(By.ID, self.ELEMENT["search_relation"]):
            self.driver.keyevent(4)
            back_cnt += 1
            if back_cnt > back_max:
                break
        return result1, result2, result3, result4, result5, result6

    @getimage
    def test_001_cgx_vip_p0(self):
        """未登陆、非VIP校验"""
        log.info(self.test_001_cgx_vip_p0.__doc__)
        try:
            result1, result2, result3, result4 = self.check_vip_normal(1)
            # 断言 - 更多筛选下拉框，展示vip入口
            self.assertTrue(result1, "===失败-获取更多筛选下拉框vip入口失败===")
            # 断言 - 更多筛选下拉框，点击vip入口
            self.assertTrue(result2, "===失败-未登陆态，更多筛选下拉框vip入口，拉起登陆页失败===")
            # 断言 - 更多筛选下拉框，点击普通筛选项
            self.assertFalse(result3, "===失败-未登陆态，更多筛选下拉框非vip筛选项错误拉起登陆===")
            # 断言 - 更多筛选下拉框，点击高级筛选项
            self.assertTrue(result4, "===失败-拉起登陆页失败===")
            # 判断非vip
            self.sift_opera.login_normal(self.phone_normal, self.account.get_pwd())
            result1, result2, result3, result4 = self.check_vip_normal(2)
            # 断言 - 更多筛选下拉框，点击vip入口
            self.assertTrue(result2, "===失败-非vip，更多筛选下拉框vip入口，拉起登陆页失败===")
            # 断言 - 更多筛选下拉框，点击普通筛选项
            self.assertFalse(result3, "===失败-非vip，更多筛选下拉框非vip筛选项，错误限制===")
            # 断言 - 更多筛选下拉框，点击高级筛选项
            self.assertTrue(result4, "===失败-弹出vip弹窗失败===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_xqy_p0(self):
        """查关系-搜索结果页，公司详情"""
        log.info(self.test_002_cgx_xqy_p0.__doc__)
        try:
            self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
            result1, result2, result3, result4, result5, result6 = self.rel_detail()
            # 断言-输入关键词，展示更多筛选按钮
            self.assertTrue(result1, "===失败-更多筛选按钮未展示===")
            # 断言-更多筛选下拉展示
            self.assertFalse(result2, "===失败-vip用户，高级筛选下拉框未隐藏vip入口===")
            self.assertTrue(result3, "===失败-更多筛选下拉展示失败===")
            # 断言-查关系搜索列表，进入企业详情
            self.assertTrue(result4, "===失败-进入查关系-企业详情选取节点页错误===")
            self.assertTrue(result5, "===失败-查关系公司详情页，公司名错误===")
            # # 断言-通过查关系企业详情页，获取关系图节点
            self.assertTrue(result6, "===失败-通过查关系公司详情页，获取节点失败===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
