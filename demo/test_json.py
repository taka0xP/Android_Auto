#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 09:16
# @Author  : Soner
# @version : 1.0.0

import os
import json
import sys



def read_json():
    with open('/Users/soner/Downloads/card_id.json', 'r', encoding='utf-8') as f:
        ret_dic = json.load(f)
    card_id_dict={}
    for i in ret_dic:
        card_id_dict[i['code']]= i['name']
    with open('/Users/soner/Downloads/card_id.json', 'w', encoding='utf-8') as e:
        json.dump(card_id_dict, e, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    read_json()
