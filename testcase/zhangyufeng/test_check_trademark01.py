# -*- coding: utf-8 -*-
# @Time    : 2020-03-17 09:57
# @Author  : ZYF
# @File    : test_check_trademark01.py
import time
import random
import unittest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger, error_format
from common.check_rules import *
log = Logger("查商标").getlog()


class Trademark01(MyTest, Operation):
    """查商标"""

    a = Read_Ex()
    ELEMENT = a.read_excel("All_server")

    def in_allserver(self, value, size=1):
        """
        金刚区 全部服务进入对应的入口
        value: 模块名称
        example: cll(查老赖)
        """
        self.value = value
        self.new_find_elements(By.ID, self.ELEMENT["king_area"])[4].click()
        if size is 1:
            pass
        else:
            self.swipeUp()
        self.new_find_element(By.XPATH, self.ELEMENT[self.value]).click()

    def search_input(self, type, value):
        """
        随机选择搜索方式-type:
            1、精准名称
            2、近似名称
            3、申请/注册号
            4、申请人名称
            5、代理/办理机构
        输入关键字搜索-value
        """
        self.new_find_element(By.ID, self.ELEMENT["search_type"]).click()  # 点击搜索方式拉起筛选
        a = self.new_find_elements(By.ID, self.ELEMENT["search_types"])
        # type = random.choice(types)
        # choose = type.text
        # log.info('选择的搜索方式是：{}'.format(choose))
        # type.click()
        if type is "1":
            a[0].click()
        elif type is "2":
            a[1].click()
            # 近似名称二级筛选(默认全选)
            self.new_find_element(By.XPATH, self.ELEMENT["all_choose"]).click()
            self.new_find_element(By.ID, self.ELEMENT["approximate_confirm"]).click()
        elif type is "3":
            a[2].click()
        elif type is "4":
            a[3].click()
        elif type is "5":
            a[4].click()
        self.new_find_element(By.ID, self.ELEMENT["search_brand_input"]).click()
        self.adb_send_input(
            By.ID, self.ELEMENT["search_brand_input"], value, self.device
        )
        search_value = self.new_find_element(
            By.ID, self.ELEMENT["search_brand_input"]
        ).text
        type = self.new_find_element(By.ID, self.ELEMENT["search_type"]).text
        return type, search_value

    def hot_search(self, value=1):
        """
        随机点击热搜商标
        """
        if value != 1:
            nums = self.new_find_elements(By.XPATH, self.ELEMENT["hot_csb2"])
            num = random.choice(nums)
            hot_search = num.text
            log.info("查商标搜索中间页热门搜索：{}".format(hot_search))
            num.click()
        else:
            nums = self.new_find_elements(By.XPATH, self.ELEMENT["hot_csb"])
            num = random.choice(nums)
            hot_search = num.text
            log.info("查商标页热门搜索：{}".format(hot_search))
            num.click()
        return hot_search

    def search_clean(self):
        """
        查商标搜索结果列表页 搜索框一X
        """
        self.new_find_element(By.ID, self.ELEMENT["search_brand_input"]).click()
        self.new_find_element(By.ID, self.ELEMENT["brand_clean"]).click()
        input_ts = self.new_find_element(By.ID, self.ELEMENT["search_brand_input"]).text
        return input_ts

    def search_recent_clear(self, default=1):
        """
        一键清除
        最近搜索-清空icon
        """
        self.new_find_element(By.ID, self.ELEMENT["history_clear"]).click()
        if default == 1:
            self.new_find_element(By.ID, self.ELEMENT["confirm"]).click()
        else:
            self.new_find_element(By.ID, self.ELEMENT["cancel"]).click()

    def is_toast_exist(self, text, timeout=1, poll_frequency=0.5):
        """is toast exist, return True or False
         - text   - 页面上看到的文本内容
         - timeout - 最大超时时间，默认1s
         - poll_frequency  - 间隔查询时间，默认0.5s查询一次
         is_toast_exist( "看到的内容")
        """
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                EC.presence_of_element_located(toast_loc)
            )
            return True
        except Exception as e:
            print(e, "未捕获toast提示")
            return False

    def count_screening(self, value):
        """
        value:提取到的字符串
        :return: 商标筛选列表的count数(取括号里面的数字)
        """
        import re

        # ss = '02类-颜料油漆（2）'
        ss = value
        patten = re.compile(r"(?<=\uff08)\d+(?=\uff09)")
        re = patten.findall(ss)
        count = int(re[0])
        log.info("商标筛选列表页的count:{}".format(count))
        return count

    @getimage
    def test_001_qbfu_csb_p0(self):
        """
        查商标页-点击热搜跳转（精准搜索的搜索结果页）
        查商标搜索中间页-热搜词跳转
        """
        log.info(self.test_001_qbfu_csb_p0.__doc__)
        try:
            # 进入查商标页
            self.in_allserver("csb")
            a = self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).text
            log.info("输入框提示信息：{}".format(a))
            self.assertEqual(a, "输入商标名称，申请号，申请人信息", msg="输入框提示信息不正确")
            b = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            log.info("页面title:{}".format(b))
            self.assertEqual(b, "查商标", msg="页面title不一致")
            # 查商标页点击热搜公司
            hot_name = self.hot_search()
            search_type = self.new_find_element(By.ID, self.ELEMENT["search_type"]).text
            search_value = self.new_find_element(
                By.ID, self.ELEMENT["search_brand_input"]
            ).text
            self.assertEqual(search_type, "精准名称", msg="热搜默认的搜索方式有问题")
            self.assertEqual(search_value, hot_name, msg="热搜商标不一致")
            # 搜索中间页点击热搜公司
            self.new_find_element(
                By.ID, self.ELEMENT["search_brand_input"]
            ).click()  # 点击输入框-展示搜索中间页热门搜索
            hot_name2 = self.hot_search(2)
            search_type = self.new_find_element(By.ID, self.ELEMENT["search_type"]).text
            search_value = self.new_find_element(
                By.ID, self.ELEMENT["search_brand_input"]
            ).text
            self.assertEqual(search_type, "精准名称", msg="热搜默认的搜索方式有问题")
            self.assertEqual(search_value, hot_name2, msg="热搜商标不一致")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_002_qbfu_csb_p0(self):
        """
        查商标页-天眼服务跳转
        """
        log.info(self.test_002_qbfu_csb_p0.__doc__)
        try:
            # 进入查商标页
            self.in_allserver("csb")
            a = self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).text
            log.info("输入框提示信息：{}".format(a))
            self.assertEqual(a, "输入商标名称，申请号，申请人信息", msg="输入框提示信息不正确")
            b = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            log.info("页面title:{}".format(b))
            self.assertEqual(b, "查商标", msg="页面title不一致")
            # 点击「商标续展」
            search1 = self.new_find_element(By.ID, self.ELEMENT["sbxz"])
            sbxz = search1.text
            log.info("点击操作-{}".format(sbxz))
            search1.click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            self.assertEqual(page_title, "商标续展", msg="页面跳转不正确")
            self.driver.keyevent(4)
            # 点击「一键申请」
            search2 = self.new_find_element(By.ID, self.ELEMENT["yjsq"])
            yjsq = search2.text
            log.info("点击操作-{}".format(yjsq))
            search2.click()
            time.sleep(0.5)
            page_title = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            self.assertEqual(page_title, "自助商标注册", msg="页面跳转不正确")
            self.driver.keyevent(4)
            # 点击「商标服务」
            search3 = self.new_find_element(By.ID, self.ELEMENT["sbfw"])
            sbfw = search3.text
            log.info("点击操作-{}".format(sbfw))
            search3.click()
            # time.sleep(1)
            page_title = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            self.assertEqual(page_title, "天眼服务", msg="页面跳转不正确")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_003_qbfw_csb_p0(self):
        """
        查商标页点击输入框跳转搜索中间页
        不同的搜索方式搜索
            精准名称无结果-注册
            精准名称有结果
            精准搜索天眼服务弹框-「立即注册」
            商标搜索结果页-自助商标入口
        """
        log.info(self.test_003_qbfw_csb_p0.__doc__)
        try:
            # 进入查商标页
            self.in_allserver("csb")
            a = self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).text
            log.info("输入框提示信息：{}".format(a))
            self.assertEqual(a, "输入商标名称，申请号，申请人信息", msg="输入框提示信息不正确")
            b = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            log.info("页面title:{}".format(b))
            self.assertEqual(b, "查商标", msg="页面title不一致")
            # 进入到搜索中间页
            self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).click()
            # 精准搜索-搜索无数据
            search = self.search_input(type="1", value="我去你妹的")
            log.info("搜索方式-关键词:{}".format(search))
            result_empty = self.new_find_element(
                By.ID, self.ELEMENT["result_empty"]
            ).text
            self.assertIn(search[1], result_empty)
            c = self.new_find_element(By.ID, self.ELEMENT["empty_register"])
            self.assertIsNotNone(c)
            # 无结果的时候点击「立即注册」
            c.click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            self.assertEqual(page_title, "顾问商标注册", msg="页面title不一致")
            self.driver.keyevent(4)
            # 精准搜索有结果
            value = self.search_input(type="1", value="无缝")
            result_title = self.new_find_elements(By.ID, self.ELEMENT["result_title"])[
                0
            ].text
            self.assertEqual(result_title, value[1])
            d = self.new_find_element(By.ID, self.ELEMENT["header_count"])
            self.assertIsNotNone(d)
            # 校验精准搜索的天眼服务弹框---立即注册
            time.sleep(5)
            Bounced_bs = self.new_find_element(By.XPATH, self.ELEMENT["Bounced_bs"])
            self.assertIsNotNone(Bounced_bs)
            # 点击「立即注册」
            self.new_find_element(By.ID, self.ELEMENT["Register_now"]).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            self.assertEqual(page_title, "顾问商标注册", msg="页面title不一致")
            self.driver.keyevent(4)
            # 点击搜索结果页「浮动商标」
            self.new_find_element(By.ID, self.ELEMENT["Floating_button"]).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["page_title"]).text
            self.assertEqual(page_title, "自助商标注册", msg="页面title不一致")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_004_qbfw_csb_p0(self):
        """
        不同的搜索方式搜索
            近似名称无结果
            近似名称有结果
            近似搜索天眼服务弹框-「在线咨询」
            搜索结果列表页-输入框一键清除
        """
        log.info(self.test_004_qbfw_csb_p0.__doc__)
        try:
            # 进入查商标页
            self.in_allserver("csb")
            a = self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).text
            log.info('输入框提示信息：{}'.format(a))
            self.assertEqual(a, "输入商标名称，申请号，申请人信息", msg="输入框提示信息不正确")
            b = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            log.info("页面title:{}".format(b))
            self.assertEqual(b, "查商标", msg="页面title不一致")
            # 进入到搜索中间页
            self.new_find_element(By.XPATH, self.ELEMENT['input_text']).click()
            # 近似搜索-搜索无结果
            search = self.search_input(type='2', value='我去你妹的我去你妹的')
            log.info('搜索方式-关键词:{}'.format(search))
            result_empty = self.new_find_element(By.ID, self.ELEMENT['result_empty']).text
            self.assertIn(search[1], result_empty)
            c = self.new_find_element(By.ID, self.ELEMENT['empty_register'])
            self.assertIsNotNone(c)
            # 搜索框一键清除
            input_bs = self.search_clean()
            self.assertEqual(input_bs, '请输入商标名称')
            # 近似搜索-搜索有结果
            search = self.search_input(type='2', value='我去你妹的')
            log.info('搜索方式-关键词:{}'.format(search))
            result_title = self.new_find_elements(By.ID, self.ELEMENT['result_title'])[0].text
            # self.assertEqual(result_title, search[1])
            log.info('提取名称：{}'.format(result_title))
            d = self.new_find_element(By.ID, self.ELEMENT['header_count'])
            self.assertIsNotNone(d)
            # 天眼服务弹框在线咨询
            time.sleep(5)
            Bounced_bs = self.new_find_element(By.XPATH, self.ELEMENT['Bounced_bs'])
            self.assertIsNotNone(Bounced_bs)
            # 点击「在线咨询」
            self.new_find_element(By.XPATH, self.ELEMENT['online_consulting']).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(page_title, '在线客服', msg='页面title不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_005_qbfw_csb_p0(self):
        """
        不同的搜索方式搜索
            申请/注册号无结果
            申请/注册号有结果
            申请人名称有结果
            声请人名称无结果
            代理/办理机构无结果
            代理/办理机构有结果
        """
        log.info(self.test_005_qbfw_csb_p0.__doc__)
        try:
            # 进入查商标页
            self.in_allserver("csb")
            a = self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).text
            log.info('输入框提示信息：{}'.format(a))
            self.assertEqual(a, "输入商标名称，申请号，申请人信息", msg="输入框提示信息不正确")
            b = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            log.info("页面title:{}".format(b))
            self.assertEqual(b, "查商标", msg="页面title不一致")
            # 进入到搜索中间页
            self.new_find_element(By.XPATH, self.ELEMENT['input_text']).click()
            # 申请/注册号-搜索无结果
            search = self.search_input(type='3', value='我去你妹的我去你妹的')
            log.info('搜索方式-关键词:{}'.format(search))
            result_empty = self.new_find_element(By.ID, self.ELEMENT['result_empty']).text
            self.assertIn(search[1], result_empty)
            c = self.new_find_element(By.ID, self.ELEMENT['empty_register'])
            self.assertIsNotNone(c)
            # 搜索框一键清除
            input_bs = self.search_clean()
            self.assertEqual(input_bs, '请输入商标申请／注册号')
            # 申请/注册号-搜索有结果
            search = self.search_input(type='3', value='6771131')
            log.info('搜索方式-关键词:{}'.format(search))
            register_code = self.new_find_elements(By.ID, self.ELEMENT['register_code'])[0].text
            self.assertEqual(register_code, search[1])
            log.info('提取申请/注册号：{}'.format(register_code))
            d = self.new_find_element(By.ID, self.ELEMENT['header_count'])
            self.assertIsNotNone(d)
            # 申请人名称-无结果
            search = self.search_input(type='4', value='我就是试试')
            log.info('搜索方式-关键词:{}'.format(search))
            result_empty = self.new_find_element(By.ID, self.ELEMENT['result_empty']).text
            self.assertIn(search[1], result_empty)
            c = self.new_find_element(By.ID, self.ELEMENT['empty_register'])
            self.assertIsNotNone(c)
            # 搜索框一键清除
            input_bs = self.search_clean()
            self.assertEqual(input_bs, '请输入申请人名称')
            # 申请人名称-搜索有结果
            search = self.search_input(type='4', value='大连市商标事务所')
            log.info('搜索方式-关键词:{}'.format(search))
            register_name = self.new_find_elements(By.ID, self.ELEMENT['register_name'])[0].text
            self.assertEqual(register_name, search[1])
            log.info('提取申请人名称：{}'.format(register_code))
            d = self.new_find_element(By.ID, self.ELEMENT['header_count'])
            self.assertIsNotNone(d)
            # 代理/办理机构-无结果
            search = self.search_input(type='5', value='我就是试试')
            log.info('搜索方式-关键词:{}'.format(search))
            result_empty = self.new_find_element(By.ID, self.ELEMENT['result_empty']).text
            self.assertIn(search[1], result_empty)
            c = self.new_find_element(By.ID, self.ELEMENT['empty_register'])
            self.assertIsNotNone(c)
            # 搜索框一键清除
            input_bs = self.search_clean()
            self.assertEqual(input_bs, '请输入代理／办理机构名称')
            # 代理/办理机构-搜索有结果
            search = self.search_input(type='5', value='大连市商标事务所')
            log.info('搜索方式-关键词:{}'.format(search))
            agency = self.new_find_elements(By.ID, self.ELEMENT['agency'])[0].text
            self.assertEqual(agency, search[1])
            log.info('提取代理/办理机构：{}'.format(agency))
            d = self.new_find_element(By.ID, self.ELEMENT['header_count'])
            self.assertIsNotNone(d)
            # 无关键字搜索
            search = self.search_input(type='1', value='')
            log.info('搜索方式-关键词:{}'.format(search))
            toast = self.is_toast_exist('你还没有输入关键词')
            self.assertTrue(toast, msg='未捕获到toast')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_006_qbfw_csb_p0(self):
        """
        商标搜索结果列表页筛选
        商标详情页
        """
        log.info(self.test_006_qbfw_csb_p0.__doc__)
        try:
            # 进入查商标页
            self.in_allserver("csb")
            a = self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).text
            log.info('输入框提示信息：{}'.format(a))
            self.assertEqual(a, "输入商标名称，申请号，申请人信息", msg="输入框提示信息不正确")
            b = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            log.info("页面title:{}".format(b))
            self.assertEqual(b, "查商标", msg="页面title不一致")
            # 查商标页点击热搜公司
            hot_name = self.hot_search()
            search_type = self.new_find_element(By.ID, self.ELEMENT['search_type']).text
            search_value = self.new_find_element(By.ID, self.ELEMENT['search_brand_input']).text
            self.assertEqual(search_type, '精准名称', msg='热搜默认的搜索方式有问题')
            self.assertEqual(search_value, hot_name, msg='热搜商标不一致')
            # 国际分类
            self.new_find_element(By.ID, self.ELEMENT['filter_one']).click()
            A1 = self.new_find_elements(By.ID, self.ELEMENT['filter_content'])
            a1 = random.choice(A1)
            value1 = a1.text
            print(value1, type(value1))
            if value1 == "全选":
                A1[1].click()
                A2 = A1[1].text
                # 选择的筛选count提取
                csr_count = self.count_screening(A2)
            else:
                a1.click()
                # 选择的筛选count提取
                csr_count = self.count_screening(value1)
            self.new_find_element(By.ID, self.ELEMENT['filter_confirm']).click()
            # 结果列表页count展示
            count = self.new_find_element(By.ID, self.ELEMENT['header_count'])
            value = self.count(count)
            log.info('查商标搜索结果列表页展示count:{}'.format(value))
            self.assertEqual(csr_count, value, msg="筛选后即如果count不一致")
            # 当前状态
            self.new_find_element(By.ID, self.ELEMENT['filter_two']).click()
            A1 = self.new_find_elements(By.ID, self.ELEMENT['filter_content'])
            a1 = random.choice(A1)
            value1 = a1.text
            if value1 == "全选":
                A1[1].click()
                A2 = A1[1].text
                # 选择的筛选count提取
                csr_count = self.count_screening(A2)
            else:
                a1.click()
                # 选择的筛选count提取
                csr_count = self.count_screening(value1)
            self.new_find_element(By.ID, self.ELEMENT['filter_confirm']).click()
            # 结果列表页count展示
            count = self.new_find_element(By.ID, self.ELEMENT['header_count'])
            value = self.count(count)
            log.info('查商标搜索结果列表页展示count:{}'.format(value))
            self.assertEqual(csr_count, value, msg="筛选后即如果count不一致")
            # 申请年份
            self.new_find_element(By.ID, self.ELEMENT['filter_three']).click()
            A1 = self.new_find_elements(By.ID, self.ELEMENT['filter_content'])
            a1 = random.choice(A1)
            value1 = a1.text
            if value1 == "全选":
                A1[1].click()
                A2 = A1[1].text
                # 选择的筛选count提取
                csr_count = self.count_screening(A2)
            else:
                a1.click()
                # 选择的筛选count提取
                csr_count = self.count_screening(value1)
            self.new_find_element(By.ID, self.ELEMENT['filter_confirm']).click()
            # 结果列表页count展示
            count = self.new_find_element(By.ID, self.ELEMENT['header_count'])
            value = self.count(count)
            log.info('查商标搜索结果列表页展示count:{}'.format(value))
            self.assertEqual(csr_count, value, msg="筛选后即如果count不一致")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_007_qbfw_csb_p0(self):
        """
        商标搜索中间页最近搜索
        最近搜索-清空
        """
        log.info(self.test_006_qbfw_csb_p0.__doc__)
        try:
            # 进入查商标页
            self.in_allserver("csb")
            a = self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).text
            log.info('输入框提示信息：{}'.format(a))
            self.assertEqual(a, "输入商标名称，申请号，申请人信息", msg="输入框提示信息不正确")
            b = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            log.info("页面title:{}".format(b))
            self.assertEqual(b, "查商标", msg="页面title不一致")
            # 进入商标搜索中间页
            self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).click()
            trademark_list = ['马云', '孙凯', '王四会', '马丁', '韩磊', '李明', '向小叶', '蓝小凯', '李晓凯', '朱小凯', '赵小凯', '陈小凯']
            for i in range(len(trademark_list)):
                self.adbSend_appium(self.device)
                self.search_input('1', trademark_list[i])
                log.info('输入关键词 {} 搜索'.format(trademark_list[i]))
                self.search_clean()
                i += 1
            self.adbSend_appium(self.device)
            print('搜索{}次'.format(i))
            history_words = self.new_find_elements(By.XPATH, self.ELEMENT['tra_recent'])
            value = len(history_words)
            print('页面展示最近浏览记录%s次' % value)
            self.assertEqual(10, value, '搜索查看12次目前展示%s个最近搜索' % value)
            for i in range(10):
                log.info("历史:{} vs 输入:{}".format(history_words[i].text, trademark_list[11 - i]))
                self.assertEqual(history_words[i].text, trademark_list[11 - i], '名字顺序不一致')
            self.assertEqual(10, value, '搜索12次目前展示%s个最近搜索' % value)
            # 最近搜索清空
            self.search_recent_clear(0)
            a = self.new_find_element(By.ID, self.ELEMENT["history_clear"])
            self.assertIsNotNone(a, msg='取消清空-还能找到最近搜索记录')
            self.search_recent_clear()
            b = self.new_find_element(By.ID, self.ELEMENT["history_clear"])
            self.assertIsNone(b, msg='确认清空-找不到最近搜索记录')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception

    @getimage
    def test_008_qbfw_csb_p0(self):
        """
        商标详情页
        """
        log.info(self.test_006_qbfw_csb_p0.__doc__)
        try:
            # 进入查商标页
            self.in_allserver("csb")
            a = self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).text
            log.info('输入框提示信息：{}'.format(a))
            self.assertEqual(a, "输入商标名称，申请号，申请人信息", msg="输入框提示信息不正确")
            b = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            log.info("页面title:{}".format(b))
            self.assertEqual(b, "查商标", msg="页面title不一致")
            # 进入搜索中间页
            self.new_find_element(By.XPATH, self.ELEMENT["input_text"]).click()
            # 查商标页点击热搜公司
            search_value = self.search_input('1', '老干妈')
            log.info('搜索: {} 进入公司详情页'.format(search_value))
            # 搜索结果列表页提取元素值（item1）
            # 搜索结果列表页-商标名称
            result_titles = self.new_find_elements(By.ID, self.ELEMENT['result_title'])
            result_title = result_titles[0].text
            log.info('搜索结果列表页 商标名称:{}'.format(result_title))
            # 搜索结果列表页-申请/注册号
            register_code = self.new_find_elements(By.ID, self.ELEMENT['register_code'])[0].text
            log.info('搜索结果列表页 申请/注册号:{}'.format(register_code))
            # 搜索结果列表页-申请日期
            content_date = self.new_find_elements(By.ID, self.ELEMENT['content_date'])[0].text
            log.info('搜索结果列表页 申请日期:{}'.format(content_date))
            # 搜索结果列表页-国际分类
            result_content_classify = self.new_find_elements(By.ID, self.ELEMENT['result_content_classify'])[0].text
            log.info('搜索结果列表页 国际分类:{}'.format(result_content_classify))
            # 搜索结果列表页-申请人名称
            register_name = self.new_find_elements(By.ID, self.ELEMENT['register_name'])[0].text
            log.info('搜索结果列表页 申请人名称:{}'.format(register_name))
            # 搜索结果列表页-代理/办理机构
            agency = self.new_find_elements(By.ID, self.ELEMENT['agency'])[0].text
            log.info('搜索结果列表页 代理/办理机构:{}'.format(agency))
            # 商标状态
            result_label = self.new_find_elements(By.ID, self.ELEMENT['result_label'])[0].text
            log.info('搜索结果列表页 代理/办理机构:{}'.format(result_label))
            # 进入到商标详情页
            result_titles[0].click()
            log.info('商标基础信息')
            # 商标详情页-商标名称
            result_title1 = self.new_find_element(By.ID, self.ELEMENT['detail_name']).text
            log.info('商标详情页页 商标名称:{}'.format(result_title1))
            # 商标详情页-国际分类
            result_content_classify1 = self.new_find_element(By.ID, self.ELEMENT['detail_cls']).text
            log.info('商标详情页页 国际分类:{}'.format(result_content_classify1))
            # 商标详情页-申请/注册号
            register_code1 = self.new_find_element(By.ID, self.ELEMENT['detail_register_code']).text
            log.info('商标详情页页 国际分类:{}'.format(register_code1))
            # 商标详情页-商标状态
            result_label1 = self.new_find_element(By.ID, self.ELEMENT['detail_status']).text
            log.info('商标详情页页 国际分类:{}'.format(result_label1))
            # 商标详情页-申请日期
            content_date1 = self.new_find_element(By.ID, self.ELEMENT['register_date']).text
            log.info('商标详情页页 申请日期:{}'.format(content_date1))
            # 商标详情页-初审公告期号
            trail_number = self.new_find_element(By.ID, self.ELEMENT['trail_number']).text
            log.info('商标详情页页 初审公告期号:{}'.format(trail_number))
            # 商标详情页-初审公告日期
            trail_date = self.new_find_element(By.ID, self.ELEMENT['trail_date']).text
            log.info('商标详情页页 初审公告日期:{}'.format(trail_date))

            # 商标详情页-注册公告期号
            trail_register_number = self.new_find_element(By.ID, self.ELEMENT['trail_register_number']).text
            log.info('商标详情页页 注册公告期号:{}'.format(trail_register_number))
            # 商标详情页-注册公告日期
            trail_register_date = self.new_find_element(By.ID, self.ELEMENT['trail_register_date']).text
            log.info('商标详情页页 注册公告日期:{}'.format(trail_register_date))
            # 商标详情页-专用权期
            detail_share_option = self.new_find_element(By.ID, self.ELEMENT['detail_share_option']).text
            log.info('商标详情页页 专用权期:{}'.format(detail_share_option))
            # 状态图跳转
            names = self.new_find_elements(By.ID, self.ELEMENT['status_short_btn'])
            name = names[0].text
            names[0].click()
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertIn(name, page_title, msg='页面title不一致')
            self.driver.keyevent(4)
            # 申请人信息
            self.swipeUp(t=1500)
            # 申请人信息-申请人名称（中文）
            register_name1 = self.new_find_element(By.ID, self.ELEMENT['register_name_cn']).text
            log.info('申请人名称（中文）:{}'.format(register_name1))
            self.assertEqual(register_name1, register_name, msg='列表页详情页申请人名称不对应')
            # 申请人名称点击跳转
            self.new_find_element(By.ID, self.ELEMENT['register_name_cn']).click()
            company_n = self.new_find_element(By.ID, self.ELEMENT['company1']).text
            self.assertEqual(company_n, register_name1, msg='申请人名称跳转前后一致')
            self.driver.keyevent(4)
            # 申请人信息-申请地址（中文）
            register_address = self.new_find_element(By.ID, self.ELEMENT['register_address_cn']).text
            log.info('申请地址（中文）:{}'.format(register_address))
            # 申请地址点击跳转
            self.new_find_element(By.ID, self.ELEMENT['register_address_cn']).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(page_title, '公司地图', msg='页面title不一致')
            self.driver.keyevent(4)
            # 申请人信息-申请人名称（英文）
            register_name_en = self.new_find_element(By.ID, self.ELEMENT['register_name_en']).text
            log.info('申请人名称（英文）:{}'.format(register_name_en))
            # 申请人信息-申请地址（英文）
            register_address_en = self.new_find_element(By.ID, self.ELEMENT['register_address_en']).text
            log.info('申请地址（英文）:{}'.format(register_address_en))
            # 代理/办理机构
            agency1 = self.new_find_element(By.ID, self.ELEMENT['detail_agency']).text
            log.info('代理/办理机构:{}'.format(agency1))
            self.assertEqual(agency1, agency, msg='结果列表页/详情页机构展示不一致')
            self.swipeUp(t=1500)
            # 商标流程信息
            # 商标流程信息-时间
            follow_dates = self.new_find_elements(By.ID, self.ELEMENT['follow_date'])
            for i in follow_dates:
                follow_date = i.text
                log.info('商标流程信息时间：{}'.format(follow_date))
                check = check_time(follow_date, True)
                self.assertTrue(check)
            # 商标流程信息-内容
            follow_contents = self.new_find_elements(By.ID, self.ELEMENT['follow_content'])
            for i in follow_contents:
                follow_content = i.text
                log.info('商标流程信息内容：{}'.format(follow_content))
            self.swipeUp()
            # 公告信息
            announcements = self.new_find_elements(By.XPATH, self.ELEMENT['announcement'])
            for i in announcements:
                announcement = i.text
                log.info('商标流程信息内容：{}'.format(announcement))
            # 商品服务项目
            projects = self.new_find_elements(By.XPATH, self.ELEMENT['project'])
            for i in projects:
                project = i.text
                log.info('商品服务项目内容：{}'.format(project))
                self.assertIn(register_code1, project)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise Exception


if __name__ == "__main__":
    unittest.main()
