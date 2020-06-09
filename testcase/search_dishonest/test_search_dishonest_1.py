#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/21
# @Author  : Soner
# @version : 1.0.0

from common.MyTest import MyTest
from common.ReadData import Read_Ex
from common.operation import Operation
from common.operation import getimage
from selenium.webdriver.common.by import By
from Providers.logger import Logger, error_format
from Providers.dishonest.dishonest_fun import Dishonest
from Providers.back_to_index import back_to_index
from Providers.company.company import CompanyFunc
import time
import unittest

log = Logger("查老赖_01").getlog()


class TestSearchDisHonest1(MyTest):
    "查老赖_01"
    a = Read_Ex()
    ELEMENT = a.read_excel("search_dishonest")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dishone = Dishonest(cls.driver, cls.ELEMENT)
        cls.operation = Operation(cls.driver)
        cls.company = CompanyFunc(cls.driver, cls.ELEMENT)

    def setUp(self):
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_in_main"]
        ).click()

    @getimage
    @unittest.skip("首页只有开工红包banner")
    def test_cll_rk_0001_1(self):
        "通过点击APP首页轮播banner「查老赖」图片，可以跳转到查老赖功能页面"
        log.info(self.test_cll_rk_0002_1.__doc__)
        try:
            back_to_index(self.driver)
            self.dishone.entrance()
            search_input = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_search_input"]
            )
            assert "输入人名/公司名/身份证号码/组织机构代码" == search_input.text
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_cll_rk_0002_1(self):
        "通过点击「百宝箱」中的「查老赖」标签，可以跳转到「查老赖」功能页面"
        log.info(self.test_cll_rk_0002_1.__doc__)
        try:
            back_to_index(self.driver)
            self.operation.new_find_elements(By.ID, self.ELEMENT["all_in_main"])[
                4
            ].click()
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_in_all"]
            ).click()
            search_input = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_search_input"]
            )
            assert "输入人名/公司名/身份证号码/组织机构代码" == search_input.text
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_cll_rmss_0001_0(self):
        "「查老赖」功能首页，搜索框下展示热门搜索公司/热门人员展示2家热门搜索公司； 展示2个热门搜索人员"
        log.info(self.test_cll_rmss_0001_0.__doc__)
        try:
            hot_words = self.operation.new_find_elements(
                By.ID, self.ELEMENT["dishonest_hot_words"]
            )
            company_sum = 0
            human_sum = 0
            for idx, word in enumerate(hot_words):
                print("热搜词：%d,%s" % (idx, word.text))
                if len(word.text) > 5:
                    company_sum += 1
                else:
                    human_sum += 1
            assert company_sum == 2
            assert human_sum == 2
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_cll_rmss_0002_0(self):
        "「查老赖」搜索中间页，在没有搜索记录的时候，显示「热门搜索」"
        log.info(self.test_cll_rmss_0002_0.__doc__)
        try:
            search_input = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_search_input"]
            )
            assert "输入人名/公司名/身份证号码/组织机构代码" == search_input.text
            search_input.click()
            res = self.operation.isElementExist(
                By.ID, self.ELEMENT["dishonest_del_history"]
            )
            if res:
                self.operation.new_find_element(
                    By.ID, self.ELEMENT["dishonest_del_history"]
                ).click()
            res = self.operation.isElementExist(
                By.ID, self.ELEMENT["dishonest_del_confirm"]
            )
            # 如果「删除最近搜索按钮」存在：
            if res:
                # 判断「热门搜索」不存在
                res = self.operation.isElementExist(
                    By.ID, self.ELEMENT["dishonest_mid_hot_scope"]
                )
                assert not res
                # 清空「最近搜索记录」
                confirm_text = self.operation.new_find_element(
                    By.ID, self.ELEMENT["dishonest_del_text"]
                ).text
                print("confirm_text debug%s" % confirm_text)
                assert "确定要清空搜索记录?" == confirm_text
                self.operation.new_find_element(
                    By.ID, self.ELEMENT["dishonest_del_submit"]
                ).click()
            # 判断「删除最近搜索按钮」不存在
            res = self.operation.isElementExist(
                By.ID, self.ELEMENT["dishonest_del_history"]
            )
            assert not res
            # 判断「热门搜索」存在
            res = self.operation.isElementExist(
                By.ID, self.ELEMENT["dishonest_mid_hot_scope"]
            )
            assert res
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_cll_rmss_0003_0(self):
        "「查老赖」搜索中间页，在有搜索记录的时候，不显示「热门搜索」"
        log.info(self.test_cll_rmss_0003_0.__doc__)
        try:
            search_input = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_search_input"]
            )
            assert "输入人名/公司名/身份证号码/组织机构代码" == search_input.text
            search_input.click()
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "暴风", self.device
            )
            # 返回中间页
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_mid_clean_iv"]
            ).click()
            time.sleep(1)
            res = self.operation.isElementExist(
                By.ID, self.ELEMENT["dishonest_del_history"]
            )
            if res:
                # 判断「热门搜索」不存在
                res = self.operation.isElementExist(
                    By.ID, self.ELEMENT["dishonest_mid_hot_scope"]
                )
                assert not res
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_cll_rmss_0004_0(self):
        "「查老赖」首页的「热门搜索」词可点击，直接进入「失信记录列表」页面"
        log.info(self.test_cll_rmss_0004_0.__doc__)
        try:
            hot_element = self.operation.new_find_elements(
                By.ID, self.ELEMENT["dishonest_hot_words"]
            )[0]
            hot_word = hot_element.text
            hot_element.click()
            list_title = self.operation.new_find_element(
                By.ID, self.ELEMENT["list_title"]
            ).text
            assert "失信记录列表" == list_title
            list_name = self.operation.new_find_element(
                By.ID, self.ELEMENT["list_name"]
            ).text
            assert hot_word == list_name
            assert self.operation.isElementExist(By.ID, self.ELEMENT["list_back"])
            assert self.operation.isElementExist(By.XPATH, self.ELEMENT["list_longpic"])
            assert self.operation.isElementExist(By.XPATH, self.ELEMENT["list_share"])
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_cll_rmss_0005_0(self):
        "「搜索中间页」的「热门搜索」词可点击，直接进入「失信记录列表」页面"
        log.info(self.test_cll_rmss_0005_0.__doc__)
        try:
            self.dishone.clean_search_history()  # 清除查老赖搜索历史
            self.dishone.into_dishonest_mid()  # 进入查老赖中间页
            hotword_name = self.dishone.click_hotword_in_mid(idx=1)  # 点击第1个热搜词

            title_text = self.operation.new_find_element(
                By.ID, self.ELEMENT["list_title"]
            ).text  # 获取页面title
            self.assertEqual(title_text, "失信记录列表", "title错误")

            list_name = self.operation.new_find_element(
                By.ID, self.ELEMENT["list_name"]
            ).text  # 获取详情页的老赖名字
            self.assertEqual(hotword_name, list_name, "错误的老赖详情页")

            self.operation.new_find_element(
                By.ID, self.ELEMENT["list_back"]
            ).click()  # 点击返回按钮，回到搜索中间页
            print("返回")
            hotsearch_name = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_hot_search"]
            ).text
            self.assertEqual(hotsearch_name, "热门搜索", "当前页为有搜索记录")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0001_01_0(self):
        "通过人名搜索老赖，搜索汉字最少字符：2"
        log.info(self.test_ss_0001_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马", self.device
            )
            text = "至少输入2个字"
            toast = self.operation.get_toast()
            self.assertEqual(toast, text, "toast不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0001_02_0(self):
        "校验count数与列表数是否一致"
        log.info(self.test_ss_0001_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            count_number = self.operation.count_num(By.ID, self.ELEMENT["count_num"])
            list_number = self.operation.new_find_elements(
                By.XPATH, self.ELEMENT["list_ico"]
            )
            self.assertEqual(count_number, len(list_number) - 1, "count数与列表数不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0001_03_0(self):
        "所有iterm是否带有老赖标志"
        log.info(self.test_ss_0001_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            for i in range(2, 4):
                join_element = "{}[{}]//*{}".format(
                    self.ELEMENT["list_ico"], i, self.ELEMENT["list_deadbeat"]
                )
                text_value = self.operation.new_find_element(By.XPATH, join_element)
                self.assertEqual(text_value.text, "老赖", "标志不为老赖")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0001_04_0(self):
        "第一条是否为全量匹配结果"
        log.info(self.test_ss_0001_04_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            text_value = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_name"].format(2)
            )
            self.assertEqual(text_value.text, "司马朝", "第一条不为司马朝")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0001_05_0(self):
        "校验count数大于999，是否显示为999+"
        log.info(self.test_ss_0001_05_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "王伟", self.device
            )
            count_number = self.operation.count_num(
                By.ID, self.ELEMENT["count_num"]
            )  # 获取count数
            self.assertTrue(count_number > 999, "列表数小于999")
            tab_text = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["tab_person_count"]
            ).text
            tab_num = tab_text[-4:]
            self.assertEqual(tab_num, "999+", "count数显示错误")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0001_06_0(self):
        "身份证号码月日加密显示"
        log.info(self.test_ss_0001_06_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            text_value = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).text
            self.assertEqual(text_value, "3211811991****3234", "身份证信息不符合")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0001_07_0(self):
        "「失信自然人」tab处，显示「搜索到3个老赖」"
        log.info(self.test_ss_0001_07_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            text_value = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            ).text
            self.assertEqual(text_value, "搜索到 3 个老赖", "搜索条数不符")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0002_01_0(self):
        "「失信企业」tab后数字与列表count数一致"
        log.info(self.test_ss_0002_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            enterprise_num = self.operation.count_num(
                By.XPATH, self.ELEMENT["broken_faith_enterprise_tab"]
            )  # 获取失信企业tab的搜索数
            list_number = self.operation.new_find_elements(
                By.XPATH, self.ELEMENT["list_ico"]
            )
            self.assertEqual(enterprise_num, len(list_number) - 1, "count数与列表数不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0002_02_0(self):
        "「失信企业」搜索结果包含搜索词"
        log.info(self.test_ss_0002_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            list_number = self.operation.new_find_elements(
                By.XPATH, self.ELEMENT["list_ico"]
            )
            for i in range(2, len(list_number)):
                name = self.operation.new_find_element(
                    By.XPATH, self.ELEMENT["dishonest_name"].format(i)
                ).text
                include_key = "".join(set("司马朝") & set(name))  # 获取交集
                self.assertIsNotNone(include_key, "搜索结果不包含关键字")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0002_03_0(self):
        "「失信企业」搜索结果iterm 都含有老赖标签"
        log.info(self.test_ss_0002_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            list_number = self.operation.new_find_elements(
                By.XPATH, self.ELEMENT["list_ico"]
            )
            for i in range(2, len(list_number)):
                join_element = "{}[{}]//*{}".format(
                    self.ELEMENT["list_ico"], i, self.ELEMENT["list_deadbeat"]
                )
                text_value = self.operation.new_find_element(By.XPATH, join_element)
                self.assertEqual(text_value.text, "老赖", "标志不为老赖")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0002_04_0(self):
        "「失信企业」未登录，点击人名，调起登录页"
        log.info(self.test_ss_0002_04_0.__doc__)
        try:
            time.sleep(1)
            self.driver.keyevent(4)
            if self.operation.is_login():
                self.operation.logout()
            self.setUp()  # 进入老赖首页
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device
            )
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_legal_person"].format(2, 1, 2)
            ).click()  # 点击企业法人，进入失信详情页
            one_click_login = self.operation.isElementExist(
                By.ID, self.ELEMENT["one_click"]
            )
            get_code_login = self.operation.isElementExist(
                By.ID, self.ELEMENT["login_code"], outtime=2
            )
            flag = False
            if one_click_login or get_code_login:
                flag = True
            self.assertTrue(flag, "已经是登陆状态")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0002_05_0(self):
        "「失信企业」进入详情页，信息与跳转前一致"
        log.info(self.test_ss_0002_05_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "司马朝", self.device)
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            # 企业名
            company_name = self.operation.new_find_element(By.XPATH, self.ELEMENT["dishonest_name"].format(2)).text
            # 获取法人
            legal_person = self.operation.new_find_element(By.XPATH,
                                                           self.ELEMENT["dishonest_legal_person"].format(2, 1, 2)).text
            # 进入失信记录列表页
            self.operation.new_find_element(By.XPATH, self.ELEMENT["dishonest_lists"].format(2)).click()
            # 进入失信详情页
            self.operation.new_find_element(By.XPATH, self.ELEMENT["dishonest_details"].format(1)).click()
            details_company_name = self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_name").text
            details_legal_person = self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_detail_legal_content").text
            self.assertEqual(company_name, details_company_name, "公司名称不一致")
            self.assertEqual(legal_person, details_legal_person, "法人名称不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0003_01_0(self):
        "输入身份证号，匹配到搜索结果"
        log.info(self.test_ss_0003_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "1310821950", self.device)
            card_id = self.operation.new_find_element(By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)).text
            self.assertIn("1310821950", card_id, "身份证不匹配")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0003_02_0(self):
        "输入身份证号，少于6位，不能进行搜索"
        log.info(self.test_ss_0003_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "13108", self.device)
            text = "至少输入6位证件号"
            toast = self.operation.get_toast()
            self.assertEqual(toast, text, "toast不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0003_03_0(self):
        "身份证号搜索，校验count数大于999，是否显示为999+"
        log.info(self.test_ss_0003_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "130984", self.device)
            count_number = self.operation.count_num(By.ID, self.ELEMENT["count_num"])  # 获取count数
            self.assertTrue(count_number > 999, "列表数小于999")
            tab_text = self.operation.new_find_element(By.XPATH, self.ELEMENT["tab_person_count"]).text
            tab_num = tab_text[-4:]
            self.assertEqual(tab_num, "999+", "count数显示错误")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0004_01_0(self):
        "组织机构代码搜索，「失信自然人」没有匹配结果"
        log.info(self.test_ss_0004_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "798532048", self.device)
            people_text = self.operation.new_find_element(By.ID, self.ELEMENT["dishonest_people_null"]).text
            self.assertEqual(people_text, "抱歉，没有找到相关失信自然人", "有搜索结果")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    def test_ss_0004_02_0(self):
        "组织机构代码搜索，输入：798532048,「失信企业」匹配到结果"
        log.info(self.test_ss_0004_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "798532048", self.device)
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            # 获取组织机构代码
            code_id = self.operation.new_find_element(By.XPATH,
                                                      self.ELEMENT["dishonest_legal_person"].format(2, 4, 2)).text
            self.assertEqual(code_id, "798532048", "组织机构代码不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0004_03_0(self):
        "组织机构代码搜索，输入：<>，「失信自然人」「失信企业」无匹配结果"
        log.info(self.test_ss_0004_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "<>", self.device)
            people_text = self.operation.new_find_element(By.ID, self.ELEMENT["dishonest_people_null"]).text
            self.assertEqual(people_text, "抱歉，没有找到相关失信自然人", "有搜索结果")
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            people_text = self.operation.new_find_element(By.ID, self.ELEMENT["dishonest_people_null"]).text
            self.assertEqual(people_text, "抱歉，没有找到相关失信企业", "有搜索结果")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0004_04_0(self):
        "取消搜索，返回到查老赖首页页"
        log.info(self.test_ss_0004_04_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.new_find_element(By.ID, self.ELEMENT["dishonest_mid_cancel"]).click()
            index_text = self.operation.new_find_element(By.ID, self.ELEMENT["index_title1"]).text
            self.assertEqual(index_text, "什么是“老赖”？", "没有返回到查老赖首页")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0005_01_0(self):
        "不输入时搜索框内，不显示一键清除"
        log.info(self.test_ss_0005_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            flag = self.operation.isElementExist(By.ID, self.ELEMENT["dishonest_mid_clean_iv"])
            self.assertFalse(flag, "一键清除按钮存在")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0005_02_0(self):
        "输入时搜索框内，显示一键清除"
        log.info(self.test_ss_0005_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "123", self.device, key_value=8)
            flag = self.operation.isElementExist(By.ID, self.ELEMENT["dishonest_mid_clean_iv"])
            self.assertTrue(flag, "一键清除按钮不存在")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0005_03_0(self):
        "「搜索框」输入内容被清除,恢复默认文案"
        log.info(self.test_ss_0005_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], "123", self.device, key_value=8)
            self.operation.new_find_element(By.ID, self.ELEMENT["dishonest_mid_clean_iv"]).click()
            search_txt = self.operation.new_find_element(By.ID, self.ELEMENT["dishonest_mid_input"]).text
            self.assertEqual(search_txt, "输入人名/公司名/身份证号码/组织机构代码", "没有恢复默认文案")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0005_04_0(self):
        "不输入搜索词，点击搜索"
        log.info(self.test_ss_0005_04_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(By.ID, self.ELEMENT["dishonest_mid_input"], " ", self.device)
            text = "你还没有输入关键词"
            toast = self.operation.get_toast()
            self.assertEqual(toast, text, "toast不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    import unittest

    start_tiem = time.strftime("%Y-%m-%d-%H_%M_%S")
    print("开始时间：{}".format(start_tiem))
    unittest.main()
    end_time = time.strftime("%Y-%m-%d-%H_%M_%S")
    print("结束时间：{}".format(end_time))
