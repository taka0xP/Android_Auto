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
import random
from Providers.logger import Logger, error_format
from Providers.sift.sift_opera import SiftOperation
import time
from Providers.account.account import Account

log = Logger("查关系_04").getlog()


class Search_relationTest(MyTest, Operation):
    """查关系_04"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_relation")
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

    def random_sift_hit(self, select_tag, index=None):
        """
        随机上滑动，选中省市区/一二级行业
        :param select_tag: True：地区；False：行业
        :param index: 0，省（自治区、直辖市）/一级行业；1，市/二级行业；2，区（县）
        :return: 返回值为选中项
        """
        if select_tag:
            tarList = [
                "select_list_level_one",
                "select_list_level_two",
                "select_list_level_three",
            ]
        else:
            tarList = ["select_list_level_one", "select_list_level_three"]
        sift_list = self.new_find_elements(By.XPATH, self.ELEMENT[tarList[index]])
        if sift_list is None or len(sift_list) == 1:
            randNum = 1
        else:
            randNum = random.randint(2, len(sift_list))
            if randNum == len(sift_list):
                randNum = len(sift_list) - 1
        l = self.driver.get_window_size()
        y1 = l["height"] * 0.5
        y2 = l["height"] * 0.2
        if index == 0:
            x1 = l["width"] * 0.15
            for i in range(random.randint(0, 4)):
                self.driver.swipe(x1, y1, x1, y2, 1500)
            area = self.new_find_element(
                By.XPATH,
                self.ELEMENT[tarList[index]]
                + "["
                + str(randNum)
                + "]/android.widget.TextView",
            )
            areaText = area.text
            area.click()
            return areaText
        elif index == 1:
            x1 = l["width"] * 0.5
            for i in range(random.randint(0, 4)):
                self.driver.swipe(x1, y1, x1, y2, 1500)
            area = self.new_find_element(
                By.XPATH,
                self.ELEMENT[tarList[index]]
                + "["
                + str(randNum)
                + "]/android.widget.TextView",
            )
            areaText = area.text
            if len(sift_list) != 1:
                area.click()
            return areaText
        else:
            x1 = l["width"] * 0.85
            if sift_list is None:
                area = self.new_find_element(
                    By.XPATH,
                    self.ELEMENT[tarList[index - 1]] + "[1]/android.widget.TextView",
                )
                areaText = area.text
                area.click()
                return areaText
            else:
                for i in range(random.randint(0, 4)):
                    self.driver.swipe(x1, y1, x1, y2, 1500)
                area = self.new_find_element(
                    By.XPATH,
                    self.ELEMENT[tarList[index]]
                    + "["
                    + str(randNum)
                    + "]/android.widget.TextView",
                )
                areaText = area.text
                area.click()
                return areaText

    @getimage
    def test_001_cgx_contact_p0(self):
        """查关系搜索结果页身边老板"""
        log.info(self.test_001_cgx_contact_p0.__doc__)
        try:
            self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
            self.new_find_element(By.ID, self.ELEMENT["search_relation"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.new_find_element(By.ID, self.ELEMENT["from_input_textview"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_contacts"]).click()
            time.sleep(5)

            # 通讯录身边老板功能
            if self.isElementExist(By.ID, "com.tianyancha.skyeye:id/btn_close_guide"):
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/btn_close_guide"
                ).click()
            if self.isElementExist(By.ID, self.ELEMENT["tv_boss_count"]):
                # 断言-查询通讯录身边老板，进入通讯录列表页
                self.assertTrue(
                    self.isElementExist(By.ID, self.ELEMENT["tv_boss_count"]),
                    "===失败-授权后查询通讯录老板失败===",
                )
                # 断言-点击身边老板列表页item，进入公司详情页
                tarCompanyName = self.new_find_element(
                    By.XPATH, self.ELEMENT["contact_list_item"]
                ).text
                self.new_find_element(
                    By.XPATH, self.ELEMENT["contact_list_item"]
                ).click()
                companyName = self.new_find_element(
                    By.ID, self.ELEMENT["firm_detail_name_tv"]
                ).text
                self.assertEqual(tarCompanyName, companyName, "===失败-点击通讯录公司，跳转错误===")
                self.driver.keyevent(4)
            else:
                if self.isElementExist(
                    By.XPATH,
                    '//*[@class="android.widget.TextView" and @text="没有发现通讯录中的老板"]',
                ):
                    log.info("===通讯录中无老板===")
                else:
                    if self.isElementExist(By.ID, self.ELEMENT["to_monitor_btn"]):
                        self.new_find_element(By.ID, self.ELEMENT["to_monitor_btn"]).click()
                    self.new_find_element(
                        By.ID, self.ELEMENT["permission_deny_button"]
                    ).click()
                    self.new_find_element(
                        By.ID, self.ELEMENT["search_contacts"]
                    ).click()
                    # 断言-未授权通讯录读取权限，再次查询身边老板，弹出二次授权弹框
                    self.assertTrue(
                        self.isElementExist(
                            By.ID, self.ELEMENT["permission_allow_button"]
                        ),
                        "===失败-未授权通讯录权限，再次查通讯录中老板，二次授权弹窗弹出失败===",
                    )
                    self.new_find_element(
                        By.ID, self.ELEMENT["permission_allow_button"]
                    ).click()
                    # 断言-通讯录读取权限二次授权通过，查询身边老板
                    self.assertTrue(
                        self.isElementExist(By.ID, self.ELEMENT["iv_update"]),
                        "===失败-授权通讯录读取权限后，查身边老板结果展示错误===",
                    )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_region_p0(self):
        """查关系-地区筛选"""
        log.info(self.test_002_cgx_region_p0.__doc__)
        try:
            self.sift_opera.search_key(2)
            self.new_find_element(By.ID, self.ELEMENT["select_region"]).click()
            region_Log_list = ["省（自治区、直辖市）", "市", "区（县）"]
            for i in range(3):
                area = self.random_sift_hit(True, i)
                log.info("===地区筛选：" + region_Log_list[i] + "：" + area + "===")
            addrInfo = area[0:2]
            self.new_find_element(By.XPATH, self.ELEMENT["from_target_item_1"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["sky_canvas"]).click()
            for i in range(20):
                if self.isElementExist(By.XPATH, self.ELEMENT["more_gsxx_dimension"]):
                    self.new_find_element(
                        By.XPATH, self.ELEMENT["more_gsxx_dimension"]
                    ).click()
                    for i in range(20):
                        if self.isElementExist(
                            By.XPATH, self.ELEMENT["field_zcdz"]
                        ):  # 普通公司校验
                            addr_detail = self.new_find_element(
                                By.XPATH,
                                self.ELEMENT["field_zcdz"]
                                + self.ELEMENT["follow_textview"],
                            ).text
                            self.assertIn(addrInfo, addr_detail, "===失败-公司地址匹配错误===")
                            break
                        elif self.isElementExist(
                            By.XPATH, self.ELEMENT["field_zs"]
                        ):  # 事业单位校验
                            addr_detail = self.new_find_element(
                                By.XPATH,
                                self.ELEMENT["field_zs"]
                                + self.ELEMENT["follow_textview"],
                            ).text
                            self.assertIn(addrInfo, addr_detail, "===失败-公司地址匹配错误===")
                            break
                        else:
                            self.swipeUp(0.5, 0.7, 0.3, 2000)
                            if i == 19:
                                log.error("===未校验出结果===")
                    break
                elif self.isElementExist(By.XPATH, self.ELEMENT["more_djxx_dimension"]):
                    self.new_find_element(
                        By.XPATH, self.ELEMENT["more_djxx_dimension"]
                    ).click()
                    for i in range(20):
                        if self.isElementExist(
                            By.XPATH, self.ELEMENT["field_jjhdz"]
                        ):  # 基金会校验
                            addr_detail = self.new_find_element(
                                By.XPATH,
                                self.ELEMENT["field_jjhdz"]
                                + self.ELEMENT["follow_textview"],
                            ).text
                            self.assertIn(addrInfo, addr_detail, "===失败-公司地址匹配错误===")
                            break
                        elif self.isElementExist(
                            By.XPATH, self.ELEMENT["field_zs"]
                        ):  # 社会组织校验
                            addr_detail = self.new_find_element(
                                By.XPATH,
                                self.ELEMENT["field_zs"]
                                + self.ELEMENT["follow_textview"],
                            ).text
                            self.assertIn(addrInfo, addr_detail, "===失败-公司地址匹配错误===")
                            break
                        elif self.isElementExist(
                            By.XPATH, self.ELEMENT["field_dz"]
                        ):  # 律师事务所校验
                            addr_detail = self.new_find_element(
                                By.XPATH,
                                self.ELEMENT["field_dz"]
                                + self.ELEMENT["follow_textview"],
                            ).text
                            self.assertIn(addrInfo, addr_detail, "===失败-公司地址匹配错误===")
                            break
                        elif self.isElementExist(
                            By.XPATH, self.ELEMENT["field_gsszd"]
                        ):  # 台湾企业校验
                            addr_detail = self.new_find_element(
                                By.XPATH,
                                self.ELEMENT["field_gsszd"]
                                + self.ELEMENT["follow_textview"],
                            ).text
                            self.assertIn(addrInfo, addr_detail, "===失败-公司地址匹配错误===")
                            break
                        else:
                            self.swipeUp(0.5, 0.7, 0.3, 2000)
                            if i == 19:
                                log.error("===未校验出结果===")
                    break
                else:
                    self.swipeUp(0.5, 0.7, 0.3, 2000)
                    if i == 19:
                        log.info("断言失败-公司详情页未找到「工商信息/登记信息」")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_cgx_industry_p0(self):
        """查关系-行业筛选"""
        log.info(self.test_003_cgx_industry_p0.__doc__)
        industry = None
        try:
            self.sift_opera.search_key(2)
            self.new_find_element(By.ID, self.ELEMENT["select_industry"]).click()
            industry_Log_list = ["一级行业", "二级行业"]
            for i in range(2):
                industry = self.random_sift_hit(False, i)
                log.info("===行业筛选：" + industry_Log_list[i] + "：" + industry + "===")
            # 若筛选无结果，重新筛选，最多筛选20次，
            if self.isElementExist(By.XPATH, self.ELEMENT["from_target_item_1"]):
                self.new_find_element(
                    By.XPATH, self.ELEMENT["from_target_item_1"]
                ).click()
                self.new_find_element(By.XPATH, self.ELEMENT["sky_canvas"]).click()
                log.info(
                    "行业筛选，断言公司名称："
                    + self.new_find_element(
                        By.ID, self.ELEMENT["firm_detail_name_tv"]
                    ).text
                )
                for i in range(20):
                    if self.isElementExist(
                        By.XPATH, self.ELEMENT["more_gsxx_dimension"]
                    ):
                        self.new_find_element(
                            By.XPATH, self.ELEMENT["more_gsxx_dimension"]
                        ).click()
                        # 断言-查关系搜索关键词，行业筛选
                        for i in range(20):
                            if self.isElementExist(
                                By.XPATH,
                                '//*[@class="android.widget.TextView" and @text="'
                                + industry
                                + '"]',
                            ):
                                self.assertEqual(
                                    industry,
                                    self.new_find_element(
                                        By.XPATH,
                                        '//*[@class="android.widget.TextView" and @text="'
                                        + industry
                                        + '"]',
                                    ).text,
                                    "===失败-工商信息详情页中，行业筛选断言错误===",
                                )
                                break
                            else:
                                self.swipeUp(0.5, 0.7, 0.3, 2000)
                                if i == 19:
                                    log.info("行业筛选断言失败-工商信息详情页，行业未找到")
                        break
                    else:
                        self.swipeUp(0.5, 0.7, 0.3, 2000)
                        if i == 19:
                            log.info("行业筛选断言失败-公司详情页未找到「工商信息」")
            else:
                log.info("行业筛选无结果！！！")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
