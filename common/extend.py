# -*- coding: utf-8 -*-
# @Time    : 2019-11-19 17:46
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : extend.py
# @Software: PyCharm
import os
import platform
import tempfile
import shutil
from functools import reduce
from PIL import Image
import cv2
import numpy as np

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")


class Extend(object):

    def __init__(self, driver):
        self.driver = driver

    def get_screenshot_by_element(self, element):
        # 获取元素 **loc参数示例：(By.ID, 'com.tianyancha.skyeye:id/sdv_banner')
        # 获取元素bounds
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])
        # 先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)
        # box = (0, 1032, 1080, 1215)  # 把banner大小直接写死，取消动态获取
        # 截取图片
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y):
        # 自定义截取范围
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    def write_to_file(self, dirPath, imageName, form="png"):
        # 将截屏文件复制到指定目录下
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        shutil.copyfile(TEMP_FILE, PATH(dirPath + "/" + imageName + "." + form))

    def load_image(self, image_path):
        # 加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" % image_path)

    def same_as(self, load_image, percent):
        # 对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image.open(TEMP_FILE)
        image2 = load_image

        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        differ = math.sqrt(
            reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, histogram1, histogram2))) / len(histogram1))
        if differ <= percent:
            print(differ)
            return True
        else:
            print(differ)
            return False

    # 计算单通道的直方图的相似值
    def calculate(self, image1, image2):
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
    def classify_hist_with_split(self, banner_path, size=(256, 256)):
        # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        img1 = cv2.imread(banner_path)
        img2 = cv2.imread(TEMP_FILE)
        image1 = cv2.resize(img1, size)
        image2 = cv2.resize(img2, size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += self.calculate(im1, im2)
        sub_data = sub_data / 3
        return float(sub_data)

# if __name__ == '__main__':
#     img1 = cv2.imread('../pics/base/80351256.png')
#     img2 = cv2.imread('../pics/80351256.png')
#
#     n = classify_hist_with_split(img1, img2)
#     print("%s%f" % ("三直方图算法相似度：", n))
