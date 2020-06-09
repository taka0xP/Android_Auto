# -*- coding: utf-8 -*-
# @Time    : 2019-12-24 14:54
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : back_to_index.py
# @Software: PyCharm


def back_to_index(driver):
    """
    :param driver: driver对象
    :return: None
    """
    back_count = 0
    while True:
        back_count += 1
        if back_count > 10:
            break
        else:
            try:
                driver.find_element_by_id('com.tianyancha.skyeye:id/tab1').click()
                break
            except:
                driver.keyevent(4)
    print('Go Back Index Page Success !!!')
