# -*- coding: utf-8 -*-
# @Time    : 2020-04-07 15:10
# @Author  : wlx
# @File    : company_detail_history_info.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep, time
from Providers.logger import Logger, error_format
from common.check_rules import *

log = Logger("历史信息_11").getlog()


class Company_detail_Test_wlx_12(MyTest, Operation):
    """热门商标"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 获取excel
        cls.ELEMENT = Read_Ex().read_excel("company_detail_wlx")
        cls.vip_user = cls.account.get_account("vip", "0")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.account.release_account(account=cls.vip_user, account_type="vip", account_special="0")

    def go_company_detail(self, company_name, index=0):
        self.search_company(company_name)
        self.new_find_elements(
            By.XPATH, self.ELEMENT["company_name_search_result_list"]
        )[index].click()

    def test_001(self):
        """热门商标"""
        log.info(self.test_001.__doc__)
        try:
            self.login(self.vip_user, self.account.get_pwd())
            self.go_company_detail("百度")
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT['hot_trademark'])
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT['change_btn'], check_cover=True)
            # 获取推荐的商标
            trademark = self.new_find_elements(By.XPATH, self.ELEMENT['trademark_for_you'])
            trademark_be = []
            for i in range(len(trademark)):
                b = trademark[i].text
                trademark_be.append(b)
            self.new_find_element(By.XPATH, self.ELEMENT['change_btn']).click()
            # 获取点击'换一批'按钮后得到的商标推荐
            trademark = self.new_find_elements(By.XPATH, self.ELEMENT['trademark_for_you'])
            trademark_af = []
            for i in range(len(trademark)):
                b = trademark[i].text
                trademark_af.append(b)
            # 两次给出的推荐商标应不相等
            self.assertNotEqual(trademark_af, trademark_be, '热门商标推荐点击换一批前后数据一样')

            # 外部推荐count数
            hot_trademark = self.new_find_element(By.XPATH, self.ELEMENT['hot_trademark'])
            for_u_count = self.count(hot_trademark)
            self.swipe_up_while_ele_located(By.ID, self.ELEMENT['trademark_all_btn'], click=True)
            self.new_find_element(By.ID, self.ELEMENT['more_service']).click()
            self.assertTrue(self.new_find_element(By.XPATH, self.ELEMENT['allserviceh5_trademark']).is_selected(),
                            '推荐商标列表页进入天眼服务全部服务页面未默认选中商标服务tab')
            self.driver.keyevent(4)
            service_1 = self.new_find_element(By.ID, self.ELEMENT['for_u_service_1'])
            service_1_name = service_1.text
            service_1.click()
            sleep(1)
            service_1_detail_title = self.new_find_element(By.ID, self.ELEMENT['app_page_title'], outtime=15)

            self.assertEqual(service_1_name, service_1_detail_title.text,
                             '推荐商标页服务入口{}进入到了天眼服务的{}页面'.format(service_1_name, service_1_detail_title.text))
            self.driver.keyevent(4)

            service_2 = self.new_find_element(By.ID, self.ELEMENT['for_u_service_2'])
            service_2_name = service_2.text
            service_2.click()
            sleep(1)
            service_2_detail_title = self.new_find_element(By.ID, self.ELEMENT['app_page_title'], outtime=15)
            self.assertEqual(service_2_name, service_2_detail_title.text,
                             '推荐商标页服务入口{}进入到了天眼服务的{}页面'.format(service_2_name, service_2_detail_title.text))
            self.driver.keyevent(4)

            service_3 = self.new_find_element(By.ID, self.ELEMENT['for_u_service_3'])
            service_3_name = service_3.text
            service_3.click()
            sleep(1)
            service_3_detail_title = self.new_find_element(By.ID, self.ELEMENT['app_page_title'], outtime=15)
            self.assertEqual(service_3_name, service_3_detail_title.text,
                             '推荐商标页服务入口{}进入到了天眼服务的{}页面'.format(service_3_name, service_3_detail_title.text))
            self.driver.keyevent(4)

            list_name = self.new_find_elements(By.ID, self.ELEMENT['safe_item_name'])[0].text
            self.new_find_elements(By.XPATH, self.ELEMENT['trademark_safe_list'])[0].click()
            sleep(1)
            detail_title = self.new_find_element(By.ID, self.ELEMENT['app_page_title'], outtime=10).text
            self.swipe_up_while_ele_located(By.XPATH, self.ELEMENT['service_name'].format(list_name))
            detail = self.new_find_element(By.XPATH, self.ELEMENT['service_name'].format(list_name)).text
            service_trademark_name = detail.split('：')[1]
            self.assertEqual(list_name, service_trademark_name,
                             '推荐商标item的商标名称{}与注册页商标名称{}不一致'.format(list_name, service_trademark_name))
            self.assertEqual(detail_title, '顾问商标注册', '推荐商标页点击list立即注册进入到了天眼服务的{}页面'.format(detail_title))
            self.driver.keyevent(4)

            real_count = self.all_count_compute_v1(By.XPATH, self.ELEMENT['trademark_safe_list'])
            self.assertEqual(real_count, for_u_count,
                             '公司详情页推荐商标count数{}与实际推荐商标item数{}不相等'.format(for_u_count, real_count))

            self.new_find_element(By.XPATH, self.ELEMENT['below_service_btn']).click()
            sleep(1)
            detail_title = self.new_find_element(By.ID, self.ELEMENT['app_page_title'], outtime=15).text
            self.assertEqual(detail_title, '顾问商标注册', '推荐商标页底部立即注册入口进入到了天眼服务的{}页面'.format(detail_title))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(error_format(e))
            raise e
