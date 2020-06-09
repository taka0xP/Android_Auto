# -*- coding: utf-8 -*-
# @Time    : 2019-12-26 15:40
# @Author  : ZYF
# @File    : test_all_service1.py

import time
import random
import unittest

from Providers.account.account import Account
from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger


log = Logger('金刚区_01').getlog()
class AllServer1(MyTest, Operation):
    """金刚区_01"""
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
        self.adb_send_input(By.ID, self.ELEMENT['search_input'], value , self.device)
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
    def test_001_sy_jgq_p0(self):
        """
        首页金刚区-查老赖入口、找电话、附近公司、企业实名认证、全部
        只做入口校验
        """
        log.info(self.test_001_sy_jgq_p0.__doc__)
        try:
            # 查老赖入口
            self.new_find_elements(By.ID, self.ELEMENT['king_area'])[0].click()
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual('查老赖', page_title, msg='页面title不一致')
            title1 = self.new_find_element(By.ID, self.ELEMENT['cll_title1']).text
            self.assertEqual('什么是“老赖”？', title1, msg='页面标识不一致')
            self.driver.keyevent(4)
            # 找电话
            self.new_find_elements(By.ID, self.ELEMENT['king_area'])[1].click()
            input_value = self.new_find_element(By.ID, self.ELEMENT['search_input']).text
            self.assertEqual('请输入企业名称', input_value, msg='输入提示不一致')
            self.driver.keyevent(4)
            # todo 新版本有变化
            # # 附近公司
            # self.new_find_elements(By.ID, self.ELEMENT['king_area'])[2].click()
            # page_title1 = self.new_find_element(self.ELEMENT['page_title']).text
            # self.assertEqual('附近公司', page_title1, msg='页面title不一致')
            # a = self.isElementExist(By.ID, self.ELEMENT['export_data'])
            # self.assertTrue(a, msg='「导出数据」未找到')
            # self.driver.keyevent(4)
            # 企业实名认证
            self.new_find_elements(By.ID, self.ELEMENT['king_area'])[3].click()
            page_title2 = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual('选择认证套餐', page_title2, msg='页面title不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_002_qbfw_cll_p0(self):
        """
        查老赖已有单独的模块,只做入口校验
        """
        log.info(self.test_002_qbfw_cll_p0.__doc__)
        try:
            self.in_allserver('cll')
            page_title = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual('查老赖', page_title, msg='页面title不一致')
            title1 = self.new_find_element(By.ID, self.ELEMENT['cll_title1']).text
            self.assertEqual('什么是“老赖”？', title1, msg='页面标识不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_003_qbfw_zdh_p0(self):
        """
        找电话功能正常使用
        1、热门搜索
        2、输入搜索—有结果（点击公司/打电话）
        3、输入搜搜索无结果
        4、筛选 ---未做校验
        5、最近搜索（最多展示10）
        6、一键清除
        7、公司详情页跳转
        8、拨打电话
        """
        log.info(self.test_003_qbfw_zdh_p0.__doc__)
        try:
            self.in_allserver('zdh')
            # 随机点击热搜公司
            hot_search = self.hot_search()
            log.info('点击热搜公司:{}'.format(hot_search))
            legal_person = self.new_find_elements(By.ID, self.ELEMENT['legal_person_name'])[0].text
            log.info('法人：{}'.format(legal_person))
            phone = self.new_find_elements(By.ID, self.ELEMENT['phone_num'])[0].text
            log.info('电话：{}'.format(phone))
            address = self.new_find_elements(By.ID, self.ELEMENT['address_ph'])[0].text
            log.info('电话：{}'.format(address))
            cname = self.new_find_elements(By.ID, self.ELEMENT['company'])[0].text
            legal_name = self.new_find_elements(By.ID, self.ELEMENT['legal_person_name'])[0].text
            # 公司详情页跳转
            self.new_find_elements(By.ID, self.ELEMENT['company'])[0].click()
            self.jump_bounced('first_btn')
            time.sleep(2)
            cname1 = self.new_find_element(By.ID, self.ELEMENT['company1']).text
            legal_name1 = self.new_find_element(By.ID, self.ELEMENT['legal_person_name1']).text
            self.assertEqual(cname1, cname, msg='结果页-详情页 公司名称不一致')
            self.assertEqual(legal_name1, legal_name, msg='结果页-详情页 法人名称不一致')
            self.driver.keyevent(4)
            # 导出数据
            self.new_find_element(By.ID, self.ELEMENT['export_data']).click()
            # 获取使用账号
            account = Account()
            acc_vip_name = account.get_account('vip')
            acc_pwd = account.get_pwd()
            log.info("登录VIP账号：".format(acc_vip_name))
            self.hit_login(account=acc_vip_name, password=acc_pwd)
            count = self.count_num(By.ID, self.ELEMENT['search_title'])
            log.info("搜索结果列表页count:{}".format(count))
            # 再次点击导出数据
            self.new_find_element(By.ID, self.ELEMENT['export_data']).click()
            if count > 5000:
                # 选择非增值导出
                self.new_find_element(By.XPATH, self.ELEMENT['free_export']).click()
                self.new_find_element(By.XPATH, self.ELEMENT['email_export']).send_keys('zhangyufeng@tianyancha.com')
            else:
                self.new_find_element(By.XPATH, self.ELEMENT['free_export']).click()
                # self.new_find_element(By.XPATH, self.ELEMENT['email_export']).click()
                self.new_find_element(By.XPATH, self.ELEMENT['email_export1']).send_keys('zhangyufeng@tianyancha.com')
            self.new_find_element(By.XPATH, self.ELEMENT['export_click']).click()
            # 成功页回到搜索结果页
            self.new_find_element(By.ID, self.ELEMENT['success_back']).click()
            # 拨打电话
            phone_num = self.new_find_elements(By.ID, self.ELEMENT['phone_num'])[0].text
            log.info('点击电话：{}'.format(phone_num))
            if phone_num == '暂无信息':
                self.new_find_elements(By.ID, self.ELEMENT['phone_num'])[1].click()
            else:
                self.new_find_elements(By.ID, self.ELEMENT['phone_num'])[0].click()
            a = self.isElementExist(By.ID, self.ELEMENT['num_input'])
            self.assertTrue(a, msg='未找到手机拨号页面')
            self.driver.keyevent(4)
            self.driver.keyevent(4)
            # 输入搜搜索无结果-@@
            self.search_clean()
            self.search_input('@@')
            c = self.isElementExist(By.ID, self.ELEMENT['search_title'])
            self.assertFalse(c, msg='标识存在的话是有结果')
            # 输入搜索—有结果 天眼查/85587728
            self.search_clean()
            d = self.search_input('85587728')
            d1 = self.new_find_elements(By.ID, self.ELEMENT['phone_num'])[0].text
            self.assertIn(d, d1, msg='电话号码in')
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
            # 使用完了要还回去
            account.release_account(acc_vip_name, "vip")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_004_qbfu_fjgs_p0(self):
        """
        附近公司
        1、筛选
        2、导出数据---目前只做了正常的流程
        3、导航
        4、点击「附近公司」item
        """
        log.info(self.test_004_qbfu_fjgs_p0.__doc__)
        try:
            self.in_allserver('fjgs')
            self.jump_bounced('allow_address')
            a = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(a, '附近公司', msg='页面title不匹配')
            b = self.isElementExist(By.ID, self.ELEMENT['export_data'])
            self.assertTrue(b, msg='「导出数据没有找到」')
            # 公司详情页
            cname = self.new_find_elements(By.ID, self.ELEMENT['company3'])[0].text
            # cname_status = self.new_find_elements(By.ID, self.ELEMENT['search_reg_status'])[0].text
            self.new_find_elements(By.ID, self.ELEMENT['company3'])[0].click()
            self.jump_bounced('first_btn')
            cname1 = self.new_find_element(By.ID, self.ELEMENT['company1']).text
            # cname_status_all = self.new_find_elements(By.ID, self.ELEMENT['search_reg_status']).text
            self.assertEqual(cname1, cname, msg='详情页{}-结果页{}不一致'.format(cname1, cname))
            # TODO 标签断言
            # self.assertIn(cname_status, cname_status_all,msg='展示标签应该在公司详情页标签中')
            self.driver.keyevent(4)
            # 导出数据
            self.new_find_element(By.ID, self.ELEMENT['export_data']).click()
            # 获取使用账号
            account = Account()
            acc_vip_name = account.get_account('vip')
            acc_pwd = account.get_pwd()
            log.info("登录VIP账号：".format(acc_vip_name))
            # 使用获取到的账号登录
            self.hit_login(account=acc_vip_name, password=acc_pwd)
            # 选择非增值导出
            self.new_find_element(By.XPATH, self.ELEMENT['free_export']).click()
            self.new_find_element(By.XPATH, self.ELEMENT['email_export']).click()
            self.new_find_element(By.XPATH, self.ELEMENT['email_export']).send_keys('zhangyufeng@tianyancha.com')
            self.new_find_element(By.XPATH, self.ELEMENT['export_click']).click()
            # 成功页回到搜索结果页
            self.new_find_element(By.ID, self.ELEMENT['success_back']).click()
            # 导航
            self.new_find_elements(By.ID, self.ELEMENT['navigation'])[0].click()
            c = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(c, '地图', msg='公司地图导航页')
            # 使用完了要还回去
            account.release_account(acc_vip_name, "vip")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_005_qbfu_qysmrz_p0(self):
        """
        认证套餐页
        立即认证-调起登录
        """
        try:
            self.in_allserver('qysmrz')
            a = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(a, '选择认证套餐', msg='页面跳转不正确')
            # self.new_find_element(By.XPATH, "//*[@class='android.view.View' and @text='下一步']").click()
            # self.hit_login(account='11099990131', password='ef08beca')
            # b = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            # self.assertEqual(b, '企业实名认证', msg='页面跳转不正确')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_006_qbfw_sblb_p0(self):
        """
        1、获取手机通讯录匹配老板/手机无通讯录
        2、搜索（通讯录不一，未做自动化）
        3、更新
        4、点击“公司”
        """
        try:
            self.in_allserver('sblb')
            self.jump_bounced('all_txl')
            time.sleep(0.5)
            self.jump_bounced(ele_key='btn_close_guide')
            a = self.new_find_element(By.XPATH, self.ELEMENT['txl_title']).text
            self.assertEqual(a, '身边老板', msg='页面title不对应')
            # 点击老板公司
            time.sleep(5)
            b = self.isElementExist(By.ID, self.ELEMENT['update_txl'])
            if b:
                cname = self.new_find_elements(By.ID, self.ELEMENT['comapany_name'])[0].text
                self.new_find_elements(By.ID, self.ELEMENT['comapany_name'])[0].click()
                self.jump_bounced('first_btn')
                cname1 = self.new_find_element(By.ID, self.ELEMENT['company1']).text
                self.assertEqual(cname1, cname, msg='身边老板name{} 公司详情页name{}不一样'.format(cname1, cname))
            else:
                log.info('通讯录为空')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_007_qbfu_csh_p0(self):
        """
        1、热门搜索
        2、搜索（有结果/无结果）
        3、点击搜索结果item
        4、税号详情页点击公司名称
        5、最近搜索 10
        6、一键清除
        """
        log.info(self.test_007_qbfu_csh_p0.__doc__)
        try:
            self.in_allserver('csh')
            prompt = self.new_find_element(By.ID, self.ELEMENT['search_input']).text
            self.assertEqual(prompt, '请输入企业名称或统一信用代码', msg='输入框提示信息不正确')
            # 随机点击热搜公司
            self.hot_search()
            a = self.new_find_elements(By.ID, self.ELEMENT['csh_bs'])[0].text
            self.assertEqual(a, '纳税人识别号：')
            # 点击搜索结果item
            b = self.new_find_elements(By.ID, self.ELEMENT['csh_company'])[0].text
            c = self.new_find_elements(By.ID, self.ELEMENT['rate_person_num'])[0].text
            self.new_find_elements(By.ID, self.ELEMENT['csh_company'])[0].click()
            d = self.new_find_element(By.ID, self.ELEMENT['page_title']).text
            self.assertEqual(d, '税号详情', msg='页面title不对应')
            b1 = self.new_find_element(By.ID, self.ELEMENT['rate_comp']).text
            c1 = self.new_find_element(By.ID, self.ELEMENT['rate_sh']).text
            self.assertEqual(b1, b, msg='搜索结果页，税号详情页 公司名称不对应')
            self.assertEqual(c1, c, msg='搜索结果页，税号详情页 税号不对应')
            # 税号详情页点击公司名称跳转
            self.new_find_element(By.ID, self.ELEMENT['rate_comp']).click()
            self.jump_bounced('first_btn')
            time.sleep(2)
            b2 = self.new_find_element(By.ID, self.ELEMENT['company1']).text
            self.assertEqual(b2, b1, msg='公司详情页，税号详情页 公司名称不对应')
            self.driver.keyevent(4)
            self.driver.keyevent(4)
            # 输入搜索无结果-查税号很无猪
            self.search_clean()
            self.search_input('查税号很无猪')
            # 调用输入框右侧搜索按钮
            self.new_find_element(By.ID, self.ELEMENT['tv_search_search']).click()
            b = self.is_toast_exist('无数据')
            self.assertTrue(b, msg='toast提示未捕获')
            c = self.isElementExist(By.ID, self.ELEMENT['search_title'])
            self.assertFalse(c, msg='标识存在的话是有结果')
            # 输入搜索—有结果 天眼查
            self.search_clean()
            self.search_input('天眼查')
            self.new_find_element(By.ID, self.ELEMENT['tv_search_search']).click()
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
                # 调用输入框右侧搜索按钮
                self.new_find_element(By.ID, self.ELEMENT['tv_search_search']).click()
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
