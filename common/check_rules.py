# -*- coding: utf-8 -*-
# @Time    : 2020-03-04 14:51
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : check_rules.py
# @Software: PyCharm
import re
import datetime


def check_time(date, is_compare=False):
    """
    校验时间格式是否正确,时间是否大于当前时间
    :param date:校验的时间
    :param is_compare:是否校验是否大于当前时间,默认不校验，校验传True
    :return:成功-True,失败-False
    """
    if date == "-":
        return True
    check_flag = re.match(
        r"[1,2][0, 9][0-9][0-9]-[0-9][0-9]-[0-3][0-9] ?(\d*:\d*:\d)?", date
    )
    if is_compare:
        if check_flag:
            patten = re.findall(r"\d\d*\d", date)
            if patten:
                compare = datetime.date(int(patten[0]), int(patten[1]), int(patten[2]))
                now = datetime.date.today()
                return compare < now
            else:
                return False
        else:
            return False
    else:
        if check_flag:
            return True
        else:
            return False


def is_bill_available(value, negative=False):
    """
    校验关于钱的字段展示是否正确
    :param value:展示的字段内容
    :param negative: 是否校验负数
    :return:成功-True，失败-False
    """
    if value == "-":
        return True
    if negative:
        pattern = re.compile(r"^-\d+(\.\d+)?(万)(人民币|美元|港币|新台币|元)?$")
    else:
        pattern = re.compile(r"^\d+(\.\d+)?(万)(人民币|美元|港币|新台币|元)?$")
    result = pattern.match(value)
    if result:
        return True
    else:
        return False


def is_percentage_available(percentage):
    """
    校验百分比类型是否合法
    :param percentage:获取到的百分比内容
    :return:成功-True，失败-False
    """
    if percentage == "-":
        return True
    else:
        check_flag = re.match(r"^\d\d{0,2}\.?\d*%$", percentage)
    if check_flag:
        return True
    else:
        return False


def operating_check(style, status):
    """
    校验营业状态是否合法
    :param status: 经营状态(str)
    :param style: 公司类型(int);1：普通公司；2：事业单位；3：律所；4：社会组织；5：香港公司；6：台湾公司；7：基金会
    :return:布尔值
    """
    operating_status = {
        1: [
            "开业",
            "在业",
            "存续",
            "迁入",
            "迁出",
            "吊销",
            "吊销，未注销",
            "吊销，已注销",
            "注销",
            "撤销",
            "停业",
            "清算",
            "其他",
        ],
        2: ["吊销", "注销", "证书废止", "证书过期", "冻结", "其他"],
        3: ["设立中", "正常", "注销", "吊销", "未年检", "其他"],
        4: ["申请中", "成立中", "正常", "注销", "注销中", "撤销", "移交", "未通过", "其他"],
        5: ["仍注册", "已告解散", "不再是独立的实体", "其他"],
        6: [
            "撤销",
            "注销",
            "废止",
            "未登记",
            "核准报",
            "核准认许",
            "核准许可登记",
            "核准设立",
            "接管",
            "解散",
            "破产",
            "迁他县市",
            "清理",
            "设立许可",
            "重整",
            "停工",
            "歇业",
            "生产中",
            "其他",
        ],
        7: ["暂无经营状态"],
    }
    if status == "-":
        return True
    else:
        if style in operating_status:
            if status in operating_status[style]:
                return True
            else:
                return False
        else:
            return False


# def check_email(email):
#     """
#     校验邮箱展示是否正确
#     :param email: 邮箱地址
#     :return:成功-True，失败-False
#     """
#     if email == "-":
#         return True
#     pattern = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
#     result = re.match(pattern, email)
#     if result:
#         return True
#     else:
#         return False


def check_post_code(value):
    """
    校验邮政编码是否正确
    :param value: str
    :return:正确-True，错误-False
    """
    if value == "-":
        return True
    pattern = "[0-9]{6}$"
    result = re.match(pattern, value)
    if result:
        return True
    else:
        return False


def check_postcode(postcode):
    """
    邮政编码校验
    :param postcode: str 邮编
    :return: bool
    """
    if postcode == '-':
        return True
    else:
        check_flag = re.match(r'[1-9]\d{5}(?!\d)', postcode)
        if check_flag:
            return True
        else:
            return False


def check_email(email):
    """
    邮箱地址校验
    :param email: str 邮箱地址
    :return: bool
    """
    if email == '-':
        return True
    flag = re.match(
        r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?", email)
    if flag:
        return True
    else:
        return False


def check_land_line(phone):
    """
    固话格式校验
    :param phone: 固话
    :return: bool
    """
    if phone == '-':
        return True
    flag = re.match(r"(\d{3}-)?\d{8}|\d{4}-\{7,8}", phone)
    if flag:
        return True
    else:
        return False


def check_url(url):
    """
    网址url格式校验
    :param url: str url
    :return: bool
    """
    if url == '-':
        return True
    flag = re.match(r"([a-zA-z]+://)?www.[^\s]*(com|cn)$", url)
    if flag:
        return True
    else:
        return False


if __name__ == "__main__":
    print(check_time("2018-09-27 00:90:99", is_compare=True))
    print(is_bill_available("18.01万元"))
    print(is_bill_available("0.10万"))
    print('-------',is_bill_available("15000万新台币"))
    print(is_bill_available("万新台币"))
    print(is_bill_available("1万"))
    print(is_bill_available("5500万"))
    print(is_bill_available("1.0"))
    print(is_bill_available("-1.0"))
    print(check_email('zhangyufeng@tianyancha.com'))
    print(check_time('1999-07-23'))
