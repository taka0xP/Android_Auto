# -*- coding: utf-8 -*-
# @Time    : 2020-02-19 17:45
# @Author  : XU
# @File    : test_search_relation_sift_module_01.py
# @Software: PyCharm
from common.operation import Operation, getimage
import unittest
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from Providers.sift.sift_opera import SiftOperation
from common.ReadData import Read_Ex
import random
import re
from Providers.logger import Logger, error_format
import datetime
from Providers.account.account import Account

log = Logger("查关系_更多筛选_01").getlog()


class Search_relation_sift(MyTest, Operation):
    """查关系_更多筛选_01"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Search_relation")
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

    def get_company_ssfw(self, selectTarget, index):
        """
        获取公司：搜索范围并断言
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """
        result1 = ""
        result2 = ""
        resultList = [
            "more_ssfw_title_company_name_result",
            "more_ssfw_title_holder_result",
            "more_ssfw_title_product_service_result",
            "more_ssfw_title_trademark_result",
            "more_ssfw_title_contact_result",
            "more_ssfw_title_management_result",
            "",
        ]
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            self.sift_opera.reset(selectTarget)
        else:
            log.info("搜索范围：{}".format(selectText))
            if index == 4:
                result1 = self.new_find_element(By.XPATH, self.ELEMENT["more_ssfw_title_trademark_title"]).text
                result2 = self.new_find_element(By.XPATH, self.ELEMENT[resultList[index - 1]]).text
            elif index == 6:
                result1 = self.new_find_element(By.XPATH, self.ELEMENT["more_ssfw_title_management_title"]).text
                result2 = self.new_find_element(By.XPATH, self.ELEMENT[resultList[index - 1]]).text
            else:
                result2 = self.new_find_element(By.XPATH, self.ELEMENT[resultList[index - 1]]).text
            self.sift_opera.reset(selectTarget)
        return result1, result2

    def get_company_jglx(self, selectTarget, inputTarget, index):
        """
        获取公司：机构类型并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        result = None
        selectText = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
        if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
            self.sift_opera.reset(selectTarget)
        else:
            if index == 1:  # 企业
                company_name = self.new_find_element(By.XPATH, self.ELEMENT["more_jglx_title_company_result"]).text
                log.info("更多筛选-机构类型：{}，断言公司名称：{}".format(selectText, company_name))
                self.sift_opera.reset(selectTarget)
                result = company_name
            else:
                self.new_find_element(By.XPATH, self.ELEMENT["from_target_item_1"]).click()
                self.new_find_element(By.XPATH, self.ELEMENT["sky_canvas"]).click()
                company_name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
                log.info("更多筛选-机构类型：{}，断言公司名称：{}".format(selectText, company_name))
                if index == 2:  # 事业单位
                    result = self.new_find_element(By.ID, self.ELEMENT["tv_des_sub_title_2"]).text
                elif index == 3:  # 基金会
                    result = self.new_find_element(By.ID, self.ELEMENT["tv_des_sub_title_2"]).text
                elif index == 4:  # 社会组织
                    result = self.new_find_element(By.ID, self.ELEMENT["tv_des_sub_title_3"]).text
                elif index == 5:  # 律师事务所
                    result = self.new_find_element(By.ID, self.ELEMENT["tv_des_sub_title_1"]).text
                elif index == 6:  # 中国香港企业
                    result = self.new_find_element(By.ID, self.ELEMENT["tv_des_sub_title_2"]).text
                else:  # 中国台湾企业
                    result = self.new_find_element(By.ID, self.ELEMENT["tv_des_sub_title_2"]).text
                self.sift_opera.back2relation_search(inputTarget)
        return result

    def get_company_zczb(self, selectTarget, inputTarget, index=None):
        """
        获取公司：注册资本并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        result1 = None
        result2 = None
        data = {
            1: [{"upper": 100, "lower": 0}],
            2: [{"upper": 200, "lower": 100}],
            3: [{"upper": 500, "lower": 200}],
            4: [{"upper": 1000, "lower": 500}],
            5: [{"upper": 99999999999999999999, "lower": 1000}],
        }
        upper = data[index][0]["upper"]
        lower = data[index][0]["lower"]
        selectText = self.sift_opera.point2company(selectTarget)
        company_name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("更多筛选-注册资本-{}，断言公司名称：{}".format(selectText, company_name))
        if self.isElementExist(By.ID, self.ELEMENT["more_zczb_title_num"]):
            tag = True
            zczbStr = self.new_find_element(By.ID, self.ELEMENT["more_zczb_title_num"]).text
            zczbNum = re.findall(r"\d+\.?\d*", zczbStr)

            if zczbNum:
                if "美元" in zczbStr:  # 美元折算
                    numFilter = float(zczbNum[0]) * 7
                elif "新台币" in zczbStr:  # 新台币折算
                    numFilter = float(zczbNum[0]) * 0.23
                elif "港" in zczbStr:  # 港币折算
                    numFilter = float(zczbNum[0]) * 0.89
                elif "日" in zczbStr:  # 日元折算
                    numFilter = float(zczbNum[0]) * 0.064
                else:
                    numFilter = float(zczbNum[0])
                log.info(company_name + "-注册资本：" + str(numFilter))
                result1 = lower <= numFilter <= upper
            else:
                result1 = index == 1
                result2 = zczbStr
        else:
            tag = False
            result2 = "===失败-公司详情页，基本信息未展示「注册资本」字段==="
        self.sift_opera.back2relation_search(inputTarget)
        return tag, result1, result2

    def get_company_zcnx(self, selectTarget, inputTarget, index=None):
        """
        获取公司：注册年限并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        result = None
        selectText = self.sift_opera.point2company(selectTarget)
        company_name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("更多筛选-注册年限-{}，断言公司名称：{}".format(selectText, company_name))
        if self.isElementExist(By.ID, self.ELEMENT["more_zcnx_title_num"]):
            zcnxStrList = self.new_find_element(By.ID, self.ELEMENT["more_zcnx_title_num"]).text.split(".")
            log.info("{}-成立日期： {} 年 {} 月 {} 日".format(company_name, zcnxStrList[0], zcnxStrList[1], zcnxStrList[2]))
            tarTime = datetime.datetime(int(zcnxStrList[0]), int(zcnxStrList[1]), int(zcnxStrList[2]))
            nowTime = datetime.datetime.now()
            subtractDay = nowTime - tarTime
            tarDay = float(subtractDay.days / 365)
            log.info("{}-注册年限：{}年".format(company_name, str(tarDay)))
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
        self.sift_opera.back2relation_search(inputTarget)
        return result

    def get_company_qyzt(self, selectTarget, inputTarget, index=None):
        """
        获取公司：企业状态并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        tagList = [
            "more_qyzt_title_in_business_tag",
            "more_qyzt_title_subsist_tag",
            "more_qyzt_title_revoke_tag",
            "more_qyzt_title_cancellation_tag",
            "more_qyzt_title_move_out_tag",
        ]
        selectText = self.sift_opera.point2company(selectTarget)
        name = self.new_find_element(By.ID, self.ELEMENT["firm_detail_name_tv"]).text
        log.info("更多筛选-企业状态-{}，断言公司名称：{}".format(selectText, name))
        if self.isElementExist(By.XPATH, self.ELEMENT[tagList[index - 1]]):
            result = self.new_find_element(By.XPATH, self.ELEMENT[tagList[index - 1]]).text
        else:
            result = "在业"
        self.sift_opera.back2relation_search(inputTarget)
        return result

    @getimage
    def test_001_cgx_ptsx_ssfw_p0(self):
        """查关系-搜索中间页，普通筛选：搜索范围"""
        log.info(self.test_001_cgx_ptsx_ssfw_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_ssfw = random.randint(1, 6)
            selectTarget, selectText = self.sift_opera.get_key("more_ssfw_title", "more_ssfw", num_ssfw)
            result1, result2 = self.get_company_ssfw(selectTarget, num_ssfw)
            if result1 is "" and result2 is "":
                log.info("搜索范围：{},筛选无结果".format(selectText))
            else:
                if num_ssfw == 4:
                    self.assertIn("商标", result1, "===失败-搜索范围-{}，筛选结果字段异常===".format(selectText))
                elif num_ssfw == 6:
                    self.assertIn("经营范围", result1, "===失败-搜索范围-{}，筛选结果字段异常===".format(selectText))
                self.assertIn(inputTarget, result2, "===失败-搜索范围-{}，筛选结果异常===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_cgx_ptsx_jglx_p0(self):
        """查关系-搜索中间页，普通筛选：机构类型"""
        log.info(self.test_002_cgx_ptsx_jglx_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_jglx = random.randint(1, 7)
            selectTarget, selectText = self.sift_opera.get_key("more_jglx_title", "more_jglx", num_jglx)
            result = self.get_company_jglx(selectTarget, inputTarget, num_jglx)
            if self.isElementExist(By.ID, self.ELEMENT["more_empty_view"]):
                log.info("机构类型：{},筛选无结果".format(selectText))
            else:
                if num_jglx == 1:  # 企业
                    self.assertIn(inputTarget, result, "===失败-机构类型-企业，筛选结果异常===")
                else:
                    if num_jglx == 2:  # 事业单位
                        self.assertEqual("开办资金", result, "===失败-机构类型-{}，筛选结果异常===".format(selectText))
                    elif num_jglx == 3:  # 基金会
                        self.assertEqual("原始基金", result, "===失败-机构类型-{}，筛选结果异常===".format(selectText))
                    elif num_jglx == 4:  # 社会组织
                        self.assertEqual("成立登记日期", result, "===失败-机构类型-{}，筛选结果异常===".format(selectText))
                    elif num_jglx == 5:  # 律师事务所
                        self.assertEqual("负责人", result, "===失败-机构类型-{}，筛选结果异常===".format(selectText))
                    elif num_jglx == 6:  # 中国香港企业
                        self.assertEqual("股本", result, "===失败-机构类型-{}，筛选结果异常===".format(selectText))
                    else:  # 中国台湾企业
                        self.assertEqual("资本总额", result, "===失败-机构类型-{}，筛选结果异常===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_cgx_ptsx_zczb_p0(self):
        """查关系-搜索中间页，普通筛选：注册资本"""
        log.info(self.test_003_cgx_ptsx_zczb_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_zczb = random.randint(1, 5)
            selectTarget, selectText = self.sift_opera.get_key("more_zczb_title", "more_zczb", num_zczb)
            tag, result1, result2 = self.get_company_zczb(selectTarget, inputTarget, num_zczb)
            if tag:
                self.assertTrue(result1, "===失败-注册资本不符合筛选结果===")
                if result2 is not None:
                    self.assertEqual("-", result2, "===失败-注册资本不符合筛选结果===")
            else:
                log.error(result2)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_004_cgx_ptsx_zcnx_p0(self):
        """查关系-搜索中间页，普通筛选：注册年限"""
        log.info(self.test_004_cgx_ptsx_zcnx_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_zcnx = random.randint(1, 5)
            selectTarget, selectText = self.sift_opera.get_key("more_zcnx_title", "more_zcnx", num_zcnx)
            result = self.get_company_zcnx(selectTarget, inputTarget, num_zcnx)
            self.assertTrue(result, "===失败-普通筛选-注册年限:{}，断言失败===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_005_cgx_ptsx_qyzt_p0(self):
        """查关系-搜索中间页，普通筛选：企业状态"""
        log.info(self.test_005_cgx_ptsx_qyzt_p0.__doc__)
        try:
            inputTarget = self.sift_opera.search_key(2)
            num_qyzt = random.randint(1, 5)
            selectTarget, selectText = self.sift_opera.get_key("more_qyzt_title", "more_qyzt", num_qyzt)
            result = self.get_company_qyzt(selectTarget, inputTarget, num_qyzt)
            self.assertIn(selectText, result, "===失败-企业状态-{}，筛选结果异常===".format(selectText))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
