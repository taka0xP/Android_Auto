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



class Human_detailTest(MyTest, Operation):
    a = Read_Ex()
    ELEMENT = a.read_excel('Human_detail')

    @getimage
    def test_001(self):
        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login(10222222229,'ls123456')
        # 预警提醒count数校验
        self.new_find_element(By.ID, self.ELEMENT['search_company']).click()
        self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
        self.new_find_element(By.ID, self.ELEMENT['middle_search_box']).send_keys('大连易航科技有限公司')
        self.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/search_legal_man_tv' and @text='孙凯']").click()
        self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
        c = self.new_find_element(By.ID, self.ELEMENT['riskinfo_warning'])
        d = self.count(c)
        c.click()
        self.swipeUp()
        e = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_risk_count']")
        l =[]
        # 获取每个item的count，放进l
        for i in e:
            b = self.count(i)
            l.append(b)
        count = sum(l)
        self.assertEqual(d,count,'预警提醒count数量与列表不符')

    @getimage
    def test_002(self):

        # 周边风险count数校验
        self.new_find_element(By.ID, self.ELEMENT['search_box']).click()
        self.new_find_element(By.ID, self.ELEMENT['middle_search_box']).send_keys('阳江市海陵镇龙轩旅游用品店')
        self.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/search_legal_man_tv' and @text='陈文勇']").click()
        self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
        c = self.new_find_element(By.ID, self.ELEMENT['riskinfo_around'])
        d = self.count(c)
        e = self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_risk_count']")
        l =[]
        # 获取每个item的count，放进l
        for i in e:
            b = self.count(i)
            l.append(b)
        count = sum(l)
        self.assertEqual(d,count,'周边风险count数量与列表不符')

    @getimage
    def test_003(self):
        self.new_find_element(By.ID, self.ELEMENT['search_boss']).click()
        self.new_find_element(By.XPATH, self.ELEMENT['top_search']).click()
        sleep(3)
        name = self.new_find_element(By.ID, self.ELEMENT['human_detail_name']).text
        # 进入纠错页面
        self.new_find_element(By.ID, self.ELEMENT['error']).click()
        self.new_find_element(By.ID, self.ELEMENT['feedback_content']).clear()

        # 校验未填写问题描述时toast
        self.new_find_element(By.ID,self.ELEMENT['error_commit_btn']).click()
        result = self.new_find_element(By.XPATH,self.ELEMENT['error_toast']).text
        self.assertEqual(result,'请填写问题描述','纠错页面未填写问题描述时toast提示错误')

        # 纠错页人员名称校验
        error_name = self.new_find_element(By.ID, self.ELEMENT['error_name']).text
        self.assertEqual(name,error_name,'纠错页面人员名称与人员详情页不一致')

        # 信息有误维度选项校验
        e = self.new_find_elements(By.XPATH, self.ELEMENT['dimension_content'])
        dimension_content = ['老板头像', '简介', '关联公司', '关联风险', '其他']
        for i in range(len(e)):
            b = e[i].text
            self.assertIn(b,dimension_content,'人员纠错页面维度选项<'+b+'>选项没有')

        # 问题描述
        a = self.new_find_element(By.ID, self.ELEMENT['feedback_content'])
        b = self.new_find_element(By.ID, self.ELEMENT['feedback_content_len'])
        default = a.text
        l = b.text
        self.assertEqual(l,'0/300','纠错页面默认文案长度错误')
        self.assertEqual(default,'请详细描述您发现的问题，可获得更快的处理','纠错反馈页面问题描述默认文案错误')
        a.send_keys('测试数据，请忽略')
        content = a.text
        self.assertEqual(content,'测试数据，请忽略','纠错反馈页面问题描述输入内容校验错误')
        l = b.text
        self.assertEqual(l,'8/300','纠错页面默认文案长度错误')
        self.driver.keyevent(4)
        self.new_find_element(By.ID, self.ELEMENT['error']).click()
        a = self.new_find_element(By.ID, self.ELEMENT['feedback_content'])
        content1 = a.text
        self.assertEqual(content,content1,'纠错页面草稿保存错误')
        sleep(3)
        a.clear()

        # 从相册添加图片
        self.new_find_element(By.ID, self.ELEMENT['add_pic']).click()
        self.new_find_element(By.XPATH, self.ELEMENT['add_pic_album']).click()

        # 添加图片超过3张toast
        a = self.new_find_elements(By.XPATH, self.ELEMENT['select_pic'])
        for i in range(4):
            a[i].click()
        b = self.new_find_element(By.XPATH, self.ELEMENT['select_pic_toast']).text
        self.assertEqual(b, '最多选择3张图片', '从相册添加图片超出提示错误')

        # 上传图片校验
        self.new_find_element(By.ID, self.ELEMENT['ok_btn']).click()
        delete_btn = self.new_find_elements(By.XPATH, self.ELEMENT['delete_pic'])
        self.assertEqual(len(delete_btn), 3, '上传图片数量错误')

        # 删除图片
        for i in range(3):
            self.new_find_elements(By.XPATH, self.ELEMENT['delete_pic'])[0].click()
        self.assertFalse(self.isElementExist(By.XPATH, self.ELEMENT['delete_pic']), '删除图片功能错误')
        self.swipeUp()
        # 联系电话
        self.assertEqual(self.new_find_element(By.ID, self.ELEMENT['phone_num'],outtime=10).text, '10222222229','人员纠错页登录用户默认电话号码错误')
        self.new_find_element(By.ID, self.ELEMENT['phone_num']).clear()
        self.assertEqual(self.new_find_element(By.ID, self.ELEMENT['phone_num'],outtime=10).text, '输入手机号，便于您获得处理反馈','人员纠错页登录用户默认电话号码错误')