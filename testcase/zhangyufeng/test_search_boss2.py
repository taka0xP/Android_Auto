# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : ZYF
# @File    : search_boss_test2.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
import time, unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger

log = Logger('查老板_2').getlog()
class Search_bossTest2(MyTest, Operation):
    """查老板_02"""
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
    def test_017_CLB_SYZJY_p0(self):
        """搜索中间页最近浏览的功能-最多10条记录"""
        log.info(self.test_017_CLB_SYZJY_p0.__doc__)
        try:
            a = self.is_login()
            if a:
                pass
            else:
                self.login(11099990134, 'ef08beca')
            self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
            self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
            name_list = ['马云', '孙凯', '王四会', '马丁', '韩磊', '李明', '向小叶', '蓝小凯', '李晓凯', '朱小凯', '赵小凯', '陈小凯']
            for i in range(len(name_list)):
                self.adbSend_appium(self.device)
                self.new_find_element(By.ID, self.ELEMENT['search_box1']).send_keys(name_list[i])
                self.adbSend_input(self.device)
                self.new_find_elements(By.ID, self.ELEMENT['all_company'])[1].click()
                loc = (By.ID, self.ELEMENT['first_btn'])
                try:
                    e = WebDriverWait(self.driver, 1, 0.5).until(EC.presence_of_element_located(loc))
                    e.click()
                except Exception as e:
                    # print(e, '没有首次弹框')
                    pass
                self.new_find_element(By.ID, self.ELEMENT['people_back']).click()
                self.new_find_element(By.ID, self.ELEMENT['clean_button']).click()
                i += 1
                print(i)
            self.adbSend_appium(self.device)
            # self.new_find_element(By.ID, self.ELEMENT['search_clean']).click()
            # self.new_find_element(By.ID, self.ELEMENT['confirm_clean']).click()
            print('搜索%s次' %i)
            value = len(self.new_find_elements(By.XPATH, self.ELEMENT['Browsing_history']))
            print('页面展示最近浏览记录%s次' % value)
            self.assertEqual(10, value, '搜索查看12次目前展示%s个最近搜索' % value)
            # 最近浏览清除
            self.new_find_element(By.ID, self.ELEMENT['Browsing_clean']).click()
            self.new_find_element(By.ID, self.ELEMENT['confirm_clean']).click()
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_018_CLB_SYZJY_p0(self):
        """最近搜索-一键清除按钮-确认"""
        log.info(self.test_018_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
            self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
            a = self.new_find_element(By.ID, self.ELEMENT['Recent_search'])
            if a is None:
                self.adb_send_input(By.ID, self.ELEMENT['search_box1'], '马云', self.device)
                log.info("输入搜索词：{}".format("马云"))
                self.new_find_element(By.ID, self.ELEMENT['clean_button']).click()
                self.new_find_element(By.ID, self.ELEMENT['search_clean']).click()
                self.new_find_element(By.ID, self.ELEMENT['confirm_clean']).click()
            else:
                self.new_find_element(By.ID, self.ELEMENT['search_clean']).click()
                self.new_find_element(By.ID, self.ELEMENT['confirm_clean']).click()
            time.sleep(0.5)
            self.assertFalse(self.isElementExist((By.ID, self.ELEMENT['Recent_search'])), '页面还有最近搜索标识')
            self.assertFalse(self.Element('最近搜索'), '最近搜索标识还在')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_019_CLB_SYZJY_p0(self):
        """最近搜索-一键清除按钮-取消"""
        log.info(self.test_019_CLB_SYZJY_p0.__doc__)
        try:
            self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
            self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
            a = self.new_find_element(By.ID, self.ELEMENT['Recent_search'])
            if a is None:
                self.adb_send_input(By.ID, self.ELEMENT['search_box1'], '马云', self.device)
                self.new_find_element(By.ID, self.ELEMENT['clean_button']).click()
                self.new_find_element(By.ID, self.ELEMENT['search_clean']).click()
                self.new_find_element(By.ID, self.ELEMENT['cancel_clean']).click()
            else:
                self.new_find_element(By.ID, self.ELEMENT['search_clean']).click()
                self.new_find_element(By.ID, self.ELEMENT['cancel_clean']).click()
            self.assertTrue(self.Element('最近搜索'), '在页面上找不到最近搜索标识')
            self.assertTrue(self.isElementExist(By.ID, self.ELEMENT['Recent_search']), '页面找不到最近搜索标识')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_020_CLB_SYZJY_p0(self):
        """最近浏览-一键清除按钮-确认"""
        log.info(self.test_020_CLB_SYZJY_p0.__doc__)
        try:
            a = self.is_login()
            if a:
                pass
            else:
                self.login(11099990134, 'ef08beca')
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
                    print(e, '没有首次弹框')
                    pass
                self.new_find_element(By.ID, self.ELEMENT['people_back']).click()
                self.new_find_element(By.ID, self.ELEMENT['clean_button']).click()
                self.new_find_element(By.ID, self.ELEMENT['Browsing_clean']).click()
                self.new_find_element(By.ID, self.ELEMENT['confirm_clean']).click()
            else:
                self.new_find_element(By.ID, self.ELEMENT['Browsing_clean']).click()
                self.new_find_element(By.ID, self.ELEMENT['confirm_clean']).click()
            self.assertFalse(self.isElementExist((By.ID, self.ELEMENT['Recent_browse'])), '页面上还有最近浏览标识')
            self.assertFalse(self.Element('最近浏览'), '在页面上还有最近浏览标识')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_021_CLB_SYZJY_p0(self):
        """最近浏览-一键清除按钮-取消"""
        log.info(self.test_021_CLB_SYZJY_p0.__doc__)
        try:
            a = self.is_login()
            if a:
                pass
            else:
                self.login(11099990134, 'ef08beca')
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
                    print(e, '没有首次弹框')
                    pass
                self.new_find_element(By.ID, self.ELEMENT['people_back']).click()
                self.new_find_element(By.ID, self.ELEMENT['clean_button']).click()
                self.new_find_element(By.ID, self.ELEMENT['Browsing_clean']).click()
                self.new_find_element(By.ID, self.ELEMENT['cancel_clean']).click()
            else:
                self.new_find_element(By.ID, self.ELEMENT['Browsing_clean']).click()
                self.new_find_element(By.ID, self.ELEMENT['cancel_clean']).click()
            time.sleep(1)
            a = self.isElementExist(By.ID, self.ELEMENT['Recent_browse'])
            print(a)
            self.assertTrue(a, '页面找不到最近搜索标识')
            self.assertTrue(self.Element('最近浏览'), '在页面上找不到最近搜索标识')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception


if __name__ == '__main__':
    unittest.main()
