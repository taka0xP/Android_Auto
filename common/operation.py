# -*- coding: utf-8 -*-
# @Time    : 2019-09-19 10:09
# @Author  : ZYF
# @File    : operation.py
import re
import time
import os
from functools import wraps
import tempfile
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from Providers.logger import Logger, error_format
from PIL import Image
import base64
import requests

log = Logger("operation").getlog()

# 失败截图base64
fail_screenshot = dict()


# 用例执行失败自动获取截图装饰器


def getimage(function):
    global fail_screenshot

    @wraps(function)
    def get_error_image(self, *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except:
            time_str = time.strftime("%Y%m%d_%H.%M.%S")
            resultpath = (
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                + "/report/FailureScreenshots/"
            )

            self.driver.get_screenshot_as_file(
                resultpath + time_str + function.__name__ + ".png"
            )
            fail_screenshot.update(
                {function.__name__: self.driver.get_screenshot_as_base64()}
            )
            raise

    return get_error_image


"""业务方法封装"""


class Operation(object):
    def __init__(self, driver):
        self.driver = driver

    """封装操作方法-上下左右滑动"""

    # 参数：t--滑动时间
    def swipeUp(self, x1=0.5, y1=0.85, y2=0.15, t=500):
        l = self.driver.get_window_size()
        log.info("上滑页面")
        x1_value = l["width"] * x1
        y1_value = l["height"] * y1
        y2_value = l["height"] * y2
        time.sleep(1)
        return self.driver.swipe(x1_value, y1_value, x1_value, y2_value, t)

    def swipeDown(self, x1=0.5, y1=0.15, y2=0.85, t=500):
        l = self.driver.get_window_size()
        log.info("下滑页面")
        x1_value = l["width"] * x1
        y1_value = l["height"] * y1
        y2_value = l["height"] * y2
        time.sleep(1)
        return self.driver.swipe(x1_value, y1_value, x1_value, y2_value, t)

    def swipeRight(self, x1=0.15, y1=0.5, x2=0.85, t=500):
        l = self.driver.get_window_size()
        log.info("右滑页面")
        x1_value = l["width"] * x1
        y1_value = l["height"] * y1
        x2_value = l["width"] * x2
        # print(x1, y1, x2)
        time.sleep(1)
        return self.driver.swipe(x1_value, y1_value, x2_value, y1_value, t)

    def swipeLeft(self, x1=0.85, y1=0.5, x2=0.15, t=500):
        l = self.driver.get_window_size()
        log.info("左滑页面")
        x1_value = l["width"] * x1
        y1_value = l["height"] * y1
        x2_value = l["width"] * x2
        # print(x1, y1, x2)
        time.sleep(1)
        return self.driver.swipe(x1_value, y1_value, x2_value, y1_value, t)

    """重写定位方法"""

    def new_find_element(self, *loc, outtime=10):
        try:
            WebDriverWait(self.driver, outtime).until(
                lambda driver: driver.find_element(*loc)
            )
            return self.driver.find_element(*loc)
        except Exception:
            log.error("页面中找不到元素：{}".format(loc))
            return None

    def new_find_elements(self, *loc, outtime=10):
        try:
            WebDriverWait(self.driver, outtime).until(
                lambda driver: driver.find_elements(*loc)
            )
            return self.driver.find_elements(*loc)
        except Exception:
            log.error("页面中找不到元素：{}".format(loc))
            return None

    # 根据type选择不同的方法
    def locateElement(self, locate_type, value):
        # 定位元素
        if locate_type == "id":
            return self.driver.find_element_by_id(value)
        elif locate_type == "name":
            return self.driver.find_element_by_name(value)
        elif locate_type == "tag":
            return self.driver.find_element_by_tag_name(value)
        elif locate_type == "class":
            return self.driver.find_element_by_class_name(value)
        elif locate_type == "text":
            return self.driver.find_element_by_link_text(value)
        elif locate_type == "partial":
            return self.driver.find_element_by_partial_link_text(value)
        elif locate_type == "xpath":
            return self.driver.find_element_by_xpath(value)
        elif locate_type == "css":
            return self.driver.find_element_by_css_selector(value)

    """判断页面元素"""

    # 判断页面元素在页面源码中是不是存在
    def Element(self, *args):
        # print('*args------',*args)
        # print('*arg1-------',args[1])
        # print('page_source-----',self.driver.page_source)
        source = self.driver.page_source
        if args[0] in source:
            log.info("元素", args[0], "存在！")
            return True
        else:
            log.error("元素", args[0], "不存在！")
            return False

    # 判断页面元素是不是存在
    def isElementExist(self, *loc, outtime=5):
        # 元素存在返回True，不存在False
        element = self.new_find_element(*loc, outtime=outtime)
        if element:
            return True
        else:
            return False

    # 屏幕截图
    def screenShot(self):
        """屏幕截图"""
        timestrmap = time.strftime("%Y%m%d_%H.%M.%S")
        # print('---',timestrmap)
        file_name = timestrmap
        # print('filename---',file_name)
        resultpath = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/Report/images/"
        )
        # print('result---',resultpath)
        dir = resultpath + file_name + ".png"
        # print('dir----',dir)
        log.info("screenshot:", timestrmap, ".png")
        self.driver.get_screenshot_as_file(dir)

    def adbSendText(self, text, device_name):
        adb1 = "adb -s {} shell ime set com.sohu.inputmethod.sogou/.SogouIME".format(
            device_name
        )
        adb2 = "adb -s {} shell input text %s".format(device_name, text)
        adb3 = "adb -s {} shell ime set io.appium.android.ime/.UnicodeIME".format(
            device_name
        )
        # print(adb2)
        os.system(adb1)
        os.system(adb2)
        # os.system(adb3)
        self.driver.keyevent(66)

    # 切换到搜狗输入法
    def adbSend_input(self, device_name):
        adb = "adb -s {} shell ime set com.sohu.inputmethod.sogou/.SogouIME".format(
            device_name
        )
        os.popen(adb)
        time.sleep(1)

    # 切换到appium输入法
    def adbSend_appium(self, device_name):
        adb = "adb -s {} shell ime set io.appium.settings/.UnicodeIME".format(device_name)
        os.popen(adb)
        time.sleep(1)

    # 切换输入法进行输入文字点击搜索（整合）
    def adb_send_input(
        self, element_id, element_value, text_value, device_name, key_value=66
    ):
        self.driver.activate_ime_engine("com.iflytek.inputmethod.google/com.iflytek.inputmethod.FlyIME")
        time.sleep(1)
        self.new_find_element(element_id, element_value).send_keys(text_value)
        self.driver.keyevent(key_value)
        self.adbSend_appium(device_name)

    # 获取toast
    def get_toast(self, outtime=5):
        """
        获取toast信息
        @return: 返回toast内容
        """
        try:
            WebDriverWait(self.driver, outtime, 0.01).until(
                lambda driver: driver.find_element(By.XPATH, "//*[@class='android.widget.Toast']")
            )
            return self.driver.find_element(By.XPATH, "//*[@class='android.widget.Toast']").text
        except Exception as e:
            log.error(error_format(e))
            return None


    # 搜索老板
    def search_boss(self, name):
        self.name = name
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_1").click()
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/home_tab2").click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/txt_search_copy1"
        ).click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/et_search_input"
        ).send_keys(self.name)

    # 搜公司
    def search_company(self, company):
        self.cpmpany = company
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/home_tab1").click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/txt_search_copy1"
        ).click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/search_input_et"
        ).send_keys(company)

    # 判断登录
    def is_login(self, back_max=30):
        back_cnt = 0
        while True:
            if back_cnt > back_max:
                break
            try:
                self.driver.find_element_by_id("com.tianyancha.skyeye:id/tab_iv_1")
                break
            except:
                self.driver.keyevent(4)
                back_cnt += 1
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
        time.sleep(0.5)
        # self.driver.find_element_by_xpath("// *[ @class ='android.widget.TextView' and @ text='VIP会员可无限次查看老板详情']").click()

        try:
            self.driver.find_element_by_xpath(
                "//*[@class ='android.widget.TextView'and@text='立即登录']"
            )
        except NoSuchElementException:
            log.info("用户已登录")
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_1").click()
            return True
        except Exception as e:
            log.error(e)
        else:
            log.info("用户未登录")
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_1").click()
            return False

    # 登录方法
    def login(self, phone_num, password, app_version="11.8.0", back_max=30):
        back_cnt = 0
        self.phone_num = phone_num
        self.password = password
        # 判断是否在登录页面
        if app_version < "11.8.0":
            try:
                self.driver.find_element_by_xpath(
                    "//android.widget.TextView[@text='普通登录']"
                )
            except NoSuchElementException:
                while True:
                    if back_cnt > back_max:
                        break
                    try:
                        self.driver.find_element_by_id(
                            "com.tianyancha.skyeye:id/tab_iv_1"
                        )
                        break
                    except:
                        self.driver.keyevent(4)
                        back_cnt += 1
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tab_iv_5"
                ).click()
                self.new_find_element(
                    By.XPATH, "//android.widget.TextView[@text='立即登录']"
                ).click()
                if self.new_find_element(
                    By.XPATH,
                    "//*[@class='android.widget.TextView' and @text='本机号码一键登录']",
                    outtime=5,
                ):
                    self.new_find_element(
                        By.XPATH,
                        "//*[@class='android.widget.TextView' and @text='其他登录方式']",
                    ).click()
                else:
                    self.new_find_element(
                        By.XPATH, "//android.widget.TextView[@text='普通登录']"
                    ).click()
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/input_phone"
                ).send_keys(self.phone_num)
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/input_password"
                ).send_keys(self.password)
                time.sleep(1)
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/btn_login"
                ).click()
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tab_iv_1"
                ).click()
                # 的登录完成回到首页
                log.info("登录完成")
            else:
                self.new_find_element(
                    By.XPATH, "//android.widget.TextView[@text='普通登录']"
                ).click()
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/input_phone"
                ).send_keys(self.phone_num)
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/input_password"
                ).send_keys(self.password)
                time.sleep(1)
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/btn_login"
                ).click()
                # 登录完成停留当前页面
                log.info("登录完成")
        else:
            time.sleep(0.5)
            try:
                self.driver.find_element_by_xpath(
                    "//android.widget.TextView[@text='短信验证码登录']"
                )
            except NoSuchElementException:
                while True:
                    if back_cnt > back_max:
                        break
                    try:
                        self.driver.find_element_by_id(
                            "com.tianyancha.skyeye:id/tab_iv_1"
                        )
                        break
                    except:
                        self.driver.keyevent(4)
                        back_cnt += 1
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tab_iv_5"
                ).click()
                self.new_find_element(
                    By.XPATH, "//android.widget.TextView[@text='立即登录']"
                ).click()
                if self.new_find_element(
                    By.XPATH,
                    "//*[@class='android.widget.TextView' and @text='本机号码一键登录']",
                    outtime=5,
                ):
                    self.new_find_element(
                        By.XPATH,
                        "//*[@class='android.widget.TextView' and @text='其他登录方式']",
                    ).click()
                self.new_find_element(
                    By.XPATH, "//android.widget.TextView[@text='密码登录']"
                ).click()
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/et_phone"
                ).send_keys(self.phone_num)
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/input_password"
                ).send_keys(self.password)
                # 判断隐私弹窗是否勾选
                a = self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/cb_login_check"
                ).get_attribute("checked")
                if a != "true":
                    self.new_find_element(
                        By.ID, "com.tianyancha.skyeye:id/cb_login_check"
                    ).click()
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tv_login"
                ).click()
                # time.sleep(10)
                # 判断日报弹窗
                if self.new_find_element(
                    By.XPATH, "//*[@class='android.widget.TextView'and @text='监控日报']"
                ):
                    self.new_find_element(
                        By.ID, "com.tianyancha.skyeye:id/btn_finish"
                    ).click()
                    self.new_find_element(
                        By.ID, "com.tianyancha.skyeye:id/tab_iv_1"
                    ).click()
                    # 登录完成停留当前页面
                    log.info("登录完成")
                else:
                    self.new_find_element(
                        By.ID, "com.tianyancha.skyeye:id/tab_iv_1"
                    ).click()
                    log.info("登录完成")
            else:
                if self.new_find_element(
                    By.XPATH,
                    "//*[@class='android.widget.TextView' and @text='本机号码一键登录']",
                ):
                    self.new_find_element(
                        By.XPATH,
                        "//*[@class='android.widget.TextView' and @text='其他登录方式']",
                    ).click()
                self.new_find_element(
                    By.XPATH, "//android.widget.TextView[@text='密码登录']"
                ).click()
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/et_phone"
                ).send_keys(self.phone_num)
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/input_password"
                ).send_keys(self.password)
                # 判断隐私条件是否勾选
                a = self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/cb_login_check"
                ).get_attribute("checked")
                if a != "true":
                    self.new_find_element(
                        By.ID, "com.tianyancha.skyeye:id/cb_login_check"
                    ).click()
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tv_login"
                ).click()
                # time.sleep(10)
                # 判断日报弹窗
                if self.new_find_element(
                    By.XPATH, "//*[@class='android.widget.TextView'and @text='监控日报']"
                ):
                    self.new_find_element(
                        By.ID, "com.tianyancha.skyeye:id/btn_finish"
                    ).click()
                    # 登录完成停留当前页面
                    log.info("登录完成")

    # 退出登录
    def logout(self, back_max=30):
        back_cnt = 0
        while True:
            if back_cnt > back_max:
                break
            try:
                self.driver.find_element_by_id("com.tianyancha.skyeye:id/tab_iv_1")
                break
            except:
                self.driver.keyevent(4)
                back_cnt += 1
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_5").click()
        time.sleep(0.5)
        try:
            self.driver.find_element_by_xpath("//android.widget.TextView[@text='立即登录']")
        except NoSuchElementException:
            log.info("用户已登录")
            self.swipeUp()
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_setting").click()
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/btn_logout").click()
            self.new_find_element(By.ID, "android:id/button1").click()
            if self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tv_setting"):
                self.swipeDown()
            else:
                log.info('退登没回到我的页面')
            try:
                self.driver.find_element_by_xpath(
                    "// *[ @class ='android.widget.TextView'and@text='立即登录']"
                )
            except NoSuchElementException:
                self.screenShot()
                log.error("无法退出登录，请人工校验")
            else:
                self.new_find_element(
                    By.ID, "com.tianyancha.skyeye:id/tab_iv_1"
                ).click()
                log.info("已退出登录")

        else:
            log.info("用户未登录1")
            self.new_find_element(By.ID, "com.tianyancha.skyeye:id/tab_iv_1").click()

    # count数获取
    def count(self, elment, index=1):
        self.elment = elment
        str1 = self.elment.text
        log.info("打印数组--------", str1.split(), "----------")
        a = str1.split()[index]
        a = str(a).replace("条", "")
        a = str(a).replace("人", "")
        a = str(a).replace("个", "")
        return int(a)

    # 正则匹配文本中的数字，适用于 查找count数
    def count_num(self, element_id, element_value):
        import re

        try:
            count_text = self.new_find_element(element_id, element_value).text
            match = re.search(r"([1-9]\d*)", count_text).group()
        except Exception as e:
            match = 0
        return int(match)

    def data_list_count(self, *loc):
        """
        数据列表页count总数计算，翻页也可统计
        :param loc: 元素
        :return:统计到的item数量
        """
        all_item = dict()
        screen_size = self.driver.get_window_size()
        items = self.new_find_elements(*loc)
        if items:
            for i in items:
                key1 = i.text
                if key1 in all_item:
                    all_item[key1] += 1
                else:
                    all_item[key1] = 1
        print("1找")
        while True:
            before = len(all_item)

            self.driver.swipe(
                0.5 * screen_size["width"],
                0.8 * screen_size["height"],
                0.5 * screen_size["width"],
                0.5 * screen_size["height"],
                1300,
            )
            print("滑")
            items = self.new_find_elements(*loc)
            if items:
                for i in items:
                    key1 = i.text
                    if key1 in all_item:
                        all_item[key1] += 1
                    else:
                        all_item[key1] = 1
            print("找")
            after = len(all_item)
            if after > before:
                print("比较")
                continue
            else:
                print("再滑")
                self.driver.swipe(
                    0.5 * screen_size["width"],
                    0.8 * screen_size["height"],
                    0.5 * screen_size["width"],
                    0.4 * screen_size["height"],
                    1500,
                )
                items = self.new_find_elements(*loc)
                if items:
                    for i in items:
                        key1 = i.text
                        if key1 in all_item:
                            all_item[key1] += 1
                        else:
                            all_item[key1] = 1
                print("再找")
                after = len(all_item)
                if after > before:
                    print("再比较")
                    continue
                else:
                    print("到底了")
                    print(all_item)
                    print(len(all_item))
                    return len(all_item)

    def swipe_up_while_ele_located(
        self, *loc, click=False, times=10, group=False, check_cover=False
    ):
        """
        定位不到元素向上滑动循环定位直到达到最大次数限制并且点击
        :param times: 查找次数
        :param loc: 定位元素
        :param click: 是否点击找到的元素
        :param group: 是否使用find_elements
        :param check_cover: 是否判断和问大家按钮重合，默认不判断
        :return: element
        """
        count = 0
        timeout = 8
        screen_size = self.driver.get_window_size()
        ele = None
        while True:
            if count == times:
                break
            else:
                if group:
                    ele = self.new_find_elements(*loc, outtime=timeout)
                else:
                    ele = self.new_find_element(*loc, outtime=timeout)
            if ele:
                if check_cover:
                    y1 = ele.location["y"]
                    height1 = ele.size["height"]
                    y2 = self.new_find_element(
                        By.ID, "com.tianyancha.skyeye:id/iv_ask"
                    ).location["y"]
                    if y2 - 20 < y1 + height1:
                        self.driver.swipe(
                            200, y1 + height1, 200, 0.6 * screen_size["height"], 10000
                        )
                if click and not group:
                    ele.click()
                break
            else:
                self.driver.swipe(
                    0.5 * screen_size["width"],
                    0.8 * screen_size["height"],
                    0.5 * screen_size["width"],
                    0.4 * screen_size["height"],
                    1500,
                )
                count += 1
                timeout = 3
        return ele

    def all_count_compute_v1(self, *loc):
        """
        维度列表页count数统计
        :param xpath: count顶层元素
        :return:
        """
        res = dict()
        screen_large = self.driver.get_window_size()
        # xpath = """//*[@resource-id="com.tianyancha.skyeye:id/recyclerview"]/android.widget.RelativeLayout"""
        items = self.new_find_elements(*loc)
        for index, value in enumerate(items):
            key = ""
            # front_xpath = xpath + "[{}]".format(index + 1) + "/preceding-sibling::*[1]"
            # behind_xpath = xpath + "[{}]".format(index + 1) + "/following-sibling::*[1]"
            # all_text_xpath = (
            #     xpath + "[{}]".format(index + 1) + "//android.widget.TextView"
            # )
            if 0 < index < len(items) - 1:
                front_flag = True
                behind_flag = True
            else:
                front_flag = False
                behind_flag = False
            # else:
            #     front_flag = self.isElementExist(By.XPATH, front_xpath, outtime=2)
            #     behind_flag = self.isElementExist(By.XPATH, behind_xpath, outtime=2)
            if index == 0:
                # all_son = self.new_find_elements(By.XPATH, all_text_xpath)
                all_son = items[index].find_elements_by_class_name(
                    "android.widget.TextView"
                )
                for son in all_son:
                    if son.text:
                        key += son.text
                if key in res:
                    res[key] += 1
                else:
                    res[key] = 1
            else:
                if front_flag and behind_flag:
                    # all_son = self.new_find_elements(By.XPATH, all_text_xpath)
                    all_son = items[index].find_elements_by_class_name(
                        "android.widget.TextView"
                    )
                    for son in all_son:
                        if son.text:
                            key += son.text
                    if key in res:
                        res[key] += 1
                    else:
                        res[key] = 1
        while True:
            before = len(res)
            self.driver.swipe(
                0.5 * screen_large["width"],
                0.8 * screen_large["height"],
                0.5 * screen_large["width"],
                0.5 * screen_large["height"],
                2000,
            )
            items = self.new_find_elements(*loc)
            if len(items) == 2:
                item0_h = items[0].size["height"]
                self.driver.swipe(
                    0.5 * screen_large["width"],
                    0.8 * screen_large["height"],
                    0.5 * screen_large["width"],
                    0.8 * screen_large["height"] - item0_h * 0.5,
                    2500,
                )
            items = self.new_find_elements(*loc)
            for index, value in enumerate(items):
                key = ""
                # front_xpath = (
                #     xpath + "[{}]".format(index + 1) + "/preceding-sibling::*[1]"
                # )
                #
                # behind_xpath = (
                #     xpath + "[{}]".format(index + 1) + "/following-sibling::*[1]"
                # )

                # all_text_xpath = (
                #     xpath + "[{}]".format(index + 1) + "//android.widget.TextView"
                # )
                if 0 < index < len(items) - 1:
                    front_flag = True
                    behind_flag = True
                else:
                    front_flag = False
                    behind_flag = False
                # else:
                #     front_flag = self.isElementExist(By.XPATH, front_xpath, outtime=2)
                #     behind_flag = self.isElementExist(By.XPATH, behind_xpath, outtime=2)
                if front_flag and behind_flag:
                    # all_son = self.new_find_elements(By.XPATH, all_text_xpath)
                    all_son = items[index].find_elements_by_class_name(
                        "android.widget.TextView"
                    )
                    for son in all_son:
                        if son.text:
                            key += son.text
                    if key in res:
                        res[key] += 1
                    else:
                        res[key] = 1
                else:
                    pass
            after = len(res)
            if after > before:
                continue
            else:
                self.driver.swipe(
                    0.5 * screen_large["width"],
                    0.8 * screen_large["height"],
                    0.5 * screen_large["width"],
                    0.5 * screen_large["height"],
                    2000
                )
                items = self.new_find_elements(*loc)
                for index, value in enumerate(items):
                    key = ""
                    # front_xpath = (
                    #     xpath + "[{}]".format(index + 1) + "/preceding-sibling::*[1]"
                    # )
                    # behind_xpath = (
                    #     xpath + "[{}]".format(index + 1) + "/following-sibling::*[1]"
                    # )
                    # all_text_xpath = (
                    #     xpath + "[{}]".format(index + 1) + "//android.widget.TextView"
                    # )
                    if 0 < index < len(items) - 1:
                        front_flag = True
                        behind_flag = True
                    else:
                        front_flag = False
                        behind_flag = False
                    # else:
                    #     front_flag = self.isElementExist(
                    #         By.XPATH, front_xpath, outtime=2
                    #     )
                    #     behind_flag = self.isElementExist(
                    #         By.XPATH, behind_xpath, outtime=2
                    #     )
                    if front_flag and behind_flag:
                        all_son = items[index].find_elements_by_class_name(
                            "android.widget.TextView"
                        )
                        for son in all_son:
                            if son.text:
                                key += son.text
                        if key in res:
                            res[key] += 1
                        else:
                            res[key] = 1
                if after > before:
                    continue
                else:
                    key1 = ""
                    items = self.new_find_elements(*loc)
                    all_son = items[-1].find_elements_by_class_name(
                        "android.widget.TextView"
                    )
                    for son in all_son:
                        if son.text:
                            key1 += son.text
                    if key1 in res:
                        res[key1] += 1
                    else:
                        res[key1] = 1
                    print(len(res))
                    log.info(res)
                    return len(res)

    def ocr(self, *loc):
        """
        根据传入元素返回通过OCR识别的文字
        :param loc:元素
        :return: 识别到的文字
        """
        ele = self.new_find_element(*loc)
        if ele:
            temp_file = os.path.abspath(tempfile.gettempdir() + "/ocr_screen.png")
            location = ele.location
            size = ele.size
            box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
            # 先截取整个屏幕，存储至系统临时目录下
            self.driver.get_screenshot_as_file(temp_file)
            # 截取图片
            image = Image.open(temp_file)
            new_image = image.crop(box)
            new_image.save(temp_file)
            with open(temp_file, 'rb') as f:
                img = base64.b64encode(f.read())
            request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
            token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=xofwLMsnbiOhKz4mhOvoBff0&client_secret=vE3HLeVZicevDO7vYux9jI9lsSnV8gTY'
            params = {"image": img}
            token_res = requests.get(token_url).json()
            access_token = token_res['access_token']
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                result = ''
                for r in response.json()['words_result']:
                    result += r['words']
                print('传入元素OCR识别结果：', result)
                return result
        else:
            return '谁给你的自信觉得你传的元素能被找到 -。-！'

    def human_detail_name(self):
        import re
        name = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/person_name_tv').text
        human_detail_name = re.search(r"[\u4e00-\u9fa5]+", name).group()
        return human_detail_name
# if __name__ == '__main__':
#     d = Config_app()
#     d = d.config_app()
#     a = Operation(d)
#     a.swipeUp()

