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
from Providers.check_card_id import card_operation
from Providers.dishonest.dishonest_fun import Dishonest
from Providers.company.company import CompanyFunc


log = Logger("查老赖_02").getlog()


class TestSearchDisHonest2(MyTest):
    "查老赖_02"

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
    def test_ss_0006_01_0(self):
        "输入搜索词，点击搜索，不在展示热搜区域"
        log.info(self.test_ss_0006_01_0.__doc__)
        try:
            # self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.dishone.into_dishonest_mid().click()

            self.operation.adb_send_input(
                By.ID,
                self.ELEMENT["dishonest_mid_input"],
                "宝鸡有一群怀揣着梦想的少年相信在牛大叔的带领下会创造生命的奇迹网络科技有限公司",
                self.device,
            )
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_mid_clean_iv"]
            ).click()
            flag = self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_mid_hot_scope"]
            )
            self.assertFalse(flag, "热搜区域存在")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0006_02_0(self):
        "输入马云，最新搜索词，排在第一个"
        log.info(self.test_ss_0006_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马凯", self.device
            )
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_mid_clean_iv"]
            ).click()
            hot_words = self.operation.new_find_elements(
                By.XPATH, self.ELEMENT["dishonest_history_search"]
            )
            self.assertEqual(hot_words[0].text, "马凯", "最新搜索词，不在第一位")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0006_03_0(self):
        "从历史搜索进入后，该条记录排在历史搜索第一位"
        log.info(self.test_ss_0006_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            hot_words = self.operation.new_find_elements(
                By.XPATH, self.ELEMENT["dishonest_history_search"]
            )
            log.info("历史搜索词，第二个是：{}".format(hot_words[1].text))
            old_word = hot_words[1].text
            hot_words[1].click()
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_mid_clean_iv"]
            ).click()
            new_words = self.operation.new_find_elements(
                By.XPATH, self.ELEMENT["dishonest_history_search"]
            )
            self.assertEqual(new_words[0].text, old_word, "搜索词顺序未发生变化")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0006_04_0(self):
        "连续输入10次不同的关键词，最后一次输入为历史搜索的第一条记录"
        log.info(self.test_ss_0006_04_0.__doc__)
        try:
            self.dishone.clean_search_history()
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            name_list = [
                "王思聪",
                "王思松",
                "吴京",
                "马里奥",
                "宝鸡有一群",
                "赵静",
                "诸葛亮",
                "赵云",
                "曹操",
                "终于第十个了",
            ]
            for name in name_list:
                log.info("输入搜索词：{}".format(name))
                self.operation.adb_send_input(
                    By.ID, self.ELEMENT["dishonest_mid_input"], name, self.device
                )
                self.operation.new_find_element(
                    By.ID, self.ELEMENT["dishonest_mid_clean_iv"]
                ).click()
            history_words = self.operation.new_find_elements(
                By.XPATH, self.ELEMENT["dishonest_history_search"]
            )
            for i in range(10):
                log.info(
                    "历史:{} vs 输入:{}".format(history_words[i].text, name_list[9 - i])
                )
                self.assertEqual(history_words[i].text, name_list[9 - i], "名字顺序不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0006_05_0(self):
        "「搜索中间页」，点击「清除最近搜索」按钮,弹窗提示"
        log.info(self.test_ss_0006_05_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_del_history"]
            ).click()
            toast_text = self.operation.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/txt_msg"
            ).text
            self.assertEqual(toast_text, "确定要清空搜索记录?", "清除搜索历史记录，提示信息不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0006_06_0(self):
        "「搜索中间页」，点击「清除最近搜索」按钮，点击取消"
        log.info(self.test_ss_0006_06_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_del_history"]
            ).click()  # 点击一键清除
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_del_cancel"]
            ).click()  # 点击取消
            search_text = self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_old_search"]
            ).text
            self.assertEqual(search_text, "最近搜索", "最近搜索标签不存在")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_ss_0006_07_0(self):
        "「搜索中间页」，点击「清除最近搜索」按钮，点击确定"
        log.info(self.test_ss_0006_07_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_del_history"]
            ).click()  # 点击一键清除
            self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_del_submit"]
            ).click()  # 点击确认
            hot_search_text = self.operation.new_find_element(
                By.XPATH,
                "//*[@resource-id='{}']/android.widget.TextView".format(
                    self.ELEMENT["dishonest_mid_hot_scope"]
                ),
            ).text
            self.assertEqual(hot_search_text, "热门搜索", "热门搜索标签不存在")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0001_01_0(self):
        "搜索马云凤后按河南省-新乡市地域筛选"
        log.info(self.test_sssx_0001_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马云凤", self.device
            )
            self.dishone.search_city("河南省", "新乡市")
            list_number = (
                len(
                    self.operation.new_find_elements(By.XPATH, self.ELEMENT["list_ico"])
                )
                - 1
            )  # 列表数
            people_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["tab_person_count"]
            )
            tab_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )
            flag = False
            if list_number == people_number == tab_number:
                flag = True
            self.assertTrue(flag, "tab数、count数、列表数不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0001_02_0(self):
        "按地域筛选后，所有的筛选结果均属于该地域"
        log.info(self.test_sssx_0001_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马云峰", self.device
            )
            self.dishone.search_city("江苏省", "无锡市")
            tab_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )
            for i in range(2, tab_number + 2):
                car_id = self.operation.new_find_element(
                    By.XPATH, self.ELEMENT["dishonest_card_id"].format(i)
                ).text
                city_info = card_operation().check_region(car_id)
                self.assertIn("无锡市", city_info, "该老赖所属区域不符合")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0001_03_0(self):
        "搜索马云，记录count数，按地域筛选后，重置筛选条件,count数不变"
        log.info(self.test_sssx_0001_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马云", self.device
            )
            tab_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )
            self.dishone.search_city("河南省", "新乡市")
            self.dishone.back_all_regions()
            new_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )
            self.assertEqual(new_number, tab_number, "两次的count数不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0002_01_0(self):
        "失信自然人，使用年龄进行筛选且列表的失信人年龄都满足"
        log.info(self.test_sssx_0002_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马云", self.device
            )
            self.dishone.search_year("1999年", 0.6, 0.5)
            tab_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )
            for i in range(2, tab_number + 2):
                log.info(i)
                card_id = self.operation.new_find_element(
                    By.XPATH, self.ELEMENT["dishonest_card_id"].format(i)
                ).text
                log.info(card_id)
                self.assertIn("1999", card_id, "年龄不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0002_02_0(self):
        "使用年龄筛选2005年，列表里没有匹配结果"
        log.info(self.test_sssx_0002_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马云", self.device
            )
            self.dishone.search_year("2005年", 0.6, 0.8)
            people_text = self.operation.new_find_element(
                By.ID, self.ELEMENT["dishonest_people_null"]
            ).text
            self.assertEqual(people_text, "抱歉，没有找到相关失信自然人", "有搜索结果")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0002_03_0(self):
        "取消年龄筛选，count数与筛选前一致"
        log.info(self.test_sssx_0002_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马云", self.device
            )
            tab_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )  # 无筛选条件的count数
            self.dishone.search_year("1999年", 0.6, 0.5)
            self.dishone.search_year("全部", y1=0.4, y2=0.8)
            new_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )
            self.assertEqual(new_number, tab_number, "两次的count数不一致")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0003_01_0(self):
        "按性别男进行筛选"
        log.info(self.test_sssx_0003_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马峰", self.device
            )
            self.dishone.search_sex("男")
            tab_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )
            for i in range(2, tab_number + 2):
                car_id = self.operation.new_find_element(
                    By.XPATH, self.ELEMENT["dishonest_card_id"].format(i)
                ).text
                sex_info = card_operation().check_sex(car_id)
                self.assertEqual("男", sex_info, "该老赖性别不符合")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0003_02_0(self):
        "按性别筛选，男+女=总的count 数"
        log.info(self.test_sssx_0003_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "王子涵", self.device
            )
            count_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )  # 无筛选条件的count数
            self.dishone.search_sex("男")
            man_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )  # 男性的count数
            self.dishone.search_sex("女")
            woman_number = self.operation.count_num(
                By.XPATH, self.ELEMENT["dishonest_tab_name"]
            )  # 女性的count数
            self.assertEqual(
                count_number, man_number + woman_number, "男+女的count数不等于总count数"
            )
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0004_01_0(self):
        "「失信自然人」可以通过「地域」+「出生年份」复合筛选"
        log.info(self.test_sssx_0004_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "李星杰", self.device
            )
            self.dishone.search_city("安徽省", "安徽省全省")
            self.dishone.search_year("1998年", 0.6, 0.5)
            car_id = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).text
            city_info = card_operation().check_region(car_id)
            self.assertIn("安徽省", city_info, "所属区域不符合筛选条件")
            self.assertIn("1998", car_id, "出生年月不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    import unittest

    unittest.main()
