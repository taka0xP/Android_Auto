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
import re
from Providers.logger import Logger, error_format
import datetime
from Providers.sift.sift_opera import SiftOperation
from Providers.account.account import Account

log = Logger("查关系_03").getlog()


class Search_relationTest(MyTest, Operation):
    """查关系_03"""

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
        cls.account.release_account(cls.phone_vip, account_type='vip')
        super().tearDownClass()

    @getimage
    def into_middle_page(self):
        """
        进入查关系页
        """
        self.new_find_element(By.ID, self.ELEMENT["search_relation"]).click()
        self.new_find_element(By.ID, self.ELEMENT["search_box"]).click()

    @getimage
    def capital(self):
        """注册资本校验"""
        if self.isElementExist(By.ID, self.ELEMENT["more_zczb_title_num"]):
            zczbStr = self.new_find_element(By.ID, self.ELEMENT["more_zczb_title_num"]).text
            if zczbStr == "-":
                result = float(0)
            else:
                result = float(re.findall(r"\d+\.?\d*", zczbStr)[0])
        else:
            result = float(0)
        return result

    @getimage
    def years(self):
        """注册年限校验"""
        zcnxStr = self.new_find_element(By.ID, self.ELEMENT["more_zcnx_title_num"]).text
        if zcnxStr == '-':
            result = datetime.datetime(1900, 1, 1)
        else:
            zcnxStrList = zcnxStr.split(".")
            result = datetime.datetime(int(zcnxStrList[0]), int(zcnxStrList[1]), int(zcnxStrList[2]))
        return result

    @getimage
    def select_image(self, sort, index, tag, inputTarget):
        """
        筛选后，选择公司
        :param sort: 排序
        :param index: 索引
        :param tag: 1：第一家公司；2：第二家公司
        :param inputTarget: 选中项
        :return:
        """
        self.new_find_element(By.ID, self.ELEMENT["search_sort_or_cancel"]).click()
        self.new_find_element(By.XPATH, '//*[@class="android.widget.TextView" and @text="{}"]'.format(sort)).click()
        img_xpath = '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[{}]/android.widget.RelativeLayout/android.widget.ImageView'.format(str(tag))
        self.new_find_element(By.XPATH, img_xpath).click()
        self.new_find_element(By.XPATH, self.ELEMENT["sky_canvas"]).click()
        company_name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("{}，断言公司名称「{}」：{}".format(sort, str(tag), company_name))
        if index == 0 or index == 1:
            result = self.capital()
        else:
            result = self.years()
        self.sift_opera.back2relation_search(inputTarget)
        return result

    @getimage
    def test_001_cgx_sszjy_p0(self):
        """查关系-搜索中间页热搜"""
        log.info(self.test_001_cgx_sszjy_p0.__doc__)
        sortKey = ["按注册资本从高到低", "按注册资本从低到高", "按成立日期从早到晚", "按成立日期从晚到早"]
        try:
            self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
            self.into_middle_page()
            self.new_find_element(By.ID, self.ELEMENT["from_input_textview"]).click()

            # 删除历史记录
            if self.isElementExist(By.ID, self.ELEMENT["middlepage_search_history"]):
                self.new_find_element(By.ID, self.ELEMENT["middlepage_search_history_delete"]).click()
                self.new_find_element(By.ID, self.ELEMENT["delete_confirm"]).click()

            # 断言-点击热搜词，输入框中带入对应关键词
            tarHotWord = self.new_find_element(By.XPATH, self.ELEMENT["middlepage_hot_search_target"])
            hotWordText = tarHotWord.text
            tarHotWord.click()
            tarWordText = self.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).text
            self.assertEqual(tarWordText, hotWordText, "===失败-搜索关键词与热搜关键词不一致===")

            # 断言-搜索输入框一键删除按钮
            btn = self.isElementExist(By.ID, self.ELEMENT["search_clean_iv"])
            self.assertTrue(btn, "===失败-搜索输入框，一键删除按钮展示错误===")

            # 断言-搜索匹配结果包含关键词
            result_text = self.new_find_element(By.XPATH, self.ELEMENT["search_result"]).text
            brand_text = self.new_find_element(By.XPATH, self.ELEMENT["search_result_brand"]).text
            tag = hotWordText in result_text or hotWordText in brand_text
            self.assertTrue(tag, "===失败-搜索结果不包含关键字===")

            # 断言-搜索结果页排序
            self.new_find_element(By.ID, self.ELEMENT["search_clean_iv"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).send_keys("佳洋")
            keyNum = random.randint(0, 3)
            result1 = self.select_image(sortKey[keyNum], keyNum, 1, "佳洋")
            result2 = self.select_image(sortKey[keyNum], keyNum, 2, "佳洋")
            if keyNum == 0 or keyNum == 3:
                # 断言-按注册资本从高到低；按成立日期从晚到早
                self.assertTrue(result1 >= result2, "===失败-{}排序错误===".format(sortKey[keyNum]))
            else:
                # 断言-按注册资本从低到高；按成立日期从早到晚
                self.assertTrue(result1 <= result2, "===失败-{}排序错误===".format(sortKey[keyNum]))

            # 断言-点击搜索输入框一键删除按钮，清空搜索关键词
            self.new_find_element(By.ID, self.ELEMENT["search_clean_iv"]).click()
            cancel = self.new_find_element(By.ID, self.ELEMENT["search_sort_or_cancel"]).text
            self.assertEqual("取消", cancel, "===失败-点击输入框关键字一键删除按钮，清空失败===")

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_gdcz_p0(self):
        """查关系-关系图，更多操作校验"""
        log.info(self.test_002_cgx_gdcz_p0.__doc__)
        try:
            self.into_middle_page()
            # 断言-展示默认关系占位图（马云-赵薇）
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["relation_empty"]),
                "===失败-未展示查关系占位图===",
            )
            # 断言-进入搜索中间页
            self.new_find_element(By.ID, self.ELEMENT["from_input_textview"]).click()
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["search_contacts"]),
                "===失败-未显示身边老板入口===",
            )
            # 断言-输入起始节点
            self.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).send_keys("北京金堤科技有限公司")
            cancel = self.new_find_element(By.ID, self.ELEMENT["search_sort_or_cancel"]).text
            self.assertEqual(cancel, "排序", "===失败-输入起始节点失败===")
            # 断言-回填起始节点
            self.new_find_element(By.XPATH, self.ELEMENT["from_target_item_1"]).click()
            self.assertEqual(
                self.new_find_element(By.ID, self.ELEMENT["from_input_textview"]).text,
                "北京金堤科技有限公司",
                "===失败-回填起始节点错误===",
            )
            # 断言-输入一个关键词，查关系按钮不可点
            attr = self.new_find_element(By.ID, self.ELEMENT["discover_btn"]).get_attribute("enabled")
            self.assertEqual(attr, "false", "===失败-查关系按钮未置灰===")
            # 断言-输入两个关键词，查关系按钮可点
            self.new_find_element(By.ID, self.ELEMENT["to_input_textview"]).click()
            self.new_find_element(By.ID, self.ELEMENT["search_input_edit"]).send_keys("盐城金堤科技有限公司")
            self.new_find_element(By.XPATH, self.ELEMENT["from_target_item_1"]).click()
            attr = self.new_find_element(By.ID, self.ELEMENT["discover_btn"]).get_attribute("enabled")
            self.assertEqual(attr, "true", "===失败-查关系按钮置灰===")
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["more_operation_btn"]),
                "===失败-未展示更多操作按钮===",
            )
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["clear_all"]),
                "===失败-未展示一键清空按钮===",
            )
            # 断言-输入完关键词后，点开查关系
            self.new_find_element(By.ID, self.ELEMENT["discover_btn"]).click()
            # 断言-关系图，更多操作-分享按钮
            self.new_find_element(By.ID, self.ELEMENT["more_operation_btn"]).click()
            self.new_find_element(By.ID, self.ELEMENT["map_more_share"]).click()
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["btn_wechat_friends"]),
                "===失败-关系图-更多操作-分享弹框-微信好友===",
            )
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["btn_wechat_pengyouquan"]),
                "===失败-关系图-更多操作-分享弹框-微信朋友圈===",
            )
            self.new_find_element(By.ID, self.ELEMENT["share_cancel"]).click()
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

        try:
            # 断言-关系图，更多操作-保存按钮
            self.new_find_element(By.ID, self.ELEMENT["more_operation_btn"]).click()
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["map_more_save"]),
                "===失败-关系图-更多操作-保存按钮===",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

        try:
            # 断言-关系图，更多操作-扫一扫按钮
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["map_more_scan"]),
                "===失败-关系图-更多操作-扫一扫按钮===",
            )
            self.new_find_element(By.ID, self.ELEMENT["map_more_scan"]).click()
            self.assertEqual(
                self.ELEMENT["scan_page_title_text"],
                self.new_find_element(By.XPATH, self.ELEMENT["scan_page_title"]).text,
                "===失败-关系图-更多操作扫一扫页title===",
            )
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["bt_scan"]),
                "===失败-关系图-更多操作-扫一扫页，扫一扫按钮===",
            )
            self.new_find_element(By.ID, self.ELEMENT["bt_scan"]).click()
            if self.isElementExist(By.XPATH, self.ELEMENT["permission_btn"]):
                self.new_find_element(By.XPATH, self.ELEMENT["permission_btn"]).click()
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["viewfinder_view"]),
                "===失败-进入扫描页失败===",
            )
            self.driver.keyevent(4)
            self.driver.keyevent(4)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

        try:
            # 断言-关系图，更多操作-删减按钮
            self.new_find_element(By.ID, self.ELEMENT["more_operation_btn"]).click()
            # 断言-关系图更多操作，展示删减按钮
            self.assertTrue(True, "===失败-关系图-更多操作-删减按钮===")
            self.new_find_element(By.ID, self.ELEMENT["map_more_edit"]).click()
            # 断言-关系图更多操作，点击删减按钮，展示取消、确认、撤销按钮
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["btn_cancle"]),
                "===失败-关系图-更多操作-删减操作取消按钮===",
            )
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["btn_save"]),
                "===失败-关系图-更多操作-删减操作确定按钮===",
            )
            # 断言-未删减节点，插销按钮不可点
            self.assertEqual(
                self.new_find_element(
                    By.ID, self.ELEMENT["btn_restore_node"]
                ).get_attribute("enabled"),
                "false",
                "===失败-查关系更多操作-撤销删减操作===",
            )
            self.new_find_element(By.XPATH, self.ELEMENT["relation_point_text"]).click()
            # 断言-删减节点，撤销按钮可点
            self.assertEqual(
                self.new_find_element(
                    By.ID, self.ELEMENT["btn_restore_node"]
                ).get_attribute("enabled"),
                "true",
                "===失败-查关系更多操作-撤销删减操作===",
            )
            # 断言-被删减节点消失
            self.assertFalse(
                self.isElementExist(By.XPATH, self.ELEMENT["relation_point_text"]),
                "===失败-删减节点失败===",
            )
            self.new_find_element(By.ID, self.ELEMENT["btn_restore_node"]).click()
            # 断言-点击撤销按钮，被删减节点恢复
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["relation_point_text"]),
                "===失败-撤销删减查关系节点===",
            )
            # 断言-取消删减按钮，回到关系图页，节点仍存在
            self.new_find_element(By.XPATH, self.ELEMENT["relation_point_text"]).click()
            self.new_find_element(By.ID, self.ELEMENT["btn_cancle"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["relation_point_text"]),
                "===失败-撤销删减查关系节点===",
            )
            # 断言-确定删减按钮，回到关系图，节点消失
            self.new_find_element(By.ID, self.ELEMENT["more_operation_btn"]).click()
            self.new_find_element(By.ID, self.ELEMENT["map_more_edit"]).click()
            self.new_find_element(By.XPATH, self.ELEMENT["relation_point_text"]).click()
            self.new_find_element(By.ID, self.ELEMENT["btn_save"]).click()
            self.assertFalse(
                self.isElementExist(By.XPATH, self.ELEMENT["relation_point_text"]),
                "===失败-删减节点失败===",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_cgx_sszjy_p0(self):
        """查关系-搜索中间页，历史搜索"""
        log.info(self.test_003_cgx_sszjy_p0.__doc__)
        keyWord = None
        keyList = [
            "测试1",
            "测试2",
            "测试3",
            "测试4",
            "测试5",
            "测试6",
            "测试7",
            "测试8",
            "测试9",
            "测试10",
            "测试11",
        ]
        try:
            self.into_middle_page()
            self.new_find_element(By.ID, self.ELEMENT["from_input_textview"]).click()
            for i in range(len(keyList)):
                keyNum = random.randint(1, len(keyList))
                keyWord = keyList[keyNum - 1]
                self.new_find_element(
                    By.ID, self.ELEMENT["search_input_edit"]
                ).send_keys(keyWord)
                self.adb_send_input(
                    By.ID, self.ELEMENT["search_input_edit"], keyWord, self.device
                )
                self.new_find_element(By.ID, self.ELEMENT["search_clean_iv"]).click()
            # 断言-点击热搜词后，生成搜索历史
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["middlepage_search_history"]),
                "===失败-无最近搜索===",
            )
            self.assertFalse(
                self.isElementExist(By.XPATH, self.ELEMENT["middlepage_hot_search"]),
                "===失败-未展示一键清除按钮===",
            )
            self.assertEqual(
                self.new_find_element(
                    By.XPATH, self.ELEMENT["first_search_history"]
                ).text,
                keyWord,
                "===失败-最近搜索词未展示在搜索历史第一位===",
            )
            # 断言-一键清空历史记录-取消清空
            self.new_find_element(
                By.ID, self.ELEMENT["middlepage_search_history_delete"]
            ).click()
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["delte_cancel"]),
                "===失败-二次确认弹窗未弹出===",
            )
            self.new_find_element(By.ID, self.ELEMENT["delte_cancel"]).click()
            self.assertFalse(
                self.isElementExist(By.ID, self.ELEMENT["delete_confirm"]),
                "===失败-二次确认弹窗未关闭===",
            )
            self.assertTrue(
                self.isElementExist(By.ID, self.ELEMENT["middlepage_search_history"]),
                "===失败-取消后，搜索历史未展示===",
            )
            # 断言-一键清空历史记录-确定清空
            self.new_find_element(
                By.ID, self.ELEMENT["middlepage_search_history_delete"]
            ).click()
            self.new_find_element(By.ID, self.ELEMENT["delete_confirm"]).click()
            self.assertTrue(
                self.isElementExist(By.XPATH, self.ELEMENT["middlepage_hot_search"]),
                "===失败-搜索记录未清空===",
            )
            self.assertFalse(
                self.isElementExist(
                    By.ID, self.ELEMENT["middlepage_search_history_delete"]
                ),
                "===失败-一键删除按钮未隐藏===",
            )
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
