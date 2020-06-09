# -*- coding: utf-8 -*-
# @Time    : 2019-12-24 14:48
# @Author  : XU
# @File    : cancel_update.py
# @Software: PyCharm

from selenium.webdriver.common.by import By
from Providers.logger import Logger, error_format
from common.operation import Operation

log = Logger("cancel_update").getlog()


def cancel_update(driver):
    """
    旧版本关闭更新弹窗
    :param driver:
    :return:
    """
    try:
        ele = Operation(driver).isElementExist(
            By.ID, "com.tianyancha.skyeye:id/btn_finish"
        )
        if ele:
            Operation(driver).new_find_element(
                By.ID, "com.tianyancha.skyeye:id/btn_finish"
            ).click()
    except Exception as e:
        log.error(error_format(e))
