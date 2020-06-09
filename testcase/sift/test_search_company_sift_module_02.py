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
from Providers.account.account import Account
from Providers.logger import Logger, error_format

log = Logger("查公司_更多筛选_02").getlog()


class Search_company_sift(MyTest, Operation):
    """查公司_更多筛选_02"""

    a = Read_Ex()
    ELEMENT = a.read_excel("test_search_company_sift")
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

    def get_company_zblx(self, selectTarget, index=None):
        """
        获取公司：资本类型并断言
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """
        result = None
        money = ["美", "新台币", "港", "澳", "日", "铢", "盾", "卢", "尼", " 镑", "尔"]
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            pass
        else:  # 查公司-「机构类型」筛选
            items = self.sift_opera.random_list()
            log.info("资本类型：「{}」，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_name_path"])
            assert_company = self.new_find_element(By.XPATH, company_xpath).text
            Layout_text = '//*[@resource-id="com.tianyancha.skyeye:id/base_info_ll"]/android.widget.LinearLayout[2]/android.widget.TextView[2]'
            text_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items), Layout_text)
            zblx_text = self.new_find_element(By.XPATH, text_xpath).text
            log.info("断言公司名称：{}，注册资本：{}".format(assert_company, zblx_text))
            if index == 1:
                if "人民" not in zblx_text:
                    # 若资本类型无币种，则默认归入人民币中，断言无其他币种即通过
                    tag = True
                    for i in money:
                        if i in zblx_text:
                            tag = False
                    result = tag
                else:
                    result = "人民" in zblx_text
            elif index == 2:
                result = "美" in zblx_text
            else:
                tag1 = "人民" not in zblx_text
                tag2 = "美" not in zblx_text
                result = tag1 and tag2
        self.sift_opera.reset(selectTarget)
        return result

    def get_company_qylx(self, selectTarget, index=None):
        """
        获取公司：企业类型并断言
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            result = "企业类型：{}，筛选无结果".format(selectText)
        else:  # 查公司-「机构类型」筛选
            items = self.sift_opera.random_list()
            log.info("企业类型：「{}」，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_name_path"])
            company_name = self.new_find_element(By.XPATH, company_xpath)
            log.info("断言公司名称：{}".format(company_name.text))
            company_name.click()
            result = self.sift_opera.company_type(selectText, index)
        self.sift_opera.back2company_search()
        self.sift_opera.reset(selectTarget)
        return result

    def get_company_cbrs(self, selectTarget, index=None):
        """
        获取公司：参保人数并断言
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """
        result = None
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            log.info("参保人数：{},筛选无结果".format(selectText))
            self.sift_opera.reset(selectTarget)
        else:  # 查公司-「机构类型」筛选
            items = self.sift_opera.random_list()
            log.info("参保人数：「{}」，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            if items > 2:  # 防止item超出页面，无法获取元素
                items = items - 2
            company_xpath = "{}[{}]{}".format(self.ELEMENT["company_list"], str(items),
                                              self.ELEMENT["company_name_path"])
            company_name_ele = self.new_find_element(By.XPATH, company_xpath)
            company_name = company_name_ele.text
            log.info("断言公司名称：{}".format(company_name))
            company_name_ele.click()
            for i in range(20):
                if self.isElementExist(By.XPATH, self.ELEMENT["more_gsxx_dimension"]):
                    self.new_find_element(By.XPATH, self.ELEMENT["more_gsxx_dimension"]).click()
                    # 工商信息维度，查找参保人数字段
                    for j in range(20):
                        if self.isElementExist(By.ID, self.ELEMENT["tv_social_staff_num"]):
                            cbrsStr = self.new_find_element(By.ID, self.ELEMENT["tv_social_staff_num"]).text
                            cbrsNum = re.findall(r"\d+\.?\d*", cbrsStr)
                            log.info("{}-参保人数：{}".format(company_name, cbrsNum[0]))
                            _dict = {
                                1: 0 <= int(cbrsNum[0]),
                                2: 50 <= int(cbrsNum[0]) <= 99,
                                3: 100 <= int(cbrsNum[0]) <= 499,
                                4: 500 <= int(cbrsNum[0]) <= 999,
                                5: 1000 <= int(cbrsNum[0]) <= 4999,
                                6: 5000 <= int(cbrsNum[0]) <= 9999,
                                7: 10000 <= int(cbrsNum[0]),
                            }
                            for k in _dict.keys():
                                if k == index:
                                    result = _dict[index]
                            break
                        else:
                            self.swipeUp(0.5, 0.7, 0.3, 2000)
                            if j == 19:
                                log.info("参保人数断言失败-工商信息详情页，参保人数未找到")
                    break
                else:
                    self.swipeUp(0.5, 0.7, 0.3, 2000)
                    if self.isElementExist(By.XPATH,
                                           '//*[@class="android.widget.TextView" and @text="登记信息"]') and index == 1:
                        log.info("{}，展示「登记信息」无参保人数".format(company_name))
                        result = True
                        break
                    if i == 19:
                        log.info("参保人数断言失败-公司详情页未找到「工商信息」")
        self.sift_opera.back2company_search()
        self.sift_opera.reset(selectTarget)
        return result

    @getimage
    def test_001_cgs_ptsx_zblx_p0(self):
        """查公司-搜索中间页，普通筛选：资本类型"""
        log.info(self.test_001_cgs_ptsx_zblx_p0.__doc__)
        try:
            self.sift_opera.login_vip(self.phone_vip, self.account.get_pwd())
            self.sift_opera.search_key(1)
            num_zblx = random.randint(1, 3)
            selectTarget, selectText = self.sift_opera.get_key("more_zblx_title", "more_zblx", num_zblx)
            result = self.get_company_zblx(selectTarget, num_zblx)
            if result is None:
                log.info("资本类型：{},筛选无结果".format(selectText))
            else:
                self.assertTrue(result, "===失败-更多筛选：资本类型：{}===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgs_ptsx_qylx_p0(self):
        """查公司-搜索中间页，普通筛选：企业类型"""
        log.info(self.test_002_cgs_ptsx_qylx_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_qylx = random.randint(1, 11)
            selectTarget, selectText = self.sift_opera.get_key("more_qylx_title", "more_qylx", num_qylx)
            result = self.get_company_qylx(selectTarget, num_qylx)
            if isinstance(result, type("返回值类型为str")):
                log.info(result)
            else:
                self.assertTrue(result, "===失败-工商信息详情页中，企业类型断言错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_cgs_ptsx_cbrs_p0(self):
        """查公司-搜索中间页，普通筛选：参保人数"""
        log.info(self.test_003_cgs_ptsx_cbrs_p0.__doc__)
        try:
            self.sift_opera.search_key(1)
            num_cbrs = random.randint(1, 7)
            selectTarget, selectText = self.sift_opera.get_key("more_cbrs_title", "more_cbrs", num_cbrs)
            result = self.get_company_cbrs(selectTarget, num_cbrs)
            if result is None:
                pass
            else:
                self.assertTrue(result, "===失败-工商信息详情页中，参保人数断言错误===")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
