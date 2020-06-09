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
import unittest


log = Logger("查老赖_03").getlog()


class TestSearchDisHonest3(MyTest):
    "查老赖_03"
    a = Read_Ex()
    ELEMENT = a.read_excel("search_dishonest")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dishone = Dishonest(cls.driver, cls.ELEMENT)
        cls.operation = Operation(cls.driver)

    def setUp(self):
        self.operation.new_find_element(
            By.XPATH, self.ELEMENT["dishonest_in_main"]
        ).click()

    @getimage
    def test_sssx_0005_01_0(self):
        "「失信自然人」可以通过「地域」+「性别」复合筛选"
        log.info(self.test_sssx_0005_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "李星雨", self.device
            )
            self.dishone.search_city("安徽省", "安徽省全省")
            self.dishone.search_sex("女")
            car_id = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).text
            city_info = card_operation().check_region(car_id)
            sex_info = card_operation().check_sex(car_id)
            self.assertIn("安徽省", city_info, "所属区域不符合筛选条件")
            self.assertEqual("女", sex_info, "出生年月不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0006_01_0(self):
        "「失信自然人」可以通过「性别」+「出生年份」复合筛选"
        log.info(self.test_sssx_0006_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "李星竹", self.device
            )
            self.dishone.search_year("1998年", 0.6, 0.5)
            self.dishone.search_sex("女")
            car_id = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).text
            self.assertIn("1998", car_id, "出生年月不正确")
            sex = card_operation().check_sex(car_id)
            self.assertEqual("女", sex, "性别不符合筛选结果")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0007_01_0(self):
        "「失信自然人」可以通过「地域」+「出生年份」+「性别」复合筛选"
        log.info(self.test_sssx_0007_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "李子微", self.device
            )
            self.dishone.search_city("河北省", "邯郸市")
            self.dishone.search_year("1998年", 0.6, 0.5)
            self.dishone.search_sex("女")
            car_id = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).text
            city_info = card_operation().check_region(car_id)
            self.assertIn("邯郸市", city_info, "所属区域不符合筛选条件")
            self.assertIn("1998", car_id, "出生年月不正确")
            sex = card_operation().check_sex(car_id)
            self.assertEqual("女", sex, "性别不符合筛选结果")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sssx_0008_01_0(self):
        "性别+年龄复合筛选，自然人筛选无结果"
        log.info(self.test_sssx_0008_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马芸芸", self.device
            )
            self.dishone.search_year("1998年", 0.6, 0.5)  # 查询年龄
            self.dishone.search_sex("男")  # 查询性别
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
    def test_sssx_0009_01_0(self):
        "「失信企业」可以通过地域进行筛选"
        log.info(self.test_sssx_0009_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "马云", self.device
            )
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            self.dishone.search_city("山西省", "山西省全省")
            company_name = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_name"].format(2)
            ).text  # 获取公司名字
            flag = "大同市" in company_name
            if not flag:
                self.operation.new_find_element(
                    By.XPATH, self.ELEMENT["dishonest_details"].format(2)
                ).click()  # 点击企业法人，进入失信详情页
                self.operation.new_find_element(
                    By.ID, self.ELEMENT["company_name"]
                ).click()  # 点击进入公司详情页
                if self.operation.isElementExist(
                    By.ID, "com.tianyancha.skyeye:id/btn"
                ):  # 判断是否第一次进入
                    self.operation.new_find_element(
                        By.ID, "com.tianyancha.skyeye:id/btn"
                    ).click()
                self.operation.swipeUp(0.4, 0.7, 0.3)  # 滑动页面，找到工商信息
                self.operation.new_find_element(
                    By.ID, self.ELEMENT["company_business_info"]
                ).click()  # 进入工商信息
                self.operation.swipeUp(0.4, 0.7, 0.3)  # 滑动页面，找到等级机关
                reg_info = self.operation.new_find_element(
                    By.ID, self.ELEMENT["company_registrar"]
                ).text  # 获取登记机关信息
                self.assertIn("山西省", reg_info, "区域不符合筛选结果")
            else:
                self.assertTrue(flag, "区域不符合筛选结果")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sxjl_0001_01_0(self):
        "「失信记录列表页」的「返回」正常"
        log.info(self.test_sxjl_0001_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马宏", self.device
            )
            old_people_name = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_name"].format(2)
            ).text
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).click()  # 进入到详情页
            self.operation.new_find_element(By.ID, self.ELEMENT["list_back"]).click()
            new_people_name = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_name"].format(2)
            ).text
            self.assertEqual(old_people_name, new_people_name, "返回搜搜页不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sxjl_0001_02_0(self):
        "「失信记录列表页」的「分享」正常"
        log.info(self.test_sxjl_0001_02_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马宏", self.device
            )
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).click()  # 进入到详情页
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["list_share"]
            ).click()  # 点击分享
            wechat_friends = self.operation.isElementExist(
                By.ID, self.ELEMENT["wechat_friends"]
            )
            self.assertTrue(wechat_friends, "分享功能未打开")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sxjl_0001_03_0(self):
        "「失信记录列表页」的「存长图」正常"
        log.info(self.test_sxjl_0001_03_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马宏", self.device
            )
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).click()  # 进入到详情页
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["list_longpic"]
            ).click()  # 点击存长图
            wechat_friends = self.operation.isElementExist(
                By.ID, self.ELEMENT["save_btn"]
            )
            self.assertTrue(wechat_friends, "存长图功能不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @unittest.skip("无法获取到toast")
    @getimage
    def test_sxjl_0001_04_0(self):
        "「失信记录列表页」的「上滑加载」功能"
        log.info(self.test_sxjl_0001_04_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "司马宏", self.device
            )
            self.dishone.broken_faith_enterprise().click()  # 进入到 失信企业 列表
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).click()  # 进入到详情页
            self.operation.swipeUp(0.3, 0.7, 0.3)
            text = "无数据"
            toast = self.operation.new_find_element(
                By.XPATH, ".//*[contains(@text,'{}')]".format(text)
            ).text
            self.assertEqual(toast.text, text, "toast不正确")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_sxxq_0001_01_0(self):
        "「失信详情」根据案号关联正确"
        log.info(self.test_sxxq_0001_01_0.__doc__)
        try:
            self.dishone.into_dishonest_mid().click()  # 进入查老赖中间页
            self.operation.adb_send_input(
                By.ID, self.ELEMENT["dishonest_mid_input"], "吴俊良", self.device
            )
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["dishonest_card_id"].format(2)
            ).click()  # 进入到详情页
            case_id = self.operation.new_find_element(
                By.XPATH, self.ELEMENT["company_case_name"].format(1)
            ).text  # 获取案号
            self.operation.new_find_element(
                By.XPATH, self.ELEMENT["company_case_name"].format(1)
            ).click()  # 进入失信详情
            details_case_id = self.operation.new_find_element(
                By.ID, "com.tianyancha.skyeye:id/dishonest_detail_gistid_tv"
            ).text
            self.assertEqual(case_id, details_case_id, "根据案号进入失信详情错误")
        except AssertionError as ae:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    import unittest

    unittest.main()
