# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : wlx
# @File    : Human_detailTest.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger, error_format

log = Logger('人员详情_01').getlog()


class Human_detail_Test_1(MyTest, Operation):
    """人员详情_01"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 获取excel
        cls.ELEMENT = Read_Ex().read_excel("human_detail")
        cls.user = cls.account.get_account()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.account.release_account(account=cls.user, account_type="account", account_special="0")
    # a = Read_Ex()
    # ELEMENT = a.read_excel('Human_detail')

    @getimage
    def test_001(self):
        log.info(self.test_001.__doc__)
        try:
            login_status = self.is_login()
            if login_status == True:
                self.logout()
            self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/txt_search_copy1").click()
            self.new_find_elements(By.ID, "com.tianyancha.skyeye:id/tv_name")[0].click()

            #     天眼风险调起登录
            self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
            login_new = self.isElementExist(By.XPATH, self.ELEMENT['login_new'])
            self.assertTrue(login_new, '进入天眼风险未调起登录')
            self.driver.keyevent(4)

            # 人员报告拉起登录
            self.new_find_element(By.ID, self.ELEMENT['person_report']).click()
            login_new = self.isElementExist(By.XPATH, self.ELEMENT['login_new'])
            self.assertTrue(login_new, '进入报告页未调起登录')
            self.driver.keyevent(4)

            #       监控拉起登录
            self.new_find_element(By.ID, self.ELEMENT['monitoring']).click()
            login_new = self.isElementExist(By.XPATH, self.ELEMENT['login_new'])
            self.assertTrue(login_new, '点击监控未调起登录')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_002(self):
        log.info(self.test_002.__doc__)
        try:
            # 未登录进入热搜人员无VIP限制
            self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/txt_search_copy1").click()
            self.new_find_elements(By.ID, "com.tianyancha.skyeye:id/tv_name")[0].click()
            self.assertFalse(self.isElementExist(By.XPATH, self.ELEMENT['vip_text']), '未登录进入热搜人员详情有VIP限制')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e

    @getimage
    def test_003(self):
        log.info(self.test_003.__doc__)
        try:
            # 非VIP进入非热搜人员
            self.search_boss('马云')
            self.new_find_elements(By.ID, "com.tianyancha.skyeye:id/root_view", outtime=10)[0].click()
            self.login(self.user, self.account.get_pwd())

            # 人员页分享存长图无按钮
            save_pic = self.isElementExist(By.ID, self.ELEMENT['save_pic'])
            self.assertFalse(save_pic)
            share = self.isElementExist(By.ID, self.ELEMENT['share'])
            self.assertFalse(share)

            # 老板详情VIP限制
            self.assertTrue(self.isElementExist(By.XPATH, self.ELEMENT['vip_text']), '非VIP进入热搜人员详情无VIP限制')

            # 信用报告VIP限制
            self.new_find_element(By.ID, self.ELEMENT['person_report']).click()
            self.new_find_element(By.ID, self.ELEMENT['person_report_vip_download']).click()
            self.assertTrue(self.isElementExist(By.XPATH, self.ELEMENT['vip_boss_report']), '非VIP人员报告无VIP弹窗')
            # 回到人员从详情页方法
            while True:
                try:
                    self.driver.find_element_by_xpath(self.ELEMENT['vip_text'])
                    break
                except:
                    self.driver.keyevent(4)

            # 天眼风险VIP限制
            self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
            vip_warning = self.isElementExist(By.XPATH, self.ELEMENT['vip_warning'], outtime=10)
            self.assertTrue(vip_warning, '非VIP天眼风险无VIP限制')
            self.driver.keyevent(4)

            # 股权穿透VIP限制
            self.new_find_element(By.ID, self.ELEMENT['map_stock']).click()
            vip_stock = self.isElementExist(By.XPATH, self.ELEMENT['vip_stock'], outtime=10)
            self.assertTrue(vip_stock, '非VIP股权穿透图无VIP限制')
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
