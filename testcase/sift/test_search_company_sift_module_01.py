# -*- coding: utf-8 -*-
# @Time    : 2020-01-15 09:47
# @Author  : XU
# @File    : test_search_company_sift_module_01.py
# @Software: PyCharm
from common.operation import Operation, getimage
from Providers.sift.sift_opera import SiftOperation
import unittest
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
import random
import re
from Providers.logger import Logger, error_format
from Providers.account.account import Account
import datetime

log = Logger("查公司_更多筛选_01").getlog()


class Search_company_sift(MyTest, Operation):
    """查公司_更多筛选_01"""

    a = Read_Ex()
    ELEMENT = a.read_excel("test_search_company_sift")
    account = Account()
    phone_vip = account.get_account("vip")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sift_opera = SiftOperation(cls.driver, cls.ELEMENT)
        cls.sift_opera.login_vip(cls.phone_vip, cls.account.get_pwd())

    @classmethod
    def tearDownClass(cls):
        cls.account.release_account(cls.phone_vip, 'vip')
        super().tearDownClass()

    def get_company_ssfw(self, selectTarget, inputTarget, index):
        """
        获取公司：搜索范围并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        result = None
        assert_info = ""
        assert_tag_info = ""
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            log.info("搜索范围：{}，筛选无结果".format(selectText))
            self.sift_opera.reset(selectTarget)
        else:
            items = self.sift_opera.random_list()
            log.info("搜索范围：{}，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            if items > 2:
                items = items - 2
            company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_name_path"])
            assert_company = self.new_find_element(By.XPATH, company_xpath).text
            if index == 4 or index == 6:
                tag_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_tag_info_path"])
                assert_tag_info = self.new_find_element(By.XPATH, tag_xpath).text
            if index != 1:
                company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                                  self.ELEMENT["company_info_path"])
                assert_info = self.new_find_element(By.XPATH, company_xpath).text
            log.info("断言公司名称：{}".format(assert_company))
            if index == 1:  # 企业名称
                result = inputTarget in assert_company
            elif index == 4 or index == 6:  # 商标、经营范围
                tag1 = selectText in assert_tag_info
                tag2 = inputTarget in assert_info
                result = tag1 and tag2
            else:
                result = inputTarget, assert_info
            self.sift_opera.reset(selectTarget)
        return result

    def get_company_jglx(self, selectTarget, inputTarget, index):
        """
        获取公司：机构类型并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        result = None
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        tagTemp = 0
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            pass
        else:  # 查公司-「机构类型」筛选
            items = self.sift_opera.random_list()
            log.info("机构类型：「{}」，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_name_path"])
            assert_company = self.new_find_element(By.XPATH, company_xpath).text
            log.info("断言公司名称：{}".format(assert_company))
            group = '//*[@resource-id="com.tianyancha.skyeye:id/rl_label"]/android.view.ViewGroup'
            label_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items), group)
            tags = self.new_find_elements(By.XPATH, label_xpath)
            if index == 1:  # 企业
                result = inputTarget in assert_company
            else:
                if tags is None:
                    result = False
                else:
                    group_text = '//*[@resource-id="com.tianyancha.skyeye:id/rl_label"]/android.view.ViewGroup/android.widget.TextView'
                    for i in range(len(tags)):
                        text_xpath = "{}[{}]{}[{}]".format(self.ELEMENT["company_list"], str(items), group_text,
                                                           str(i + 1))
                        tag = self.new_find_element(By.XPATH, text_xpath, ).text
                        if index == 5:  # 律所
                            if tag != "律所":
                                tagTemp += 1
                        else:
                            if tag != selectText:
                                tagTemp += 1
                    result = len(tags) != tagTemp
        self.sift_opera.reset(selectTarget)
        return result

    def get_company_zczb(self, selectTarget, index=None):
        """
        获取公司：注册资本并断言
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """
        data = {
            1: [{"upper": 100, "lower": 0}],
            2: [{"upper": 200, "lower": 100}],
            3: [{"upper": 500, "lower": 200}],
            4: [{"upper": 1000, "lower": 500}],
            5: [{"upper": 99999999999999999999, "lower": 1000}],
        }
        upper = data[index][0]["upper"]
        lower = data[index][0]["lower"]
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            result = "注册资本：{},筛选无结果".format(selectText)
        else:  # 查公司-「机构类型」筛选
            items = self.sift_opera.random_list()
            log.info("注册资本：「{}」，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_name_path"])
            assert_company = self.new_find_element(By.XPATH, company_xpath).text
            log.info("断言公司名称：{}".format(assert_company))
            Layout_text = '//*[@resource-id="com.tianyancha.skyeye:id/base_info_ll"]/android.widget.LinearLayout[2]/android.widget.TextView[2]'
            text_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items), Layout_text)
            if self.isElementExist(By.XPATH, text_xpath):
                zczbStr = self.new_find_element(By.XPATH, text_xpath).text
                zczbNum = re.findall(r"\d+\.?\d*", zczbStr)
                if zczbNum:
                    if "美元" in zczbStr:  # 美元折算
                        numFilter = float(zczbNum[0]) * 7
                    elif "新台币" in zczbStr:  # 新台币折算
                        numFilter = float(zczbNum[0]) * 0.23 / 10000
                    elif "港" in zczbStr:  # 港币折算
                        numFilter = float(zczbNum[0]) * 0.89
                    elif "日" in zczbStr:  # 日元折算
                        numFilter = float(zczbNum[0]) * 0.064
                    else:
                        numFilter = float(zczbNum[0])
                    log.info("{}-注册资本：{}".format(assert_company, str(numFilter)))
                    result = lower <= numFilter <= upper
                else:
                    log.info("{}-注册资本：{}".format(assert_company, zczbStr))
                    result = index == 1 and "-" is zczbStr
            else:
                result = "===失败-公司详情页，基本信息未展示「注册资本」字段==="
        self.sift_opera.reset(selectTarget)
        return result

    def get_company_zcnx(self, selectTarget, index=None):
        """
        获取公司：注册年限并断言
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """
        result = None
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            result = "注册年限：{},筛选无结果".format(selectText)
        else:  # 查公司-「机构类型」筛选
            items = self.sift_opera.random_list()
            log.info("注册年限：「{}」，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_name_path"])
            assert_company = self.new_find_element(By.XPATH, company_xpath).text
            log.info("断言公司名称：{}".format(assert_company))
            Layout_text = '//*[@resource-id="com.tianyancha.skyeye:id/base_info_ll"]/android.widget.LinearLayout[3]/android.widget.TextView[2]'
            text_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items), Layout_text)
            if self.isElementExist(By.XPATH, text_xpath):
                zcnxStrList = self.new_find_element(By.XPATH, text_xpath).text.split("-")
                log.info("{}-成立日期： {} 年 {} 月 {} 日".format(assert_company, zcnxStrList[0], zcnxStrList[1], zcnxStrList[2]))
                tarTime = datetime.datetime(int(zcnxStrList[0]), int(zcnxStrList[1]), int(zcnxStrList[2]))
                nowTime = datetime.datetime.now()
                subtractDay = nowTime - tarTime
                tarDay = float(subtractDay.days / 365)
                log.info("{}-注册年限：{}年".format(assert_company, str(tarDay)))
                _dict = {
                    1: tarDay < 1,
                    2: 1 <= tarDay < 2,
                    3: 2 <= tarDay < 3,
                    4: 3 <= tarDay < 5,
                    5: 5 <= tarDay < 10,
                    6: 10 <= tarDay,
                }
                for i in _dict.keys():
                    if i == index:
                        result = _dict[index]
                if result is None:
                    result = "===失败-普通筛选-注册年限:{}，断言失败===".format(selectText)
            else:
                result = "===失败-普通筛选-注册年限:{}，断言失败===".format(selectText)
        self.sift_opera.reset(selectTarget)
        return result

    def get_company_qyzt(self, selectTarget):
        """
        获取公司：企业状态并断言
        :param selectTarget: 选中条件
        """
        result = None
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            pass
        else:  # 查公司-「机构类型」筛选
            items = self.sift_opera.random_list()
            log.info("企业状态：「{}」，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_name_path"])
            assert_company = self.new_find_element(By.XPATH, company_xpath).text
            log.info("断言公司名称：{}".format(assert_company))
            reg_id = '//*[@resource-id="com.tianyancha.skyeye:id/search_reg_status_tv"]'
            reg_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items), reg_id)
            reg_text = self.new_find_element(By.XPATH, reg_xpath).text
            result = reg_text
        self.sift_opera.reset(selectTarget)
        return result

    @getimage
    def test_001_cgs_ptsx_ssfw_p0(self):
        """查公司-搜索中间页，普通筛选：搜索范围"""
        log.info(self.test_001_cgs_ptsx_ssfw_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(1)
            num_ssfw = random.randint(1, 6)
            selectTarget, selectText = self.sift_opera.get_key("more_ssfw_title", "more_ssfw", num_ssfw)
            result = self.get_company_ssfw(selectTarget, inputTarget, num_ssfw)
            if result is None:
                log.info("搜索范围：{}，筛选无结果".format(selectText))
            else:
                self.assertTrue(result, "===失败-搜索范围-{}，筛选结果异常===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgs_ptsx_jglx_p0(self):
        """查公司-搜索中间页，普通筛选：机构类型"""
        log.info(self.test_002_cgs_ptsx_jglx_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(1)
            num_jglx = random.randint(1, 7)
            selectTarget, selectText = self.sift_opera.get_key("more_jglx_title", "more_jglx", num_jglx)
            result = self.get_company_jglx(selectTarget, inputTarget, num_jglx)
            if result is None:
                log.info("机构类型：{},筛选无结果".format(selectText))
            else:
                self.assertTrue(result, "===失败-查公司：更多筛选「{}」标签===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_cgs_ptsx_zczb_p0(self):
        """查公司-搜索中间页，普通筛选：注册资本"""
        log.info(self.test_003_cgs_ptsx_zczb_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_zczb = random.randint(1, 5)
            selectTarget, selectText = self.sift_opera.get_key("more_zczb_title", "more_zczb", num_zczb)
            result = self.get_company_zczb(selectTarget, num_zczb)
            if isinstance(result, type("返回值类型为str")):
                log.info(result)
            else:
                self.assertTrue(result, "===失败-注册资本不符合筛选结果===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_004_cgs_ptsx_zcnx_p0(self):
        """查公司-搜索中间页，普通筛选：注册年限"""
        log.info(self.test_004_cgs_ptsx_zcnx_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_zcnx = random.randint(1, 5)
            selectTarget, selectText = self.sift_opera.get_key("more_zcnx_title", "more_zcnx", num_zcnx)
            result = self.get_company_zcnx(selectTarget, num_zcnx)
            if isinstance(result, type("返回值类型为str")):
                log.info(result)
            else:
                self.assertTrue(result, "===失败-普通筛选-注册年限:{}，断言失败===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_005_cgs_ptsx_qyzt_p0(self):
        """查公司-搜索中间页，普通筛选：企业状态"""
        log.info(self.test_005_cgs_ptsx_qyzt_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_qyzt = random.randint(1, 5)
            selectTarget, selectText = self.sift_opera.get_key("more_qyzt_title", "more_qyzt", num_qyzt)
            result = self.get_company_qyzt(selectTarget)
            if result is None:
                log.info("企业状态：{},筛选无结果".format(selectText))
            else:
                self.assertEqual(selectText, result, "===失败-企业状态-{}，筛选结果异常===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
