# -*- coding: utf-8 -*-
# @Time    : 2019-12-26 15:40
# @Author  : ZYF
# @File    : test_all_service2.py

import time
import random
import unittest
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger


log = Logger('金刚区_02').getlog()
class AllServer2(MyTest, Operation):
    """金刚区_02"""
    a = Read_Ex()
    ELEMENT = a.read_excel('All_server')

    def in_allserver(self, value, size=1):
        """
        金刚区 全部服务进入对应的入口
        value: 模块名称
        example: cll(查老赖)
        """
        self.value = value
        self.new_find_elements(By.ID, self.ELEMENT['king_area'])[4].click()
        if size is 1:
            pass
        else:
            self.swipeUp()
        self.new_find_element(By.XPATH, self.ELEMENT[self.value]).click()

    def search_input(self, value):
        """
        输入关键字搜索
        """
        self.new_find_element(By.ID, self.ELEMENT['search_input']).send_keys(value)
        self.new_find_element(By.ID, self.ELEMENT['search_icon']).click()
        time.sleep(0.5)
        search_value = self.new_find_element(By.ID, self.ELEMENT['search_input']).text
        return search_value

    def hot_search(self):
        """
        随机点击热门搜索
        """
        nums = self.new_find_elements(By.XPATH, self.ELEMENT['hot_search'])
        num = random.choice(nums)
        hot_search = num.text
        log.info('热门搜索：{}'.format(hot_search))
        num.click()
        return hot_search

    def search_clean(self):
        """
        搜索框一X
        """
        self.new_find_element(By.ID, self.ELEMENT['search_input']).click()
        self.new_find_element(By.ID, self.ELEMENT['search_clean']).click()

    def search_recent_clear(self, default=1):
        """
        一键清除
        最近搜索-清空icon
        """
        self.new_find_element(By.ID, self.ELEMENT['search_recent_clear']).click()
        if default == 1:
            self.new_find_element(By.ID, self.ELEMENT['confirm']).click()
        else:
            self.new_find_element(By.ID, self.ELEMENT['cancel']).click()

    def jump_bounced(self, ele_key='first_btn'):
        """
        跳过弹框
        默认：'我知道了'
        """
        loc = (By.ID, self.ELEMENT[ele_key])
        try:
            e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
            e.click()
        except Exception as e:
            print(e, '没有首次弹框')
            pass

    def is_toast_exist(self, text, timeout=1, poll_frequency=0.5):
        """is toast exist, return True or False
         - text   - 页面上看到的文本内容
         - timeout - 最大超时时间，默认1s
         - poll_frequency  - 间隔查询时间，默认0.5s查询一次
         is_toast_exist( "看到的内容")
        """
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % text)
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.presence_of_element_located(toast_loc))
            return True
        except Exception as e:
            print(e, '未捕获toast提示')
            return False

    def hit_login(self, account='18535081116', password='zyf643163'):
        """
        点击操作正好遇到需要登录的时候使用
        :param account: 账号
        :param password: 密码
        """
        try:
            loc = (By.XPATH, '//*[@class="android.widget.TextView" and @text="短信验证码登录"]')
            login = self.isElementExist(*loc)
            if login:
                self.new_find_element(By.XPATH, "//*[@class='android.widget.TextView' and @text='密码登录']").click()
                self.new_find_element(By.XPATH, "//*[@class='android.widget.EditText' and @text='输入手机号']").send_keys(account)
                self.new_find_element(By.XPATH, "//*[@class='android.widget.EditText' and @text='输入密码']").send_keys(password)
                # 点击勾选协议
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/cb_login_check").click()
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_login").click()
            else:
                pass
        except Exception as e:
            print(e, '用户已登录')
            pass

    @getimage
    def test_008_qbfu_sbzc_p0(self):
        """商标注册-只做了入口校验"""
        log.info(self.test_008_qbfu_sbzc_p0.__doc__)
        try:
            self.in_allserver('sbzc')
            self.hit_login(account='11099990132', password='ef08beca')
            a = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(a, '顾问商标注册', msg='页面title不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_009_qbfu_qyhm_p0(self):
        """
        「企业核名」已有单独的模块
        """
        try:
            pass
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_010_qbfu_zp_p0(self):
        """
        招聘功能正常使用
        1、热门搜索
        2、输入搜索—有结果
        3、输入搜搜索---无结果
        4、筛选-未做校验
        5、最近搜索
        6、一键清除
        7、搜索有结果点击「招聘信息」
        8、招聘信息详情页--点击「数据来源」
        """
        log.info(self.test_010_qbfu_zp_p0.__doc__)
        try:
            self.in_allserver('zp')
            a = self.new_find_element(By.ID, self.ELEMENT['search_input']).text
            self.assertEqual(a, '请输入企业名称、行业或职位', msg='输入框提示信息不正确')
            # 随机点击热搜公司
            self.hot_search()
            a = self.isElementExist(By.ID, self.ELEMENT['zp_result'])
            self.assertTrue(a, msg='结果页存在数据list')
            # 点击搜索结果item
            b = self.new_find_elements(By.ID, self.ELEMENT['job_title'])[0].text
            c = self.new_find_elements(By.ID, self.ELEMENT['job_address'])[0].text
            self.new_find_elements(By.ID, self.ELEMENT['job_title'])[0].click()
            d = self.new_find_element(By.ID, self.ELEMENT['court_detail_tv_title']).text
            self.assertEqual(d, '招聘详情', msg='页面title不对应')
            b1 = self.new_find_element(By.ID, self.ELEMENT['job_title']).text
            c1 = self.new_find_element(By.ID, self.ELEMENT['job_city']).text
            self.assertEqual(b1, b, msg='搜索结果页，招聘详情页 职位不对应')
            self.assertEqual(c1, c, msg='搜索结果页，招聘详情页 地址不对应')
            # 招聘详情页点击公司名称跳转
            e = self.new_find_element(By.ID, self.ELEMENT['job_company_name']).text
            self.new_find_element(By.ID, self.ELEMENT['job_company_name']).click()
            self.jump_bounced('first_btn')
            e2 = self.new_find_element(By.ID, self.ELEMENT['company1']).text
            self.assertEqual(e2, e, msg='公司详情页，招聘详情页 公司名称不对应')
            self.driver.keyevent(4)
            # 招聘详情页有数据来源
            url = self.isElementExist(By.ID, self.ELEMENT['job_url'])
            self.assertTrue(url, msg='数据来源未找到')
            self.driver.keyevent(4)
            # 点击搜索结果关联公司
            f = self.new_find_elements(By.ID, self.ELEMENT['job_company'])[0].text
            self.new_find_elements(By.ID, self.ELEMENT['job_company'])[0].click()
            self.jump_bounced()
            f1 = self.new_find_element(By.ID, self.ELEMENT['company1']).text
            self.assertEqual(f1, f, msg='搜索结果页关联公司与公司详情页公司 不一致')
            self.driver.keyevent(4)
            # 输入搜索无结果-保德县树林食品加工坊
            self.search_clean()
            self.search_input('保德县树林食品加工坊')
            b = self.is_toast_exist('无数据')
            self.assertTrue(b, msg='toast提示未捕获')
            c = self.isElementExist(By.ID, self.ELEMENT['search_title'])
            self.assertFalse(c, msg='标识存在的话是有结果')
            # 输入搜索—有结果 天眼查
            self.search_clean()
            self.search_input('天眼查')
            e = self.isElementExist(By.ID, self.ELEMENT['search_title'])
            self.assertTrue(e, msg='标识不存在的话是无结果')
            self.search_clean()
            # 一键清除
            self.search_recent_clear(2)
            f = self.isElementExist(By.ID, self.ELEMENT['search_recent_clear'])
            self.assertTrue(f, msg='一键清除-取消，最近搜索按钮还存在')
            self.search_recent_clear()
            g = self.isElementExist(By.ID, self.ELEMENT['search_recent_clear'])
            self.assertFalse(g, msg='一键清除-确认，最近搜索按钮不存在')
            h = self.isElementExist(By.XPATH, self.ELEMENT['hotsearch_bs'])
            self.assertTrue(h, msg='一键清除不存在，「热门搜素」存在')
            # 最近搜索记录
            name_list = ['马云', '孙凯', '王四会', '马丁', '韩磊', '李明', '向小叶', '蓝小凯', '李晓凯', '朱小凯', '赵小凯', '陈小凯']
            for name in name_list:
                log.info('输入搜索词：{}'.format(name))
                self.search_input(name)
                self.search_clean()
            history_words = self.new_find_elements(By.XPATH, self.ELEMENT['hot_search'])
            for i in range(10):
                log.info("历史:{} vs 输入:{}".format(history_words[i].text, name_list[11 - i]))
                self.assertEqual(history_words[i].text, name_list[11 - i], '名字顺序不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_011_qbfu_ztb_p0(self):
        """
        招投标功能正常使用
        1、热门搜索
        2、输入搜索—有结果
        3、输入搜搜索---无结果
        4、招投标详情
        5、最近搜索
        6、一键清除
        7、搜索有结果点击「招投标」
        8、招投标信息详情页--点击「来源链接」
        """
        log.info(self.test_011_qbfu_ztb_p0.__doc__)
        try:
            self.in_allserver('ztb')
            a = self.new_find_element(By.ID, self.ELEMENT['search_input']).text
            self.assertEqual(a, '请输入企业名称', msg='输入框提示信息不正确')
            # 随机点击热搜公司
            self.hot_search()
            a = self.isElementExist(By.ID, self.ELEMENT['zp_result'])
            self.assertTrue(a, msg='结果页存在数据list')
            # 点击搜索结果item
            b = self.new_find_elements(By.ID, self.ELEMENT['company'])[0].text
            log.info("招投标-标题:{}".format(b))
            self.new_find_elements(By.ID, self.ELEMENT['company'])[0].click()
            d = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(d, '招投标详情', msg='页面title不对应')
            b1 = self.new_find_element(By.XPATH, self.ELEMENT['page_bt']).text
            log.info("招投标详情页-标题:{}".format(b1))
            self.assertEqual(b1, b, msg='搜索结果页，招投标详情页 标题不对应')
            # TODO 详情页数据来源目前发现有2种类型 中国移动通信集团有限公司
            # # 招投标详情页点击公司名称跳转
            # e = self.new_find_element(By.XPATH, self.ELEMENT['associated']).text
            # self.new_find_element(By.ID, self.ELEMENT['associated']).click()
            # self.jump_bounced('first_btn')
            # e2 = self.new_find_element(By.ID, self.ELEMENT['company1']).text
            # self.assertEqual(e2, e, msg='公司详情页，招投标详情页关联公司 公司名称不对应')
            # self.driver.keyevent(4)
            # # 招聘详情页有数据来源
            # url = self.isElementExist(By.XPATH, self.ELEMENT['link'])
            # self.assertTrue(url, msg='数据来源未找到')
            self.driver.keyevent(4)
            # 输入搜索无结果-保德县树林食品加工坊
            self.search_clean()
            self.search_input('保德县树林食品加工坊')
            b = self.is_toast_exist('无数据')
            self.assertTrue(b, msg='toast提示未捕获')
            c = self.isElementExist(By.ID, self.ELEMENT['search_title'])
            self.assertFalse(c, msg='标识存在的话是有结果')
            # 输入搜索—有结果 天眼查
            self.search_clean()
            self.search_input('天眼查')
            e = self.isElementExist(By.ID, self.ELEMENT['search_title'])
            self.assertTrue(e, msg='标识不存在的话是无结果')
            self.search_clean()
            # 一键清除
            self.search_recent_clear(2)
            f = self.isElementExist(By.ID, self.ELEMENT['search_recent_clear'])
            self.assertTrue(f, msg='一键清除-取消，最近搜索按钮还存在')
            self.search_recent_clear()
            g = self.isElementExist(By.ID, self.ELEMENT['search_recent_clear'])
            self.assertFalse(g, msg='一键清除-确认，最近搜索按钮不存在')
            h = self.isElementExist(By.XPATH, self.ELEMENT['hotsearch_bs'])
            self.assertTrue(h, msg='一键清除不存在，「热门搜素」存在')
            # 最近搜索记录
            name_list = ['马云', '孙凯', '王四会', '马丁', '韩磊', '李明', '向小叶', '蓝小凯', '李晓凯', '朱小凯', '赵小凯', '陈小凯']
            for name in name_list:
                log.info('输入搜索词：{}'.format(name))
                self.search_input(name)
                self.search_clean()
            history_words = self.new_find_elements(By.XPATH, self.ELEMENT['hot_search'])
            for i in range(10):
                log.info("历史:{} vs 输入:{}".format(history_words[i].text, name_list[11 - i]))
                self.assertEqual(history_words[i].text, name_list[11 - i], '名字顺序不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_012_qbfu_zq_p0(self):
        """
        债券功能正常使用
        1、热门搜索
        2、输入搜索—有结果
        3、输入搜搜索---无结果
        4、最近搜素
        5、一键清除
        6、搜索有结果点击查看详情
        7、债券信息详情页点击「发行人」
        """
        log.info(self.test_012_qbfu_zq_p0.__doc__)
        try:
            self.in_allserver('zq')
            a = self.new_find_element(By.ID, self.ELEMENT['search_input']).text
            self.assertEqual(a, '请输入发行人、债券代码或债券名称', msg='输入框提示信息不正确')
            # 随机点击热搜公司
            self.hot_search()
            a = self.isElementExist(By.ID, self.ELEMENT['zp_result'])
            self.assertTrue(a, msg='结果页存在数据list')
            # 点击搜索结果item
            b = self.new_find_elements(By.ID, self.ELEMENT['item_name'])[0].text
            c = self.new_find_elements(By.ID, self.ELEMENT['fxr_name'])[0].text
            self.new_find_elements(By.ID, self.ELEMENT['item_name'])[0].click()
            d = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(d, '债券信息详情', msg='页面title不对应')
            b1 = self.new_find_element(By.ID, self.ELEMENT['bond_name']).text
            c1 = self.new_find_element(By.ID, self.ELEMENT['fxr_name1']).text
            self.assertEqual(b1, b, msg='搜索结果页，债券信息详情页 标题不对应')
            self.assertEqual(c1, c, msg='搜索结果页，债券详情页 发行人不对应')
            # 债券详情页点击公司名称跳转
            e = self.new_find_element(By.ID, self.ELEMENT['fxr_name1']).text
            self.new_find_element(By.ID, self.ELEMENT['fxr_name1']).click()
            self.jump_bounced('first_btn')
            e2 = self.new_find_element(By.ID, self.ELEMENT['company1']).text
            self.assertEqual(e2, e, msg='公司详情页，债券信息详情页「发行人」 公司名称不对应')
            self.driver.keyevent(4)
            self.driver.keyevent(4)
            # 输入搜索无结果-知春路
            self.search_clean()
            self.search_input('知春路')
            b = self.is_toast_exist('无数据')
            self.assertTrue(b, msg='toast提示未捕获')
            c = self.isElementExist(By.ID, self.ELEMENT['search_title'])
            self.assertFalse(c, msg='标识存在的话是有结果')
            # 输入搜索—有结果 建设银行
            self.search_clean()
            self.search_input('建设银行')
            e = self.isElementExist(By.ID, self.ELEMENT['search_title'])
            self.assertTrue(e, msg='标识不存在的话是无结果')
            self.search_clean()
            # 一键清除
            self.search_recent_clear(2)
            f = self.isElementExist(By.ID, self.ELEMENT['search_recent_clear'])
            self.assertTrue(f, msg='一键清除-取消，最近搜索按钮还存在')
            self.search_recent_clear()
            g = self.isElementExist(By.ID, self.ELEMENT['search_recent_clear'])
            self.assertFalse(g, msg='一键清除-确认，最近搜索按钮不存在')
            h = self.isElementExist(By.XPATH, self.ELEMENT['hotsearch_bs'])
            self.assertTrue(h, msg='一键清除不存在，「热门搜素」存在')
            # 最近搜索记录
            name_list = ['马云', '孙凯', '王四会', '马丁', '韩磊', '李明', '向小叶', '蓝小凯', '李晓凯', '朱小凯', '赵小凯', '陈小凯']
            for name in name_list:
                log.info('输入搜索词：{}'.format(name))
                self.search_input(name)
                self.search_clean()
            history_words = self.new_find_elements(By.XPATH, self.ELEMENT['hot_search'])
            for i in range(10):
                log.info("历史:{} vs 输入:{}".format(history_words[i].text, name_list[11 - i]))
                self.assertEqual(history_words[i].text, name_list[11 - i], '名字顺序不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception


if __name__ == '__main__':
    unittest.main()
