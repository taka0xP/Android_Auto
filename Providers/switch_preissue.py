#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/22 09:50
# @Author  : Soner
# @version : 1.0.0
from common.operation import Operation
from Providers.skip_guide import skip_guide, agree_license
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from Providers.cancel_update import cancel_update
import time


def preissue(driver):
    # 判断是否是测试包，是的话，切换环境
    scene = Operation(driver).isElementExist(By.ID, "android:id/button1")
    if scene:
        driver.find_element_by_id("android:id/button1").click()
        # 切换到 我的
        WebDriverWait(driver, 5, 0.5).until(
            EC.presence_of_element_located((By.ID, "com.tianyancha.skyeye:id/tab_iv_5"))
        ).click()
        # 下滑，寻找 设置
        switch = Operation(driver)
        switch.swipeUp()
        WebDriverWait(driver, 5, 0.5).until(
            EC.presence_of_element_located(
                (By.ID, "com.tianyancha.skyeye:id/tv_setting")
            )
        ).click()
        # 判断是否需要切换环境
        try:
            # 是否为测试包
            presence = switch.isElementExist(By.ID, "com.tianyancha.skyeye:id/test")
            if presence:
                presence_text = WebDriverWait(driver, 5, 0.5).until(
                    EC.presence_of_element_located(
                        (By.ID, "com.tianyancha.skyeye:id/test")
                    )
                )
                if presence_text.text == "测试":
                    # 点击 切换环境 按钮
                    WebDriverWait(driver, 5, 0.5).until(
                        EC.presence_of_element_located(
                            (By.ID, "com.tianyancha.skyeye:id/btn_change_environment")
                        )
                    ).click()
                    WebDriverWait(driver, 3, 0.5).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//*[@resource-id="com.tianyancha.skyeye:id/tv_name" and @text="预发环境"]',
                            )
                        )
                    ).click()
                    # time.sleep(1)
                    driver.close_app()
                    # time.sleep(1)
                    print("重启APP")
                    driver.launch_app()
                    # 点击同意用户协议
                    agree_license(driver)
                    # 跳过引导页
                    skip_guide(driver)
                    # 跳过更新提示
                    cancel_update(driver)
                    WebDriverWait(driver, 5, 0.5).until(
                        EC.presence_of_element_located((By.ID, "android:id/button1"))
                    ).click()
                    print("环境切换完毕")
                    return
            WebDriverWait(driver, 5, 0.5).until(
                EC.presence_of_element_located(
                    (By.ID, "com.tianyancha.skyeye:id/iv_back")
                )
            ).click()
            WebDriverWait(driver, 5, 0.5).until(
                EC.presence_of_element_located(
                    (By.ID, "com.tianyancha.skyeye:id/tab_iv_1")
                )
            ).click()
        except Exception as e:
            print(e)
