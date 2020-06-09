#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31
# @Author  : Soner
# @version : 1.0.0

import random
import string

class RandomStr():

    def zh_cn(self, len):
        """
        根据给定的 len 生成中文字符
        @param len:
        @return:
        """
        # 2W 个汉子
        # return_str = ''.join(chr(random.randint(0x4e00, 0x9fbf)) for i in range(len))
        # 常用 6K 个汉子
        temp_str = ''.join(
            # 此写法适用于python3.6以上
            # bytes.fromhex(f'{random.randint(0xb0, 0xF7):x}{random.randint(0xa1, 0xf9):x}').decode('gb2312') for i in
            bytes.fromhex("{:x}{:x}".format(random.randint(0xb0, 0xf7), random.randint(0xa1, 0xf9))).decode('gb2312') for i in
            range(len))
        return temp_str

    def en_us(self, len):
        """
        随机生成 a-z和A-Z
        @param len:
        @return:
        """
        chars = string.ascii_letters
        temp_str = ''.join(random.choice(chars) for i in range(len))
        return temp_str

    def digit(self, len):
        """
        随机生成 0-9
        @param len:
        @return:
        """
        chars = string.digits
        temp_str = ''.join(random.choice(chars) for i in range(len))
        return temp_str

    def special_chars(self, len):
        """
        生成特殊字符
        @param len:
        @return:
        """
        chars = "!@#$%^&*()_+=-<>?"
        temp_str = ''.join(random.choice(chars) for i in range(len))
        return temp_str

    def mixing_one(self, len):
        """
        混合 a-z和A-Z、0-9
        @param len:
        @return:
        """
        chars = string.ascii_letters + string.digits
        temp_str = ''.join(random.choice(chars) for i in range(len))
        return temp_str

    def mixing_two(self, len):
        """
        混合 a-z和A-Z、0-9、"!@#$%^&*()_+=-<>?"
        @param len:
        @return:
        """
        chars = string.ascii_letters + string.digits + '"!@#$%^&*()_+=-<>?"'
        temp_str = ''.join(random.choice(chars) for i in range(len))
        return temp_str

    def mixing_three(self, len):
        """
        混合 a-z和A-Z、0-9、中文
        @param len:
        @return:
        """
        temp = [bytearray.fromhex('%x %x' % (c+0xa0, p+0xa0)) for c in range(16, 56) for p in range(1, 95)]
        chineses = ''.join([str(a.decode('gb2312')) for a in temp[:-5]])
        chars = string.ascii_letters + string.digits + chineses
        temp_str = ''.join(random.choice(chars) for i in range(len))
        return temp_str

if __name__ == '__main__':
    st = RandomStr()
    print(st.zh_cn(100))
