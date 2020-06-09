#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/5 18:59
# @Author  : Soner
# @version : 1.0.0

def is_sex(car_id):
    if len(car_id) == 18:
        index = car_id[16]
    else:
        return "身份证位数不满18位"
    num = int(index)
    if (num % 2) == 0:
        sex = '女'
    else:
        sex = '男'
    return sex



if __name__ == '__main__':
    print(is_sex('3412251998****608X'))
