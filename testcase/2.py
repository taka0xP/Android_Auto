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
        self.search_boss('马云')
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']", outtime=10).click()
        # 登录VIP账户
        self.login(10222222229, 'ls123456')

        # 人员页分享存长图限制
        save_pic = self.isElementExist(By.ID, self.ELEMENT['save_pic'], outtime=10)
        self.assertTrue(save_pic)
        print('有保存按钮')
        share = self.isElementExist(By.ID, self.ELEMENT['share'])
        self.assertTrue(share)
        print('有分享按钮')

        # 曾经任职
        used_to_work = self.new_find_element(By.XPATH, self.ELEMENT['used_to_work'])
        used_to_work_count = self.count(used_to_work)
        used_to_work.click()
        # 历史法人列表
        his_legal = self.new_find_element(By.ID, self.ELEMENT['his_legal'])
        his_legal1 = self.count(his_legal)
        his_legal_count = self.count(self.new_find_element(By.XPATH, self.ELEMENT['his_legal_count']))
        self.assertEqual(his_legal1, his_legal_count, '历史法人count校验错误')
        # 历史股东列表
        his_shareholder = self.new_find_element(By.ID, self.ELEMENT['his_shareholder'])
        his_shareholder1 = self.count(his_shareholder)
        his_shareholder.click()
        his_shareholder_count = self.count(self.new_find_element(By.XPATH, self.ELEMENT['his_shareholder_count']))
        self.assertEqual(his_shareholder1, his_shareholder_count, '历史股东count校验错误')
        # 历史高管列表
        his_executive = self.new_find_element(By.ID, self.ELEMENT['his_executive'])
        his_executive1 = self.count(his_executive)
        his_executive.click()
        his_executive_count = self.count(self.new_find_element(By.XPATH, self.ELEMENT['his_executive_count']))
        self.assertEqual(his_executive1, his_executive_count, '历史高管count校验错误')
        # 校验里外count
        his_count = his_legal_count + his_shareholder_count + his_executive_count
        self.assertEqual(used_to_work_count, his_count, '曾经任职和历史数据count不对')
        self.driver.keyevent(4)

        # 担任法人
        sleep(1)
        fr1 = self.new_find_element(By.ID, self.ELEMENT['act_as_legal_representative'])
        fr1.click()
        sleep(1)
        fr2 = self.new_find_element(By.XPATH, self.ELEMENT['legal_representative_companies'])
        frcount1 = self.count(fr1)
        frcount2 = self.count(fr2)
        self.assertEqual(frcount1, frcount2, '担任法人count数check错误')

        # 担任股东
        gd1 = self.new_find_element(By.ID, self.ELEMENT['act_as_shareholder'])
        gd1.click()
        gd2 = self.new_find_element(By.XPATH, self.ELEMENT['shareholder_companies'])
        # 获取count数
        gdcount1 = self.count(gd1)
        gdcount2 = self.count(gd2)
        self.assertEqual(gdcount1, gdcount2, '担任股东count数check错误')

        # 担任高管
        gg1 = self.new_find_element(By.ID, self.ELEMENT['executive'])
        gg1.click()
        gg2 = self.new_find_element(By.XPATH, self.ELEMENT['executive_companies'])
        ggcount1 = self.count(gg1)
        ggcount2 = self.count(gg2)
        self.assertEqual(ggcount1, ggcount2, '担任高管count数check错误')

        # 实际控制权
        s1 = self.new_find_element(By.ID, self.ELEMENT['actual_control'])
        s1.click()
        s2 = self.new_find_element(By.XPATH, self.ELEMENT['actual_control_count'])
        s1count = self.count(s1)
        s2count = self.count(s2)
        self.assertEqual(s1count, s2count, '实际控制权count数check错误')
        self.new_find_element(By.XPATH, self.ELEMENT['view_investment_chain']).click()
        a = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/app_title_name').text
        self.assertEqual(a, '投资链', '投资链页面title错误')
        self.driver.keyevent(4)

        # 合作伙伴
        h1 = self.new_find_element(By.ID, self.ELEMENT['partners'])
        h1.click()
        h2 = self.new_find_element(By.XPATH, self.ELEMENT['partners_count'])
        h1count = self.count(h1)
        h2count = self.count(h2)
        self.assertEqual(h1count, h2count, '合作伙伴count数check错误')

    @getimage
    def test_002(self):
        # 人员详情页执行监控同步
        self.search_boss('马云')
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']", outtime=10).click()
        # 检测是否监控当前人员，如监控执行取消监控

        if self.new_find_element(By.XPATH, "//android.widget.TextView[@text='监控']", outtime=10):
            print('未监控')
        else:
            self.new_find_element(By.ID, self.ELEMENT['monitoring']).click()
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn_pos').click()
            print('已取消监控')

        # 监控人员
        self.new_find_element(By.ID, self.ELEMENT['monitoring']).click()
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']").click()

        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_text_monitoring', outtime=20)
        monitoring = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_text_monitoring', outtime=20).text
        self.assertEqual(monitoring, '已监控', '监控失败')

        # 天眼风险页面监控态同步
        self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
        monitoring_setail = self.isElementExist(By.ID, 'com.tianyancha.skyeye:id/tv_monitoring', outtime=15)
        self.assertFalse(monitoring_setail, '监控后天眼风险页面监控按钮未同步')

        # 回到搜索结果页
        while True:
            try:
                self.driver.find_element_by_id('com.tianyancha.skyeye:id/et_search_input')
                break
            except:
                self.driver.keyevent(4)

        # 取消监控
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']").click()
        self.new_find_element(By.ID, self.ELEMENT['monitoring'], outtime=10).click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn_pos').click()
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']").click()
        sleep(5)
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_text_monitoring')
        monitor = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_text_monitoring').text
        self.assertEqual(monitor, '监控', '取消监控失败')

        # 取消监控，天眼风险页面同步
        self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()

        monitoring_setail = self.isElementExist(By.ID, 'com.tianyancha.skyeye:id/tv_monitoring', outtime=10)
        self.assertTrue(monitoring_setail, '取消监控后天眼风险页面监控按钮未同步')

    @getimage
    def test_003(self):
        # 天眼风险页执行监控同步
        self.search_boss('马云')
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']").click()
        # 检测是否监控当前人员，如监控执行取消监控
        if self.new_find_element(By.XPATH, "//android.widget.TextView[@text='监控']", outtime=10):
            print('未监控')
        else:
            self.new_find_element(By.ID, self.ELEMENT['monitoring']).click()
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/btn_pos').click()
            print('已取消监控')

        # 进入天眼风险页进行监控
        self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
        # 判断页面是否有监控按钮
        if self.isElementExist(By.ID, 'com.tianyancha.skyeye:id/tv_monitoring', outtime=20):
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_monitoring').click()
            sleep(5)
            monitoring_setail = self.isElementExist(By.ID, 'com.tianyancha.skyeye:id/tv_monitoring')
            self.assertFalse(monitoring_setail, '天眼风险页面监控失败')
            self.driver.keyevent(4)

            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_text_monitoring', outtime=20)
            monitoring = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_text_monitoring', outtime=20).text
            self.assertEqual(monitoring, '已监控', '天眼风险监控后按钮同步失败')
        else:
            self.assertTrue(self.isElementExist(By.ID, 'com.tianyancha.skyeye:id/tv_monitoring', outtime=20),
                            '天眼风险页无监控按钮')

    @getimage
    def test_004(self):
        self.search_boss('马云')
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']").click()
        name = self.new_find_element(By.ID, self.ELEMENT['human_detail_name']).text
        self.new_find_element(By.ID, self.ELEMENT['person_report'], outtime=10).click()

        # 人员报告权益
        a = self.isElementExist(By.XPATH, self.ELEMENT['report_content_1'])
        self.assertTrue(a, '人员报告权益第1条错误')
        a = self.isElementExist(By.XPATH, self.ELEMENT['report_content_2'])
        self.assertTrue(a, '人员报告权益第2条错误')
        a = self.isElementExist(By.XPATH, self.ELEMENT['report_content_3'])
        self.assertTrue(a, '人员报告权益第3条错误')
        a = self.isElementExist(By.XPATH, self.ELEMENT['report_content_4'])
        self.assertTrue(a, '人员报告权益第4条错误')
        a = self.isElementExist(By.XPATH, self.ELEMENT['report_content_5'])
        self.assertTrue(a, '人员报告权益第5条错误')
        a = self.isElementExist(By.XPATH, self.ELEMENT['report_content_6'])
        self.assertTrue(a, '人员报告权益第6条错误')
        a = self.isElementExist(By.XPATH, self.ELEMENT['report_content_7'])
        self.assertTrue(a, '人员报告权益第7条错误')
        sleep(2)

        # 人员报告样本预览
        self.new_find_element(By.ID, self.ELEMENT['sample_preview']).click()
        a = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/pdf_web_title_name', outtime=10).text
        self.assertEqual(a, '样本预览', '样本预览页错误')
        self.driver.keyevent(4)
        self.new_find_element(By.XPATH, self.ELEMENT['report_download']).click()
        # 报告下载默认选择PDF格式校验
        pdf = self.new_find_element(By.XPATH,
                                    "//*[@resource-id='com.tianyancha.skyeye:id/order_report_pdf_iv']").is_selected()
        self.assertTrue(pdf, '人员报告页未默认选中PDF格式')

        # 人员报告下载页名字校验
        name1 = self.new_find_element(By.ID, self.ELEMENT['name_report']).text
        self.assertEqual(name, name1, '报告下载页名字和详情页名字不一致')

        # 人员报告pdf下载，邮箱修改,结果校验
        a = self.isElementExist(By.ID, self.ELEMENT['email_del'])
        if a == True:
            # 判断是否有默认邮箱
            self.new_find_element(By.ID, self.ELEMENT['email_del']).click()
        # self.new_find_element(By.ID, self.ELEMENT['email']).click()
        self.new_find_element(By.ID, self.ELEMENT['email']).send_keys('18732096902@163.com')
        self.new_find_element(By.ID, self.ELEMENT['send_report']).click()

        # 人员名称校验
        name2 = self.new_find_elements(By.XPATH, self.ELEMENT['report_name'])[0].text
        self.assertEqual(name2, name, '订单页名字与详情页人员名字不符')
        # 订单页校验报告类型
        dow_type = self.new_find_elements(By.XPATH, self.ELEMENT['report_download_type'])[0].text
        self.assertEqual(dow_type, 'PDF', '订单页人员报告下载类型与选择的不符')

        # 校验接收邮箱
        rev_email = self.new_find_elements(By.XPATH, self.ELEMENT['rec_email'])[0].text
        self.assertEqual(rev_email, '18732096902@163.com', '订单页接收邮箱错误')
        self.driver.keyevent(4)

        self.new_find_element(By.XPATH, self.ELEMENT['report_download'], outtime=15).click()

        # 下载PDF+Word报告
        self.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/order_report_pdf_word_iv']").click()
        self.new_find_element(By.ID, self.ELEMENT['send_report'], outtime=10).click()
        dow_type = self.new_find_elements(By.XPATH, self.ELEMENT['report_download_type'])[0].text
        self.assertEqual(dow_type, 'PDF+Word', '订单页人员报告下载类型与选择的不符_PDF+WORD')

        # 校验下载类型
        rev_email = self.new_find_elements(By.XPATH, self.ELEMENT['rec_email'])[0].text
        self.assertEqual(rev_email, '18732096902@163.com', '订单页接收邮箱错误_PDF+WORD')
        # 校验人名
        name3 = self.new_find_elements(By.XPATH, self.ELEMENT['report_name'])[0].text
        self.assertEqual(name3, name, '订单页名字与详情页人员名字不符_PDF+WORD')

    @getimage
    def test_005(self):
        self.search_boss('马云')
        self.new_find_element(By.XPATH, "//android.widget.TextView[@text='陆兆禧']").click()

        # 获取人员详情页自身风险count
        riskself = self.new_find_element(By.XPATH, self.ELEMENT['risk_self_count'])
        riskself_count = self.count(riskself, 0)
        # 获取人员详情页周边风险count
        around = self.new_find_element(By.XPATH, self.ELEMENT['risk_around_count'])
        around_count = self.count(around, 0)
        # 滑动banner切换到预警提醒
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        self.driver.swipe(0.5 * x, 0.4 * y, 0.25 * x, 0.4 * y, 300)
        # 获取人员详情页预警提醒count
        warning = self.new_find_element(By.XPATH, self.ELEMENT['risk_warning_count'])
        warning_count = self.count(warning, 0)
        # 进入天眼风险详情页
        self.new_find_element(By.ID, self.ELEMENT['riskinfo']).click()
        a = self.new_find_element(By.ID, self.ELEMENT['riskinfo_self'])
        b = self.count(a)
        self.assertEqual(riskself_count, b, '自身风险count人员详情和风险详情不一样')
        c = self.new_find_element(By.XPATH, self.ELEMENT['riskinfo_self_count'])
        d = self.count(c)
        self.assertEqual(b, d, '天眼风险详情页自身风险count数校验错误')
        # 周边风险count校验
        c = self.new_find_element(By.ID, self.ELEMENT['riskinfo_around'])
        d = self.count(c)
        c.click()
        self.assertEqual(around_count, d, '周边风险count人详情和天眼风险详情里外不一样')
        e = self.new_find_element(By.XPATH, self.ELEMENT['riskinfo_around_count'])
        f = self.count(e)
        self.assertEqual(around_count, f, '天眼风险详情页周边风险count数校验错误')
        # 预警提醒count校验
        a = self.new_find_element(By.ID, self.ELEMENT['riskinfo_warning'])
        b = self.count(a)
        a.click()
        self.assertEqual(warning_count, b, '预警提醒count人详情和天眼风险详情里外不一样')
        sleep(1)
        c = self.new_find_element(By.XPATH, self.ELEMENT['riskinfo_warning_count'])
        d = self.count(c)
        self.assertEqual(warning_count, d, '天眼风险详情页预警提醒count数校验错误')
        self.driver.keyevent(4)