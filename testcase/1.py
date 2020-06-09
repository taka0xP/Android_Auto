# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 18:44
# @Author  : wlx
# @File    : Human_detailTest.py

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import logging



class Human_Test(MyTest, Operation):
    a = Read_Ex()
    ELEMENT = a.read_excel('Human_detail')

    @getimage
    def test_001(self):
        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
        self.new_find_element(By.XPATH, self.ELEMENT['top_search']).click()
        # 首次进入人员详情页点击'我知道了按钮'
        if self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn',outtime=10):
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn').click()
        # 获取头像旁的名字
        name=self.new_find_element(By.ID, self.ELEMENT['human_detail_name']).text
        self.new_find_element(By.XPATH, self.ELEMENT['head_image']).click()

        # 获取蒙层的名字
        name1 = self.new_find_element(By.ID, self.ELEMENT['human_detail_name_1']).text
        self.assertEqual(name,name1,'蒙层前后名字不一致')
        self.driver.keyevent(4)

    #     天眼风险调起登录
        self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
        login_use_pwd = self.isElementExist(By.XPATH,self.ELEMENT['login_use_pwd'])
        login_new = self.isElementExist(By.XPATH,self.ELEMENT['login_new'])
        if login_use_pwd == True or login_new == True:
            result = True
        else:
            result = False
        self.assertTrue(result,'进入天眼风险未调起登录')
        self.driver.keyevent(4)

        # 人员报告拉起登录
        self.new_find_element(By.ID, self.ELEMENT['person_report']).click()
        login_use_pwd = self.isElementExist(By.XPATH, self.ELEMENT['login_use_pwd'])
        login_new = self.isElementExist(By.XPATH,self.ELEMENT['login_new'])
        if login_use_pwd == True or login_new == True:
            result = True
        else:
            result = False
        self.assertTrue(result,'进入报告页未调起登录')
        self.driver.keyevent(4)

#       监控拉起登录
        self.new_find_element(By.ID, self.ELEMENT['monitoring']).click()
        login_use_pwd = self.isElementExist(By.XPATH, self.ELEMENT['login_use_pwd'])
        login_new = self.isElementExist(By.XPATH,self.ELEMENT['login_new'])
        if login_use_pwd == True or login_new == True:
            result = True
        else:
            result = False
        self.assertTrue(result,'点击监控未调起登录')

    @getimage
    def test_002(self):
        # 未登录进入热搜人员无VIP限制
        self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
        self.new_find_element(By.XPATH, self.ELEMENT['top_search']).click()
        self.assertFalse(self.isElementExist(By.XPATH,self.ELEMENT['vip_text']),'未登录进入热搜人员详情有VIP限制')

    @getimage
    def test_003(self):
        # 非VIP进入非热搜人员
        self.search_boss('马云')
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']",outtime=10).click()
        self.login(10222222225,'ls123456')

        # 人员页分享存长图无按钮
        save_pic = self.isElementExist(By.ID,self.ELEMENT['save_pic'])
        self.assertFalse(save_pic)
        share = self.isElementExist(By.ID, self.ELEMENT['share'])
        self.assertFalse(share)


        # 老板详情VIP限制
        self.assertTrue(self.isElementExist(By.XPATH, self.ELEMENT['vip_text']), '非VIP进入热搜人员详情无VIP限制')

        # 信用报告VIP限制
        self.new_find_element(By.ID, self.ELEMENT['person_report']).click()
        self.new_find_element(By.ID, self.ELEMENT['person_report_vip_download']).click()
        self.assertTrue(self.isElementExist(By.XPATH,self.ELEMENT['vip_boss_report']),'非VIP人员报告无VIP弹窗')
        # 回到人员从详情页方法
        while True:
            try:
                self.driver.find_element_by_xpath(self.ELEMENT['vip_text'])
                break
            except:
                self.driver.keyevent(4)

        # 天眼风险VIP限制
        self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
        vip_warning = self.isElementExist(By.XPATH, self.ELEMENT['vip_warning'],outtime=10)
        self.assertTrue(vip_warning,'非VIP天眼风险无VIP限制')
        self.driver.keyevent(4)

        # 股权穿透VIP限制
        self.new_find_element(By.ID, self.ELEMENT['map_stock']).click()
        vip_stock = self.isElementExist(By.XPATH, self.ELEMENT['vip_stock'],outtime=10)
        self.assertTrue(vip_stock,'非VIP股权穿透图无VIP限制')

