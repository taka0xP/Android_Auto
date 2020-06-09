#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 11:14 下午
# @Author  : wangwei
# @Site    : www.tianyancha.com
# @File    : area.py
# @Software: PyCharm

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 10:57 上午
# @Author  : wangwei
# @Site    : www.tianyancha.com
# @File    : id_number.py
# @Software: PyCharm

import json
import os

PROVINCE_LEN = 2
CITY_LEN = 4
COUNTY_LEN = 6
SHORT_NAME_SUFFIX = ['省', '市', '县', '区']
AREA_NAME_LEN_MIN = 2
SHORT_NAME_THRESHOLD = 3


def load_area_code():
    parent_dir = os.path.split(os.path.realpath(__file__))[0]
    area_json_file = "{}/{}".format(parent_dir, "area_code.json")
    with open(area_json_file, 'r', encoding='utf-8') as fp:
        return json.load(fp)


def append_belong_to(belong_to, belong):
    if not belong in belong_to:
        return belong_to.append(belong)


def area_belong_to(area_name):
    if len(area_name) < AREA_NAME_LEN_MIN:
        return []
    areas = load_area_code()
    pro_keys = areas.keys()
    # city_keys = []
    # county_keys = []
    belong_to = []
    for pro_key in pro_keys:
        prov_name = areas[pro_key]['name']
        city_keys = areas[pro_key]['cities'].keys()
        for city_key in city_keys:
            city_name = areas[pro_key]['cities'][city_key]['name']
            if city_name == area_name or area_name in city_name:
                belong = {"level": "city", "prov": prov_name, "city": city_name}
                append_belong_to(belong_to, belong)
            county_keys = areas[pro_key]['cities'][city_key]['counties'].keys()
            for county_key in county_keys:
                county_name = areas[pro_key]['cities'][city_key]['counties'][county_key]['name']
                if county_name == area_name or \
                        area_name in county_name or \
                        county_name in area_name:
                    belong = {"level": "county", "prov": prov_name, "city": city_name, "county": county_name}
                    append_belong_to(belong_to, belong)
                if len(county_name) >= SHORT_NAME_THRESHOLD and county_name[-1] in SHORT_NAME_SUFFIX:
                    short_county_name = county_name[:-1]
                    if short_county_name in area_name:
                        belong = {"level": "county", "prov": prov_name, "city": city_name, "county": county_name}
                        append_belong_to(belong_to, belong)

    return belong_to


if __name__ == '__main__':
    areas = ['河北省保定市徐水区巨力路', '大连市甘井子区海茂街', '沧州', '沧州市', '河间', '河北河间', '沧州市献县', '庆阳', '区', '河北省河间市', '北京市昌平区', '河间市瀛洲镇',
             '鼓楼区', '河北']
    for area in areas:
        belong_to = area_belong_to(area)
        print("area:{}\tbelong_to:{}\n".format(area, belong_to))
