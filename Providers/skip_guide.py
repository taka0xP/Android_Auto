#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 15:31
# @Author  : Soner
# @version : 1.0.0

from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from common.operation import Operation
from Providers.logger import Logger

log = Logger("skip_guide").getlog()


def skip_guide(driver, x1=0.8, x2=0.1, outtime=5):
    """
    跳过引导页
    :param driver:
    :param x1:
    :param x2:
    :param outtime:
    :return:
    """
    try:
        element = Operation(driver).isElementExist(
            By.ID, "com.tianyancha.skyeye:id/launch_vp", outtime=outtime
        )
        win = driver.get_window_size()
        if element:
            for i in range(3):
                TouchAction(driver).press(
                    x=win["width"] * x1, y=win["height"] * 0.5
                ).move_to(
                    x=win["width"] * x2, y=win["height"] * 0.5
                ).release().perform()
            driver.find_element_by_id("com.tianyancha.skyeye:id/launch_btn").click()
        # 是否存在 “显示在其他应用的上层”
        bar_title = Operation(driver).isElementExist(
            By.ID, "android:id/title", outtime=3
        )
        if bar_title:
            driver.keyevent(4)
    except Exception as e:
        log.error(e)


def agree_license(driver, outtime=5):
    try:
        element = Operation(driver).isElementExist(
            By.ID, "com.tianyancha.skyeye:id/btn_agreement_next", outtime=outtime
        )
        if element:
            Operation(driver).new_find_element(
                By.ID, "com.tianyancha.skyeye:id/btn_agreement_next"
            ).click()
            log.info("点击同意用户协议和隐私政策！")
        else:
            log.info("点击同意用户协议失败！！！")
    except Exception as e:
        log.error(e)
