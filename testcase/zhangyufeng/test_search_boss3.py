# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : ZYF
# @File    : search_boss_test3.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
import time, unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger

log = Logger('查老板_03').getlog()
class Search_bossTest3(MyTest, Operation):
    """查老板_03"""
    a = Read_Ex()
    ELEMENT = a.read_excel('Search_boss')

    def close_guide(self):
        loc = (By.ID, 'com.tianyancha.skyeye:id/btn_close_guide')
        try:
            e = WebDriverWait(self.driver, 2, 0.5).until(EC.presence_of_element_located(loc))
            e.click()
        except:
            pass

    @getimage
    def test_022_CLB_SYZJY_p0(self):
        """搜索中间页-点击最近搜索"""
        log.info(self.test_022_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
            self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
            a = self.new_find_element(By.ID, self.ELEMENT['Recent_search'])
            if a is None:
                self.adb_send_input(By.ID, self.ELEMENT['search_box1'], '马云', self.device)
                log.info("输入搜索词：{}".format("马云"))
                self.new_find_element(By.ID, self.ELEMENT['clean_button']).click()
                name = self.new_find_elements(By.XPATH, self.ELEMENT['Search_records'])[0].text
                self.new_find_elements(By.XPATH, self.ELEMENT['Search_records'])[0].click()
                name1 = self.new_find_element(By.ID, self.ELEMENT['search_box1']).text
            else:
                name = self.new_find_elements(By.XPATH, self.ELEMENT['Search_records'])[0].text
                self.new_find_elements(By.XPATH, self.ELEMENT['Search_records'])[0].click()
                name1 = self.new_find_element(By.ID, self.ELEMENT['search_box1']).text
            self.assertEqual(name, name1, '最近搜索与搜索框老板名称不一致')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_023_CLB_SYZJY_p0(self):
        """搜索中间页-点击最近浏览-登录"""
        log.info(self.test_023_CLB_SYZJY_p0.__doc__)
        try:
            a = self.is_login()
            if a:
                pass
            else:
                self.login(11099990135, 'ef08beca')
            self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
            self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
            a = self.new_find_element(By.ID, self.ELEMENT['Recent_browse'])
            if a is None:
                self.adb_send_input(By.ID, self.ELEMENT['search_box1'], '马云', self.device)
                self.new_find_elements(By.ID, self.ELEMENT['all_company'])[1].click()
                loc = (By.ID, self.ELEMENT['first_btn'])
                try:
                    e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                    e.click()
                except Exception as e:
                    print(e, "没有首次弹框")
                    pass
                self.new_find_element(By.ID, self.ELEMENT['people_back']).click()
                self.new_find_element(By.ID, self.ELEMENT['clean_button']).click()
                self.new_find_elements(By.XPATH, self.ELEMENT['Recent_records'])[0].click()
            else:
                self.new_find_elements(By.XPATH, self.ELEMENT['Recent_records'])[0].click()
            loc = (By.ID, self.ELEMENT['first_btn'])
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                e.click()
            except Exception as e:
                print(e, '没有首次弹框')
                pass
            self.new_find_element(By.ID, self.ELEMENT['name'])
            value = self.new_find_element(By.ID, self.ELEMENT['name']).text
            self.assertTrue(self.Element('人员详情'))
            self.assertIsNotNone(value)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_024_CLB_SYZJY_p0(self):
        """搜索中间页-点击最近浏览-登录"""
        log.info(self.test_024_CLB_SYZJY_p0.__doc__)
        try:
            a = self.is_login()
            if a:
                self.logout()
            else:
                pass
            self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
            self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
            b = self.new_find_element(By.ID, self.ELEMENT['Browsing_clean'])
            if b is None:
                self.adb_send_input(By.ID, self.ELEMENT['search_box1'], '马云', self.device)
                self.new_find_elements(By.ID, self.ELEMENT['all_company'])[1].click()
                self.driver.keyevent(4)
                self.new_find_element(By.ID, self.ELEMENT['clean_button']).click()
                self.new_find_elements(By.XPATH, self.ELEMENT['Recent_records'])[0].click()
                time.sleep(0.5)
            else:
                self.new_find_elements(By.XPATH, self.ELEMENT['Recent_records'])[0].click()
                time.sleep(0.5)
            a = self.isElementExist(By.ID, self.ELEMENT['login_bs'])
            self.assertTrue(a, '登录页标识-->页面元素不存在')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception

    @getimage
    def test_025_CLB_SYdb_p0(self):
        """
        首页底部-查老板，未登录
        点击热门人物可以查看人详情
        点击热门人物合作伙伴拉起登录
        点击搜索框跳转查老板搜索中间页
        """
        log.info(self.test_025_CLB_SYdb_p0.__doc__)
        try:
            a = self.is_login()
            if a:
                self.logout()
            else:
                pass
            self.new_find_element(By.ID, self.ELEMENT['Homepage_2']).click()
            # 点击热门人物
            self.new_find_element(By.XPATH, self.ELEMENT['sensation_1']).click()
            loc = (By.ID, self.ELEMENT['first_btn'])
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                e.click()
            except Exception as e:
                print(e, '没有首次弹框')
                pass
            time.sleep(1)
            self.assertTrue(self.Element('人员详情'))
            self.driver.keyevent(4)
            # 点击搜索框
            self.new_find_element(By.ID, self.ELEMENT['homepage_2_search']).click()
            time.sleep(0.5)
            self.assertTrue(self.Element(self.ELEMENT['found_boss']))
            self.driver.keyevent(4)
            # 点击热门人物合作伙伴
            self.new_find_elements(By.ID, self.ELEMENT['partners'])[0].click()
            time.sleep(0.5)
            a = self.isElementExist(By.ID, self.ELEMENT['login_bs'])
            self.assertTrue(a, '登录页标识-->页面元素不存在')
            # 返回首页
            self.driver.keyevent(4)
            self.new_find_element(By.ID, self.ELEMENT['Homepage_1']).click()
        except AssertionError as ae:
            print(ae)
            raise self.failureException()
        except Exception as e:
            print(e)

    @getimage
    def test_026_CLB_SYdb_p0(self):
        """
        首页底部-查老板，登录
        点击热门人物可以查看人详情
        点击热门人物合作伙伴拉起登录
        点击搜索框跳转查老板搜索中间页
        """
        log.info(self.test_026_CLB_SYdb_p0.__doc__)
        try:
            a = self.is_login()
            if a:
                pass
            else:
                self.login(11099990135, 'ef08beca')
            self.new_find_element(By.ID, self.ELEMENT['Homepage_2']).click()
            # 点击热门人物
            self.new_find_element(By.XPATH, self.ELEMENT['sensation_1']).click()
            loc = (By.ID, self.ELEMENT['first_btn'])
            try:
                e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                e.click()
            except Exception as e:
                print(e, '没有首次弹框')
                pass
            self.assertTrue(self.Element('人员详情'))
            self.driver.keyevent(4)
            # 点击搜索框
            self.new_find_element(By.ID, self.ELEMENT['homepage_2_search']).click()
            time.sleep(0.5)
            self.assertTrue(self.Element(self.ELEMENT['found_boss']))
            self.driver.keyevent(4)
            # 点击热门人物合作伙伴
            name = self.new_find_elements(By.XPATH, self.ELEMENT['partners1'])[0].text
            log.info('热门合作伙伴：{}'.format(name))
            self.new_find_elements(By.ID, self.ELEMENT['partners'])[0].click()
            time.sleep(3)
            name1 = self.new_find_element(By.ID, self.ELEMENT['name']).text
            print(name1)
            self.assertTrue(self.Element('人员详情'))
            self.assertIn(name, name1, '老板名称不对应')
            # 返回首页
            self.driver.keyevent(4)
            self.new_find_element(By.ID, self.ELEMENT['Homepage_1']).click()
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            print(e)
            raise Exception


if __name__ == '__main__':
    unittest.main()
