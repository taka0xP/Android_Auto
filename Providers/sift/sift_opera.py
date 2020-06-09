# -*- coding: utf-8 -*-
# @Time    : 2020-02-20 09:13
# @Author  : XU
# @File    : sift_opera.py
# @Software: PyCharm

from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from Providers.logger import Logger
import random
from selenium.webdriver.support.wait import WebDriverWait


class SiftOperation:
    def __init__(self, driver, element):
        self.driver = driver
        self.operation = Operation(driver)
        self.element = element
        self.log = Logger("sift_tools").getlog()

    @getimage
    def get_key(self, key_, value, index):
        """
        获取高级筛选，选中项
        :param key_: 高级筛选项，键集合
        :param value: 高级筛选项，值集合
        :param index: 选择项索引
        :return:返回被选中项key
        """
        len_ = self.driver.get_window_size()
        x = len_["width"] * 0.5
        y1 = len_["height"] * 0.5
        y2 = len_["height"] * 0.15
        listKey = self.element[key_].split("###")
        listValue = self.element[value].split("###")
        origin = self.element[listKey[index - 1]]
        target = listValue[index - 1]
        if not self.operation.isElementExist(By.ID, self.element["bt_reset"]):
            self.operation.new_find_element(By.ID, self.element["select_more"]).click()
        all_icon = origin.split("..")[0] + "following-sibling::android.widget.ImageView"
        for i in range(20):
            icon_tag = self.operation.isElementExist(By.XPATH, all_icon)
            origin_tag = self.operation.isElementExist(By.XPATH, origin)
            if len(listKey) > 2 and icon_tag:
                self.operation.new_find_element(By.XPATH, all_icon).click()
                break
            elif origin_tag:
                break
            else:
                self.driver.swipe(x, y1, x, y2, 2000)
                if i == 19:
                    self.log.info("获取「{}」失败".format(target))

        origin_text = self.operation.new_find_element(By.XPATH, origin).text
        self.operation.new_find_element(By.XPATH, origin).click()
        if self.operation.isElementExist(By.ID, self.element["more_commit"]):
            self.operation.new_find_element(By.ID, self.element["more_commit"]).click()

        return listKey[index - 1], origin_text

    @getimage
    def back2relation_search(self, inputTarget):
        """
        从公司详情页检验完成后，回到查关系
        :param inputTarget: 搜索关键词
        """
        for i in range(20):
            if self.operation.isElementExist(By.ID, self.element["clear_all"]):
                self.operation.new_find_element(By.ID, self.element["clear_all"]).click()
                self.operation.new_find_element(By.ID, self.element["delete_confirm"]).click()
                self.operation.new_find_element(By.ID, self.element["from_input_textview"]).click()
                self.operation.new_find_element(By.ID, self.element["search_input_edit"]).send_keys(inputTarget)
                break
            else:
                self.driver.keyevent(4)

    @getimage
    def back2company_search(self):
        """
        从公司详情页检验完成后，回到查公司
        """
        for i in range(20):
            if self.operation.isElementExist(By.ID, self.element["search_sort_or_cancel"]):
                break
            else:
                self.driver.keyevent(4)

    @getimage
    def reset(self, targetSelect):
        """
        重置高级筛选项
        :param targetSelect: 被选中筛选项
        """

        if self.operation.isElementExist(By.ID, self.element["bt_reset"]):
            if targetSelect is None:
                self.operation.new_find_element(By.ID, self.element["bt_reset"]).click()
            else:
                self.operation.new_find_element(By.XPATH, self.element[targetSelect]).click()
        else:
            if not self.operation.isElementExist(By.ID, self.element["select_more"]):
                self.operation.swipeDown()
            self.operation.new_find_element(By.ID, self.element["select_more"]).click()
            if targetSelect is None:
                self.operation.new_find_element(By.ID, self.element["bt_reset"]).click()
            else:
                self.operation.new_find_element(By.XPATH, self.element[targetSelect]).click()

    @getimage
    def login_vip(self, phone_num_vip, phone_passwd):
        """
        登陆vip账号
        """
        if self.operation.is_login():
            self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
            login_text = self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_user_type").text
            if "到期时间" in login_text:
                self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_1").click()
            else:
                self.operation.logout()
                self.operation.login(phone_num_vip, phone_passwd)
        else:
            self.operation.login(phone_num_vip, phone_passwd)

    @getimage
    def login_normal(self, phone_num_normal, phone_passwd):
        """
        登陆普通账号
        """
        if self.operation.is_login():
            self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
            login_text = self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_user_type").text
            if "到期时间" in login_text:
                self.operation.logout()
                self.operation.login(phone_num_normal, phone_passwd)
            else:
                self.operation.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_1").click()
        else:
            self.operation.login(phone_num_normal, phone_passwd)

    @getimage
    def search_key(self, tag):
        """
        输入搜索关键词
        :param tag: 1:查公司；2：查关系
        :return: 返回输入的关键词
        """
        if tag == 1:
            self.operation.new_find_element(By.ID, self.element["search_company"]).click()
        else:
            self.operation.new_find_element(By.ID, self.element["search_relation"]).click()
        self.operation.new_find_element(By.ID, self.element["search_box"]).click()
        tarList = self.element["from_input_target"].split("###")
        inputTarget = tarList[random.randint(0, len(tarList) - 1)]
        if tag == 2:
            self.operation.new_find_element(By.ID, self.element["from_input_textview"]).click()
        self.operation.new_find_element(By.ID, self.element["search_input_edit"]).send_keys(inputTarget)
        self.log.info("搜索词：{}".format(inputTarget))
        return inputTarget

    @getimage
    def point2company(self, selectTarget):
        """
        从关系节点介入公司详情页
        :param selectTarget: 选中条件
        :return: 输入内容
        """
        selectText = self.operation.new_find_element(By.ID, self.element["tv_title"]).text
        if self.operation.isElementExist(By.ID, self.element["more_empty_view"]):
            self.log.info(selectText)
            self.reset(selectTarget)
        else:
            self.operation.new_find_element(By.XPATH, self.element["from_target_item_1"]).click()
            self.operation.new_find_element(By.XPATH, self.element["sky_canvas"]).click()
        return selectText

    @getimage
    def click2company(self, selectText, selectTarget):
        """
        用于查公司-更多筛选，点击搜索列表页中item
        :param selectText: 更多筛选-筛选项
        :param selectTarget: 搜索关键词
        :return: 返回被校验公司名
        """
        company_name = ''
        if self.operation.isElementExist(By.ID, self.element["more_empty_view"]):
            self.log.info("「{}」筛选无结果".format(selectText))
            self.reset(selectTarget)
        else:  # 查公司-「机构类型」筛选
            items = self.random_list()
            self.log.info("「{}」，搜索结果页-公司列表长度：{}".format(selectText, str(items)))
            # 防止item超出页面，无法获取元素
            if items > 2:
                items = items - 2
            t_item = "{}[{}]{}".format(self.element["company_list"], str(items), self.element["company_name_path"])
            company_name_ele = self.operation.new_find_element(By.XPATH, t_item)
            company_name = company_name_ele.text
            self.log.info("断言公司名称：{}".format(company_name))
            company_name_ele.click()
        return company_name

    @getimage
    def random_list(self):
        """
        搜索列表页，随机上滑
        :return: 返回搜索列表页，list长度
        """
        len_ = self.driver.get_window_size()
        x = len_["width"] * 0.5
        y1 = len_["height"] * 0.8
        y2 = len_["height"] * 0.3
        for i in range(random.randint(2, 6)):
            self.driver.swipe(x, y1, x, y2, 1000)
        return len(self.operation.new_find_elements(By.XPATH, self.element["company_list"]))

    @getimage
    def detail4relation(self, detailText, selectTarget, inputTarget, index=None):
        """
        获取公司：详情页维度
        :param detailText: 详情页维度名称
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        :param index: 选中项索引
        """
        selectText = self.point2company(selectTarget)
        firm_name = self.operation.new_find_element(By.ID, self.element["firm_detail_name_tv"]).text
        self.log.info("高级筛选:{}，断言公司名称：{}".format(selectText, firm_name))
        result = self.find_dim(detailText, selectText, index)
        self.back2relation_search(inputTarget)
        return result

    @getimage
    def detail4company(self, selectText, detailText, selectTarget, index=None):
        """
        获取公司：详情页维度
        :param selectText: 选中的筛选条件
        :param detailText: 详情页维度名称
        :param selectTarget: 选中条件
        :param index: 选中项索引
        """
        self.click2company(selectText, selectTarget)
        result = self.find_dim(detailText, selectText, index)
        self.back2company_search()
        self.reset(selectTarget)
        return result

    @getimage
    def erg_ew(self, selectText):
        """
        选中网址/邮箱
        :param selectText: 被选中项
        """
        _map = [
            {"tag": "邮箱", "ele": "tv_base_info_email"},
            {"tag": "网址", "ele": "tv_base_info_web"},
        ]
        result = "false"
        for i in _map:
            if i["tag"] in selectText:
                if self.operation.isElementExist(By.ID, self.element[i["ele"]]):
                    result = self.driver.find_element_by_id(self.element[i["ele"]]).get_attribute("enabled")
                if not self.operation.isElementExist(By.ID, "com.tianyancha.skyeye:id/iv_claim_label"):
                    if result == "true":
                        self.log.info("===公司被认证，企业主上传了「{}信息」===".format(i["tag"]))
                        result = "false"
        return result

    @getimage
    def basic4relation(self, selectTarget, inputTarget):
        """
        获取公司：基本信息(网址、邮箱)并断言
        :param selectTarget: 选中条件
        :param inputTarget: 输入内容
        """
        selectText = self.point2company(selectTarget)
        company_name = self.operation.new_find_element(By.ID, self.element["firm_detail_name_tv"]).text
        self.log.info("高级筛选：{}，断言公司名称：{}".format(selectText, company_name))
        result = self.erg_ew(selectText)
        self.back2relation_search(inputTarget)
        return result, company_name

    @getimage
    def basic4company(self, selectText, selectTarget):
        """
        获取公司：基本信息(网址、邮箱)并断言
        :param selectText: 被选中的筛选项
        :param selectTarget: 选中条件
        """
        self.click2company(selectText, selectTarget)
        WebDriverWait(self.driver, 5).until(
            lambda driver: driver.find_element_by_id(self.element["tv_base_info_email"])
        )
        result = self.erg_ew(selectText)
        self.back2company_search()
        self.reset(selectTarget)
        return result

    @getimage
    def into_company(self, company=None):
        """搜公司，并进入公司详情页"""
        if company is not None:
            self.operation.new_find_element(By.ID, self.element["search_company"]).click()
            self.operation.new_find_element(By.ID, self.element["search_box"]).click()
            self.operation.new_find_element(By.ID, self.element["search_input_edit"]).send_keys(company)
            company_ele = '//*[@class="android.widget.TextView" and @text="{}"]'.format(company)
            self.operation.new_find_element(By.XPATH, company_ele).click()
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element_by_id(self.element["tag_firm"])
            )
        else:
            self.search_key(1)
            WebDriverWait(self.driver, 5).until(
                lambda driver: driver.find_element_by_id(self.element["btn_export_data"])
            )
            items = self.random_list()
            # 防止item超出页面，无法获取元素
            if items > 2:
                items = items - 2
            item_tag = "{}[{}]{}".format(self.element["company_list"], str(items), self.element["company_name_path"])
            company_item = self.operation.new_find_element(By.XPATH, item_tag)
            company_name = company_item.text
            self.log.info("断言公司名称：{}".format(company_name))
            company_item.click()
            return company_name

    @getimage
    def find_dim(self, detailText, selectText, index):
        """查找维度"""
        result = ''
        d_wd = '//*[@class="android.widget.TextView" and @text="{}"]'.format(detailText)
        d_count = '//*[@class="android.widget.TextView" and @text="{}"]/preceding-sibling::android.widget.TextView'.format(
            detailText)
        for i in range(20):
            if self.operation.isElementExist(By.XPATH, d_wd):
                detailCount = self.operation.isElementExist(By.XPATH, d_count)
                if detailText == "著作权":
                    if index == 2 and not detailCount:
                        # 断言-详情页「著作权」维度无数据时
                        result = detailCount
                    else:
                        self.operation.new_find_element(By.XPATH, d_wd).click()
                        targ = selectText[1:]  # 截取著作权类别
                        if targ == "软件著作权":
                            result = self.operation.count_num(By.XPATH, self.element["rjzzq_detail_tab_layout"])
                        elif targ == "作品著作权":
                            result = self.operation.count_num(By.XPATH, self.element["rjzzq_detail_tab_layout"])
                    break
                else:
                    result = detailCount
            else:
                self.operation.swipeUp(0.5, 0.7, 0.3, 2000)
                if i == 19:
                    self.log.info("断言失败-公司详情页未找到「{}」".format(detailText))
        return result

    @getimage
    def company_type(self, selectText, index, result=None):
        """进入工商信息，验证企业类型，相关操作"""
        _type_dict = {4: ["国有"], 6: ["个体"], 9: ["外"], 10: ["港", "澳", "台"], 11: ["联营"], 12: ["一人有限责任公司"]}
        for i in range(20):
            if self.operation.isElementExist(By.XPATH, self.element["more_gsxx_dimension"]):
                self.operation.new_find_element(By.XPATH, self.element["more_gsxx_dimension"]).click()
                # 工商信息维度，查找企业类型字段
                for j in range(20):
                    if self.operation.isElementExist(By.ID, self.element["companyinfo_company_org_type_tv"]):
                        result_text = self.operation.new_find_element(By.ID, self.element["companyinfo_company_org_type_tv"]).text
                        self.log.info("企业类型筛选:{}".format(selectText))
                        result = None
                        for k in _type_dict.keys():
                            if index == k:
                                result = False
                                for l in _type_dict[k]:
                                    if l in result_text:
                                        result = True
                                        break
                                break
                            else:
                                result = selectText in result_text
                        break
                    else:
                        self.operation.swipeUp(0.5, 0.7, 0.3, 2000)
                        if j == 19:
                            result = "企业类型断言失败-工商信息详情页，企业类型未找到"
                break
            else:
                self.operation.swipeUp(0.5, 0.7, 0.3, 2000)
                if i == 19:
                    result = "企业类型断言失败-公司详情页未找到「工商信息」"
        return result
