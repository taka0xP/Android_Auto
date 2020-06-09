#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 2:56 下午
# @Author  : wangwei
# @Site    : www.tianyancha.com
# @File    : imageDifferenceDemo.py
# @Software: PyCharm

from common.MyTest import MyTest
from common.ReadData import Read_Ex
from common.operation import Operation
from selenium.webdriver.common.by import By
from Providers.logger import Logger
from PIL import Image
import cv2
import numpy as np
import time
import os
import sys
import shutil

log = Logger('TestImageDifferenceDemo').getlog()


# 均值哈希算法
def aHash(img):
    # 缩放为8*8
    img = cv2.resize(img, (8, 8))
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# 差值感知算法
def dHash(img):
    # 缩放8*8
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# Hash值对比
def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] == hash2[i]:
            n = n + 1
    return n / 64.0


def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


# 通过得到RGB每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    image1 = cv2.resize(img1, size)
    image2 = cv2.resize(img2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return float(sub_data)


def get_screenshot_by_element(driver, element, image_path):
    # 获取元素 **loc参数示例：(By.ID, 'com.tianyancha.skyeye:id/sdv_banner')
    # 获取元素bounds
    location = element.location
    size = element.size
    box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
    # 先截取整个屏幕，存储至系统临时目录下
    try:
        driver.get_screenshot_as_file(image_path)
        # 截取图片
        image = Image.open(image_path)
        new_image = image.crop(box)
        new_image.save(image_path)
    except Exception:
        print('Exception catched')
        return False
    return True


# elements_location = [{'x': 0, 'y': 0, 'w': 10, 'h': 10}, {'x': 10, 'y': 10, 'w': 100, 'h': 100}, ]
def draw_frame(image_path, locations):
    image = cv2.imread(image_path)
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for loc in locations:
        x = loc['x']
        y = loc['y']
        w = loc['w']
        h = loc['h']
        draw_1 = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # cv2.imwrite("vertical_flip.png", draw_1)
        cv2.imwrite(image_path, draw_1)


def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def is_elements_show_good(driver, image_base, image_curr, case_name, step, elements_map, if_overwrite_base=False):
    full_image_base = "%s/%s_%s.png" % (image_base, case_name, step)
    full_image_curr = "%s/%s_%s.png" % (image_curr, case_name, step)
    # 截母图
    time.sleep(3)
    driver.save_screenshot(full_image_curr)
    # 指定跑基准图 or 基准图为空，则创建基准图
    if if_overwrite_base or not os.path.exists(full_image_base):
        driver.save_screenshot(full_image_base)
    # 抠子图
    eles = elements_map.keys()
    e = None
    locations = []

    # 计算相似度 子图 vs 基准子图
    for ele in eles:
        print(ele)
        if elements_map[ele]['type'] == 'id':
            e = driver.find_element(By.ID, elements_map[ele]['value'])
        elif elements_map[ele]['type'] == 'xpath':
            e = driver.find_element(By.XPATH, elements_map[ele]['value'])
        sub_image_curr = "%s/%s_%s_%s.png" % (image_curr, case_name, step, ele)
        get_screenshot_by_element(driver, e, sub_image_curr)
        sub_image_base = "%s/%s_%s_%s.png" % (image_base, case_name, step, ele)

        # 指定跑基准图 or 基准图为空，则创建基准图
        if if_overwrite_base or not os.path.exists(sub_image_base):
            shutil.copyfile(sub_image_curr, sub_image_base)

        if not is_images_similar(sub_image_base, sub_image_curr):
            location = {'x': e.location['x'], 'y': e.location['y'], 'h': e.size['height'], 'w': e.size['width']}
            print("location:{}, sub_image_curr={}".format(location, elements_map[ele]))
            locations.append(location)
    print("element locations lens=%d" % len(locations))
    if len(locations) == 0:
        return True
    draw_frame(full_image_curr, locations)
    return False


def is_images_similar(image1, image2):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)

    hash1 = dHash(img1)
    hash2 = dHash(img2)
    rate = cmpHash(hash1, hash2)
    print("%s%f" % ('差值哈希算法相似度：', rate))
    if rate >= 0.98:
        return True
    return False

    # hash1 = aHash(img1)
    # hash2 = aHash(img2)
    # rate = cmpHash(hash1, hash2)
    # print("%s%f" % ('均值哈希算法相似度：', rate))
    # if rate >= 0.9:
    #     return True
    # return False

    # rate = classify_hist_with_split(image1, image2)
    # print("%s%f" % ("三直方图算法相似度：", rate))
    # print("similary rate:%f, image1=%s, image2=%s" % (rate, image1, image2))
    # if rate >= 0.9:
    #     return True
    # return False


class TestImageDifferenceDemo(MyTest, Operation):
    a = Read_Ex()

    def clean_search_history(self):
        """从「查老赖首页」开始，进入「搜索中间页」，删除「最近搜索记录」"""
        self.new_find_element(By.XPATH, self.ELEMENT['dishonest_search_input']).click()

        res = self.isElementExist(By.ID, self.ELEMENT['dishonest_del_history'])
        # 如果「删除最近搜索按钮」存在：
        if res:
            self.new_find_element(By.ID, self.ELEMENT['dishonest_del_history']).click()
            self.new_find_element(By.ID, self.ELEMENT['dishonest_del_submit']).click()

        # 判断「删除最近搜索按钮」不存在，然后返回「查老赖」首页
        res = self.isElementExist(By.ID, self.ELEMENT['dishonest_del_history'])
        if not res:
            self.new_find_element(By.ID, self.ELEMENT['dishonest_mid_cancel']).click()

        print("清除查老赖搜索历史")

    def search_dishonest_from_dishonest_main(self, dishonest_word):
        self.into_dishonest_mid()
        self.search_dishonest_from_dishonest_mid(dishonest_word)

    def search_dishonest_from_dishonest_mid(self, dishonest_word):
        # ele = self.new_find_element(By.ID, self.ELEMENT['dishonest_mid_input'])
        self.adb_send_input(By.ID, self.ELEMENT['dishonest_mid_input'], dishonest_word)

    def setUp(self):
        self.if_overwrite_base = False
        a = Read_Ex()
        self.ELEMENT = a.read_excel('search_dishonest')
        self.class_name = self.__class__.__name__
        self.image_base_path = './images/base/%s' % self.class_name
        self.image_curr_path = './images/curr/%s' % self.class_name
        create_dir_not_exist(self.image_base_path)
        create_dir_not_exist(self.image_curr_path)

    def into_dishonest_main(self):
        self.new_find_element(By.XPATH, self.ELEMENT['dishonest_in_main']).click()
        print("进入查老赖首页页")

    def into_dishonest_mid(self):
        search_input = self.new_find_element(By.XPATH, self.ELEMENT['dishonest_search_input'])
        print("进入查老赖中间页")
        search_input.click()

    def test_demo(self):
        method_name = sys._getframe().f_code.co_name
        time.sleep(2)
        step = 'step1'  # 进入查老赖首页

        self.into_dishonest_main()

        # 图片校验（适合：①大块的；②稳定的；③样式的）
        # 校验步骤：
        # 1，定义需要校验的元素集合
        # 2，调用is_elements_show_good()方法。
        # is_elements_show_good(driver, image_base, image_curr, case_name, step, elements_map, if_overwrite_base=False):
        #   参数列表：
        #       driver，司机
        #       image_base，基准图所在目录，
        #       image_curr，当前执行图片存放目录，
        #       case_name，用例名，
        #       step，自定义步骤名，
        #       elements_map，需要校验的元素集合
        #       if_overwrite_base，是否覆盖基准图
        demo_step1_eles = {
            'scroll': {
                'type': 'xpath',
                'value': '//android.widget.LinearLayout[@resource-id="com.tianyancha.skyeye:id/ll_hot_search"]/following-sibling::android.widget.RelativeLayout'
            }
        }
        is_elements_show_good(self.driver, self.image_base_path, self.image_curr_path, method_name, step,
                              demo_step1_eles, self.if_overwrite_base)

        step = 'step2'  # 进入查老赖中间页
        self.clean_search_history()
        self.into_dishonest_mid()

        # 图片校验（适合：①大块的；②稳定的；③样式的）
        demo_step2_eles = {
            'search_title_rl': {'type': 'id',
                                'value': 'com.tianyancha.skyeye:id/search_title_rl'},
            'll_hot_search': {'type': 'id',
                              'value': 'com.tianyancha.skyeye:id/ll_hot_search'}
        }
        is_elements_show_good(self.driver, self.image_base_path, self.image_curr_path, method_name, step,
                              demo_step2_eles)

        step = 'step3'  # 查询
        word = '暴风'
        self.search_dishonest_from_dishonest_mid(word)

        # 图片校验（适合：①大块的；②稳定的；③样式的）
        demo_step3_eles = {
            'filter_header_multi_level_view': {
                'type': 'id',
                'value': 'com.tianyancha.skyeye:id/filter_header_multi_level_view'
            }
        }
        is_elements_show_good(self.driver, self.image_base_path, self.image_curr_path, method_name, step,
                              demo_step3_eles)

        assert 1 == 1


if __name__ == '__main__':
    origin_image = 'wee_full_screen_base.png'
    locations = [{'x': 0, 'y': 0, 'h': 768, 'w': 1080}, {'x': 936, 'y': 90, 'h': 72, 'w': 144}]
    draw_frame(origin_image, locations)
