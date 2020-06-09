#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 10:57 上午
# @Author  : wangwei
# @Site    : www.tianyancha.com
# @File    : id_number.py
# @Software: PyCharm

import json
import os
import re

PROVINCE_LEN = 2
CITY_LEN = 4
COUNTY_LEN = 6
SEX_POS = [16, 17]
BIRTH_YEAR_POS = [6, 10]
BIRTH_MONTH_POS = [10, 12]
BIRTH_DAY_POS = [12, 14]
ID_NUMBER_PATTEN = '^[1-9][0-9]{5}'
AREA_FILTER = ['市辖区']


def load_area_code():
    parent_dir = os.path.split(os.path.realpath(__file__))[0]
    area_json_file = "{}/{}".format(parent_dir, "area_code.json")
    with open(area_json_file, 'r', encoding='utf-8') as fp:
        return json.load(fp)


def get_section_code(id, start, end):
    if len(id) < end:
        return ""
    section_code = id[start:end]

    if not section_code.isdigit():
        section_code = ""
    return section_code


def get_sex(id, start, end):
    sex = ""
    sex_code = get_section_code(id, start, end)
    if sex_code and int(sex_code) % 2 == 0:
        sex = '女'
    elif sex_code and int(sex_code) % 1 == 0:
        sex = '男'
    return sex


def is_valid_id_number(id_number):
    if re.match(ID_NUMBER_PATTEN, id_number):
        return True
    return False


def area_filer(area_name):
    if area_name in AREA_FILTER:
        return ""
    return area_name


def struct_id_number(id_number):
    struct_id_num = {"id": id_number, "codes": {"province": "", "city": "", "county": ""},
                     "province": "", "city": "", "county": "", "birth_year": "",
                     "birth_month": "", "birth_day": "", "sex": ""}
    if not is_valid_id_number(id_number):
        return struct_id_num

    province_name = ""
    city_name = ""
    county_name = ""
    areas = load_area_code()
    province_code = get_section_code(id_number, 0, PROVINCE_LEN)
    city_code = get_section_code(id_number, 0, CITY_LEN)
    county_code = get_section_code(id_number, 0, COUNTY_LEN)
    birth_year = get_section_code(id_number, BIRTH_YEAR_POS[0], BIRTH_YEAR_POS[1])
    birth_month = get_section_code(id_number, BIRTH_MONTH_POS[0], BIRTH_MONTH_POS[1])
    birth_day = get_section_code(id_number, BIRTH_DAY_POS[0], BIRTH_DAY_POS[1])
    sex = get_sex(id_number, SEX_POS[0], SEX_POS[1])

    try:
        province = areas[province_code]
        if province:
            province_name = province['name']
            if province['cities']:
                city = province['cities'][city_code]
                if city:
                    city_name = city['name']
                    if city['counties']:
                        county = city['counties'][county_code]
                        if county:
                            county_name = county['name']
    except KeyError as e:
        pass

    struct_id_num['id'] = id_number
    struct_id_num['codes']['province'] = province_code
    struct_id_num['codes']['city'] = city_code
    struct_id_num['codes']['county'] = county_code
    struct_id_num['province'] = province_name
    struct_id_num['city'] = area_filer(city_name)
    struct_id_num['county'] = area_filer(county_name)
    struct_id_num['birth_year'] = birth_year
    struct_id_num['birth_month'] = birth_month
    struct_id_num['birth_day'] = birth_day
    struct_id_num['sex'] = sex
    return struct_id_num


if __name__ == '__main__':
    id_nums = ['370205621219253', '4101021965****2538', '1101021983****0878', '******201309201139',
               '13098420130920****',
               '1309842013', '510101', '130201', '110101']
    for id_num in id_nums:
        struct_id_num = struct_id_number(id_num)
        print("id:{}\t\tstruct_id:{}".format(id_num, struct_id_num))
