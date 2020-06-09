#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 09:34
# @Author  : Soner
# @version : 1.0.0

import os
import json

class card_operation():
    def __init__(self):
        #  获取项目根目录
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def transorm_json(self):
        # 将列表型dict转为json，后续添加更多支持方式
        # 读取待转换的文件
        with open(self.BASE_DIR+'/Data/card_id_temp.json', 'r', encoding='utf-8') as f:
            ret_dic = json.load(f)
        # 将待转换的文件，转为dict
        card_id_dict = {}
        for i in ret_dic:
            card_id_dict[i['code']] = i['name']
        # 字典保存为json
        with open(self.BASE_DIR+'/Data/card_id.json', 'w', encoding='utf-8') as e:
            json.dump(card_id_dict, e, ensure_ascii=False, indent=4)

    def read(self):
        # 获取 json文件内容转为dict
        card_dir = self.BASE_DIR + '/Data/card_id.json'
        with open(card_dir, 'r', encoding='utf-8') as f:
            card_json = json.load(f)
        return card_json

    def check_sex(self, card_id_num):
        "检查性别"
        if len(card_id_num) == 18:
            index = card_id_num[16]
        else:
            return "身份证位数不满18位"
        num = int(index)
        if (num % 2) == 0:
            sex = '女'
        else:
            sex = '男'
        return sex

    def check_region(self, card_id_num):
        "校验身份证所属区域"
        if len(card_id_num) >= 6:
            card_num = card_id_num[:6]
            if card_num.isdigit():
                card_json = self.read()
                if card_num in card_json:
                    return card_json[card_num]
                else:
                    return "未查询到该身份证所属区域"
            else:
                return "身份证编号非法"
        else:
            return "身份证位数不满足最少6位"



if __name__ == '__main__':
    print(card_operation().check_region("520302"))
