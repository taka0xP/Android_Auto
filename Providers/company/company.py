#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/3
# @Author  : Soner
# @version : 1.0.0

from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from common.operation import Operation
from Providers.logger import Logger
import random

log = Logger("公司相关操作").getlog()


class CompanyFunc:
    def __init__(self, driver, excel):
        self.driver = driver
        self.operation = Operation(driver)
        self.excel = excel

    def search_company(self, company_name, device, company_num=1, max_num=5):
        """
        搜索公司，并进入
        @param company_name:  公司名字
        @param device:  设备名字
        @param company_num: 搜索结果第几个，从1 开始
        @param max_num:
        @return:
        """
        while True:
            if (self.operation.isElementExist(By.ID, self.excel["tab_1"]) or max_num <= 0):
                break
            self.driver.keyevent(4)
            max_num -= 1
        # 点击首页
        self.operation.new_find_element(By.ID, self.excel["tab_1"]).click()
        # 首页进入查公司
        self.operation.new_find_element(By.ID, self.excel["check_company"]).click()
        # 搜索公司名
        self.operation.adb_send_input(By.ID, self.excel["search_company"], company_name, device)
        # 进入公司
        counts = self.operation.new_find_elements(By.XPATH, self.excel['search_num'])
        if len(counts) > 1:
            self.operation.new_find_element(By.XPATH, self.excel["entry_company"].format(company_num)).click()
        else:
            self.operation.new_find_element(By.XPATH, self.excel['entry_one_company']).click()

    def ask_banner(self):
        """
        是否有 问大家 条幅
        @return:
        """
        if self.operation.isElementExist(By.ID, self.excel['ask_banner'], outtime=10):
            self.operation.new_find_element(By.ID, self.excel['ask_banner']).click()

    def is_monitor(self):
        """
        公司是否被监控
        @return: status
        @rtype: bool
        """
        status = None
        monitor = self.operation.new_find_element(By.ID, self.excel["monitor_txt"]).text
        if monitor == "监控":
            status = False
        elif monitor == "已监控":
            status = True
        return status

    def is_group(self, group_name):
        """
        判断分组是否存在
        @param group_name:
        @return:
        """
        status = False
        groups = self.operation.new_find_elements(By.XPATH, self.excel['group_count'])
        for i in range(1, len(groups) + 1):
            name = self.operation.new_find_element(By.XPATH, self.excel['group_name'].format(i)).text
            log.info("当前分组名字：{}， 传入的名字：{}".format(name, group_name))
            if group_name in name:
                status = True
                break
        return status

    def is_collect(self):
        """
        公司是否被收藏
        @return:
        """
        status = None
        collect_text = self.operation.new_find_element(By.ID, self.excel['collect_txt']).text
        if collect_text == "关注":
            status = False
        elif collect_text == "已关注":
            status = True
        return status

    def click_monitor(self, monitor_status=False, click_status=False):
        """
        点击监控
        @return:
        """
        # 点击监控按钮
        self.operation.new_find_element(By.ID, self.excel["click_monitor"]).click()
        if monitor_status:
            self.is_first_monitor()
            if click_status:
                # 点击「我在想想」
                self.operation.new_find_element(By.ID, self.excel["email_neg"]).click()
            else:
                # 点击「确认」
                self.operation.new_find_element(By.ID, self.excel["email_neg_pos"]).click()

    def click_collect(self, collect_status=False, click_status=False):
        """
        点击 关注 按钮
        @return:
        """
        # 点击监控按钮
        self.operation.new_find_element(By.ID, self.excel["click_collect"]).click()
        if collect_status:
            if click_status:
                # 点击「确认」
                self.operation.new_find_element(By.ID, self.excel['email_neg_pos']).click()
                log.info("点击「确定」按钮")
            else:
                # 点击「取消」
                self.operation.new_find_element(By.ID, self.excel['email_neg']).click()
                log.info("点击「取消」按钮")

    def is_first_monitor(self, outtime=1):
        """
        账号是否是第一次监控，是的话需要关闭填写邮箱
        @return:
        """
        status = self.operation.isElementExist(By.ID, self.excel['email_title'], outtime=outtime)
        if status:
            # 第一次监控，点击「取消」
            self.operation.new_find_element(By.ID, self.excel['email_neg'], outtime=0.5).click()

    def entry_monitor(self, back_max=5):
        """
        进入监控列表
        @param back_max:
        @return:
        """
        back_cnt = 0
        while True:
            if self.operation.isElementExist(By.ID, self.excel["tab_1"], outtime=1) or back_cnt > back_max:
                break
            else:
                self.driver.keyevent(4)
                back_cnt += 1
        # 点击「我的」
        self.operation.new_find_element(By.ID, self.excel["tab_5"]).click()
        # 点击「我的监控」
        self.operation.new_find_element(By.ID, self.excel["my_monitor"]).click()
        # 点击「监控列表」
        self.operation.new_find_element(By.XPATH, '//*[@text="监控列表"]').click()

    def entry_collect(self, back_max=5):
        """
        进入 我的-我的关注
        @param back_max:
        @return:
        """
        back_cnt = 0
        while True:
            if self.operation.isElementExist(By.ID, self.excel['tab_1'], outtime=1) or back_cnt > back_max:
                break
            else:
                self.driver.keyevent(4)
                back_cnt += 1
        # 点击「我的」
        self.operation.new_find_element(
            By.ID, self.excel['tab_5']
        ).click()
        # 点击「我的监控」
        self.operation.new_find_element(By.ID, self.excel['my_collect']).click()

    def exists_monitor_list(self, company_name, monitor_count=5):
        """
        判断是否存在该公司
        @param company_name:
        @return:
        """
        # status = False
        # monitor_list = self.operation.new_find_elements(By.XPATH, self.excel['monitor_list'])
        # log.info(len(monitor_list))
        # for i in range(1, len(monitor_list) + 1):
        #     name = self.operation.new_find_element(By.XPATH, self.excel[
        #         'monitor_list'] + '[{}]/android.widget.LinearLayout[1]/android.widget.TextView'.format(i)).text
        #     log.info("获取当前监控列表公司名：{}，待验证公司名：{}".format(name, company_name))
        #     if company_name == name:
        #         status = True
        #         break
        # return status
        # 是否存在列表中
        status = self.operation.isElementExist(By.XPATH, '//*[@text="{}"]'.format(company_name))
        # 当前页没找过，上拉查找
        while not status:
            if monitor_count <= 0:
                log.info('剩余查找次数：{}'.format(monitor_count))
                return False
            else:
                self.operation.swipeUp(y1=0.8, y2=0.5)
                # 是否存在列表中
                status = self.operation.isElementExist(By.XPATH, '//*[@text="{}"]'.format(company_name))
                monitor_count -= 1
        log.info("当前页列表存在公司：{}".format(company_name))
        return status

    def monitor_list_info(self):
        """
        判断监控列表是否有监控信息
        @return:
        """
        monitor_list = self.operation.new_find_elements(By.XPATH, self.excel['monitor_list'])
        if monitor_list is None:
            return False
        return True

    def report_format(self, form):
        if form == 'pdf':
            self.operation.new_find_element(By.ID, self.excel['report_pdf']).click()
        elif form == 'pdf+word':
            self.operation.new_find_element(By.ID, self.excel['report_word']).click()

    def click_tab(self, more_local, x_proportion=108, y_proportion=200):
        """
        根据坐标点击, 默认是点击投诉
        纠错：y_proportion=50
        @return:
        """
        width = more_local['x'] + x_proportion
        height = more_local['y'] - y_proportion

        TouchAction(self.driver).tap(x=width, y=height).release().perform()

    def up_pic(self, num):
        """
        上传图片
        """
        self.operation.new_find_element(By.XPATH, self.excel['select_album']).click()
        pic_num = len(self.operation.new_find_elements(By.XPATH, self.excel['pic_num']))
        # 如果一屏图片多余15个，则只算15个，不然会造成点击不到的情况
        list_count = pic_num
        if list_count > 15:
            list_count = 15
        # 生成相册需要的下标列表，从1开始
        pic_list = [i for i in range(1, list_count + 1)]
        if pic_num > 0:
            if pic_num >= num:
                for i in range(1, num + 1):
                    # 随机一个相册列表下标
                    pop_random = random.randint(0, len(pic_list) - 1)
                    # 获取随机的相册列表对应的xpath下标
                    pop_num = pic_list.pop(pop_random)
                    self.operation.new_find_element(By.XPATH, self.excel['click_pic'].format(pop_num)).click()
                    log.info("第 {} 次随机选择第 {} 个图片".format(i, pop_num))
                self.operation.new_find_element(By.ID, self.excel['pic_btn']).click()
            else:
                raise Exception('相册数量小于要上传的数量')
        else:
            raise Exception('相册数量为0')

    def caption_info(self, check_num, report_list):
        report_count = self.operation.new_find_elements(By.XPATH, self.excel['report_caption'].format(check_num))
        for i in range(0, len(report_count)):
            report_caption = self.operation.new_find_element(By.XPATH,
                                                             self.excel['report_caption_info'].format(check_num,
                                                                                                      i + 1)).text
            log.info("待校验报告说明文案：{}".format(report_caption))
            assert report_list[i] == report_caption, "{}、{}不相等".format(report_list[i], report_caption)

    def check_caption_info(self, check_name, check_num):
        """
        校验 报告说明
        """
        if check_name == "企业信用报告-专业版":
            report_list = ["多维度评估企业信用，包含内容：", "1. 报告包含全部企业基本信息", "2. 股东出资信息、主要人员任职信息",
                           "3. 法定代表人对外投资及任职信息", "4. 股权控制路径"]
            self.caption_info(check_num=check_num, report_list=report_list)

        elif check_name == "企业信用报告-基础版":
            report_list = ["多维度评估企业信用，包含内容：", "1. 工商信息、股东、对外投资、司法风险", "2. 企业发展、知识产权、经营状况、企业年报"]
            self.caption_info(check_num=check_num, report_list=report_list)

        elif check_name == "董监高对外投资及任职报告":
            report_list = ["多维度评估企业信用，包含内容：", "1. 基本信息", "2. 担任法定代表人的企业信息",
                           "3. 对外投资的企业信息（含股比）", "4. 在外任职的企业信息", "5. 拥有疑似实际控制权的企业信息（含投资链）",
                           "6. 曾经任职的企业信息", "7. 人脉圈分析"]
            self.caption_info(check_num=check_num, report_list=report_list)

        elif check_name == "股权结构报告":
            report_list = ["多维度分析企业股权结构，包含内容：", "1. 工商基本信息", "2. 企业类型统计", "3. 各级股东信息", "4. 对外投资信息"]
            self.caption_info(check_num=check_num, report_list=report_list)
