# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : ZYF
# @File    : search_boss_test1.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
import time, random, unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger

log = Logger("查老板_01").getlog()


class Search_bossTest1(MyTest, Operation):
    """查老板_01"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_boss")
    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     a = Read_Ex()
    #     cls.ELEMENT = a.read_excel('Search_boss')

    def close_guide(self):
        loc = (By.ID, "com.tianyancha.skyeye:id/btn_close_guide")
        try:
            e = WebDriverWait(self.driver, 2, 0.5).until(
                EC.presence_of_element_located(loc)
            )
            e.click()
        except:
            pass

    @getimage
    def test_001_CLB_SYSS_p0(self):
        """首页TAB切换"""
        log.info(self.test_001_CLB_SYSS_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.assertEqual(
                self.new_find_element(By.ID, self.ELEMENT["search_box"]).text,
                self.ELEMENT["boss_input_prompt"],
                "输入框文本信息不一致",
            )
            self.assertTrue(self.Element(By.ID, self.ELEMENT["boss_icon"]))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_002_CLB_SYSS_p0(self):
        """首页-查老板点击热门搜索"""
        log.info(self.test_002_CLB_SYSS_p0.__doc__)
        try:
            index = random.randint(6, 11)
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_elements(By.XPATH, self.ELEMENT["top_search"])[index].click()
            loc = (By.ID, self.ELEMENT["first_btn"])
            try:
                e = WebDriverWait(self.driver, 2, 0.5).until(
                    EC.presence_of_element_located(loc)
                )
                e.click()
            except:
                pass
            a = self.new_find_element(By.ID, self.ELEMENT["name"])
            print("操作热搜人员名称：", a.text, index)
            time.sleep(0.5)
            self.assertTrue(self.Element("人员详情"))
            self.assertIsNotNone(a.text)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_003_CLB_SYSS_p0(self):
        """首页-查老板跳转搜索中间页"""
        log.info(self.test_003_CLB_SYSS_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.assertEqual(
                self.new_find_element(By.ID, self.ELEMENT["search_box1"]).text,
                self.ELEMENT["boss_input_prompt"],
                "输入框文本信息不正确",
            )
            self.assertTrue(self.Element(self.ELEMENT["found_boss"]))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_004_CLB_SYZJY_p0(self):
        """查老板搜索中间页点击热门搜索"""
        log.info(self.test_004_CLB_SYZJY_p0.__doc__)
        try:
            index = random.randint(0, 8)
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            a = self.new_find_elements(By.XPATH, self.ELEMENT["top_search1"])
            if a == None:
                b = self.new_find_element(By.ID, self.ELEMENT["search_clean"])
                if b == None:
                    self.new_find_element(By.ID, self.ELEMENT["Browsing_clean"]).click()
                    self.new_find_element(By.ID, self.ELEMENT["confirm_clean"]).click()
                    self.new_find_elements(By.XPATH, self.ELEMENT["top_search1"])[
                        index
                    ].click()
                else:
                    self.new_find_element(By.ID, self.ELEMENT["search_clean"]).click()
                    self.new_find_element(By.ID, self.ELEMENT["confirm_clean"]).click()
                    c = self.new_find_element(By.ID, self.ELEMENT["Browsing_clean"])
                    if c is None:
                        self.new_find_elements(By.XPATH, self.ELEMENT["top_search1"])[
                            index
                        ].click()
                    else:
                        self.new_find_element(
                            By.ID, self.ELEMENT["Browsing_clean"]
                        ).click()
                        self.new_find_element(
                            By.ID, self.ELEMENT["confirm_clean"]
                        ).click()
                        self.new_find_elements(By.XPATH, self.ELEMENT["top_search1"])[
                            index
                        ].click()
            else:
                self.new_find_elements(By.XPATH, self.ELEMENT["top_search1"])[
                    index
                ].click()
            loc = (By.ID, self.ELEMENT["first_btn"])
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(
                    EC.presence_of_element_located(loc)
                )
                e.click()
            except Exception as e:
                print(e, "没有首次弹框")
                pass
            print(
                "操作热搜人员名称：",
                self.new_find_element(By.ID, self.ELEMENT["name"]).text,
                index,
            )
            self.assertTrue(self.Element(self.ELEMENT["personnel"]))
            self.assertIsNotNone(
                self.new_find_element(By.ID, self.ELEMENT["name"]).text
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_005_CLB_SYZJY_p0(self):
        """搜索-通过中文人名-有结果「马云 杭州」"""
        log.info(self.test_005_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box1"]).send_keys(
                self.ELEMENT["people"]
            )
            self.assertEqual(
                self.new_find_element(By.ID, self.ELEMENT["search_box1"]).text,
                self.ELEMENT["people"],
                "搜索框老板名不匹配",
            )
            self.assertEqual(
                int(self.new_find_element(By.ID, self.ELEMENT["person_result"]).text),
                int(self.ELEMENT["result_num"]),
                "结果count不一致",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_006_CLB_SYZJY_p0(self):
        """搜索-通过中文人名-无结果"""
        log.info(self.test_006_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box1"]).send_keys("张三丰安利")
            self.assertEqual(
                self.new_find_element(By.ID, self.ELEMENT["search_box1"]).text,
                self.ELEMENT["people1"],
                "搜索框老板名不匹配",
            )
            self.assertFalse(self.Element(self.ELEMENT["person_result"]))
            self.assertIsNotNone(
                self.new_find_element(By.ID, self.ELEMENT["noResult_jump"]).text
            )
            self.assertTrue(self.Element("抱歉，没有找到相关老板！"))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_007_CLB_SYZJY_p0(self):
        """搜索-通过英文人名-有结果"""
        log.info(self.test_007_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.adb_send_input(
                By.ID, self.ELEMENT["search_box1"], self.ELEMENT["people2"], self.device
            )
            result = self.new_find_element(By.ID, self.ELEMENT["search_box1"]).text
            # self.assertEqual(result, self.ELEMENT['people2'], "搜索框老板名不匹配")
            a = int(self.ELEMENT["result_num1"])
            b = int(self.new_find_element(By.ID, self.ELEMENT["person_result"]).text)
            self.assertEqual(a, b, "结果count不一致")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_008_CLB_SYZJY_p0(self):
        """"搜索-通过英文人名-无结果"""
        log.info(self.test_008_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.adb_send_input(
                By.ID, self.ELEMENT["search_box1"], self.ELEMENT["people3"], self.device
            )
            self.assertEqual(
                self.new_find_element(By.ID, self.ELEMENT["search_box1"]).text,
                "marry",
                "搜索框老板名不匹配",
            )
            self.assertIsNotNone(
                self.new_find_element(By.ID, self.ELEMENT["noResult_jump"]).text
            )
            self.assertTrue(self.Element("抱歉，没有找到相关老板！"))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_009_CLB_SYZJY_p0(self):
        """搜索-通过特殊字符-无结果"""
        log.info(self.test_009_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.adb_send_input(
                By.ID, self.ELEMENT["search_box1"], self.ELEMENT["people4"], self.device
            )
            ele = self.isElementExist(By.ID, self.ELEMENT["person_result"])
            self.assertEqual(
                self.ELEMENT["people4"],
                self.new_find_element(By.ID, self.ELEMENT["search_box1"]).text,
                "搜索框老板名不匹配",
            )
            self.assertFalse(ele)
            self.assertIsNotNone(
                self.new_find_element(By.ID, self.ELEMENT["noResult_jump"]).text
            )
            self.assertTrue(self.Element("抱歉，没有找到相关老板！"))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_010_CLB_SYZJY_p0(self):
        """搜索-不输入关键字搜索"""
        log.info(self.test_010_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.adb_send_input(By.ID, self.ELEMENT["search_box1"], "", self.device)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_011_CLB_SYTGY_p0(self):
        """搜索中间页-一键清除"""
        log.info(self.test_011_CLB_SYTGY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box1"]).send_keys(
                self.ELEMENT["people"]
            )
            self.new_find_element(By.ID, self.ELEMENT["clean_button"]).click()
            self.assertEqual(
                self.ELEMENT["boss_input_prompt"],
                self.new_find_element(By.ID, self.ELEMENT["search_box1"]).text,
                "输入框文本信息不正确",
            )
            self.assertTrue(self.Element("发现手机通讯录里的大老板，"))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_012_CLB_SYJGY_p0(self):
        """搜索结果页-筛选"""
        log.info(self.test_012_CLB_SYJGY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box1"]).send_keys(
                "王四会"
            )
            a = self.new_find_element(By.ID, self.ELEMENT["person_result"]).text
            self.new_find_element(By.ID, self.ELEMENT["All_areas"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["Screening1"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["Screening2"]).click()
            b = self.new_find_element(By.ID, self.ELEMENT["person_result"]).text
            self.assertGreaterEqual(a, b, "筛选后的结果比筛选前大")
            c = self.new_find_element(By.ID, self.ELEMENT["All_areas"]).text
            self.assertEqual(self.ELEMENT["All_areas_value"], c, "地区筛选后标题不一致")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_013_CLB_SYJGY_p0(self):
        """搜索结果页跳转人详情-未登录"""
        log.info(self.test_013_CLB_SYJGY_p0.__doc__)
        try:
            a = self.is_login()
            if a is False:
                pass
            else:
                self.logout()
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.adbSend_appium(self.device)
            self.new_find_element(By.ID, self.ELEMENT["search_box1"]).send_keys(
                "王四会"
            )
            self.new_find_elements(By.ID, self.ELEMENT["all_company"])[1].click()
            time.sleep(0.5)
            a = self.Element(self.ELEMENT["login_bs"])
            self.assertTrue(a)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_014_CLB_SYJGY_p0(self):
        """搜索结果页跳转人详情-登录"""
        log.info(self.test_014_CLB_SYJGY_p0.__doc__)
        try:
            a = self.is_login()
            if a:
                pass
            else:
                self.login(11099990133, "ef08beca")
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.adbSend_appium(self.device)
            self.new_find_element(By.ID, self.ELEMENT["search_box1"]).send_keys(
                "王四会"
            )
            self.new_find_elements(By.ID, self.ELEMENT["all_company"])[1].click()
            a = self.new_find_element(By.ID, self.ELEMENT["name"])
            self.assertTrue(self.Element("人员详情"))
            self.assertIsNotNone(a.text)
            # 后退回到搜素搜结果列表页
            self.driver.keyevent(4)
            # 输入框『X』
            self.new_find_element(By.ID, self.ELEMENT["clean_button"]).click()
            # 最近浏览清除
            self.new_find_element(By.ID, self.ELEMENT['Browsing_clean']).click()
            self.new_find_element(By.ID, self.ELEMENT['confirm_clean']).click()
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_015_CLB_SYZJY_p0(self):
        """搜索中间页点击-发现通讯录中的老板"""
        log.info(self.test_015_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            self.new_find_element(By.ID, self.ELEMENT["view"]).click()
            loc = (By.ID, self.ELEMENT["permission_allow_button"])
            try:
                e = WebDriverWait(self.driver, 10, 0.5).until(
                    EC.presence_of_element_located(loc)
                )
                e.click()
            except Exception as e:
                print(e, "已开启通讯录权限")
                pass
            self.close_guide()
            self.assertTrue(self.isElementExist(By.ID, self.ELEMENT["phone_bs"]))
            self.assertTrue(self.isElementExist(By.XPATH, self.ELEMENT["phone"]))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_016_CLB_SYZJY_p0(self):
        """搜索中间页最近搜索的功能-最多10条记录"""
        log.info(self.test_016_CLB_SYZJY_p0.__doc__)
        try:
            name_list = [
                "马云1",
                "孙凯1",
                "王四会1",
                "马丁1",
                "韩磊1",
                "李明1",
                "向小叶1",
                "蓝小凯1",
                "李晓凯1",
                "朱小凯1",
                "赵小凯1",
                "陈小凯1",
            ]
            self.new_find_element(By.ID, self.ELEMENT["search_boss"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()
            i = 0
            for i in range(len(name_list)):
                self.adb_send_input(
                    By.ID, self.ELEMENT["search_box1"], name_list[i], self.device
                )
                log.info("输入搜索词：{}".format(name_list[i]))
                self.new_find_element(By.ID, self.ELEMENT["clean_button"]).click()
                i += 1
            print("搜索%s次" % (i))
            history_words = self.new_find_elements(
                By.XPATH, self.ELEMENT["search_history"]
            )
            value = len(history_words)
            for i in range(10):
                log.info(
                    "历史:{} vs 输入:{}".format(history_words[i].text, name_list[11 - i])
                )
                self.assertEqual(history_words[i].text, name_list[11 - i], "名字顺序不一致")
            print("页面展示最近搜索记录%s次" % value)
            self.assertEqual(10, value, "搜索12次目前展示%s个最近搜索" % value)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception


if __name__ == "__main__":
    unittest.main()
