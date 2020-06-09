# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 19:58
# @Author  : ZYF
# @File    : ReadData.py
import pymysql.cursors
import xlrd
import os


class Read_Ex():
    def read_excel(self, sheet_name):
        self.sheet_name = sheet_name
        # print(sheet_name)
        dir = 'Data'
        # 找到文件
        current_dir = os.path.abspath(os.path.dirname(__file__))  # 本地文件
        excel_dir = os.path.dirname(current_dir) + '/' + dir
        # 打开Excel表格，填写路径
        workbook = xlrd.open_workbook(excel_dir + '/' + '{}.xlsx'.format(sheet_name))
        # print(workbook)

        # # 获取sheet页---按sheet名称
        # sheets = workbook.sheet_names()
        # # print('获取表格的sheet页：', sheets)
        # sheet = workbook.sheet_by_name(self.sheet_name)
        # print(sheet)

        # 打开sheet页
        sheet_value = workbook.sheet_by_name(self.sheet_name)
        # print(sheet_value)

        # 获取sheet页行数
        row_nu = sheet_value.nrows
        print('选取 {} sheet页的行数 {}'.format(sheet_name, row_nu))

        # 取表格数据到字典
        a = []
        b = []
        c = []
        for i in range(1, row_nu):
            self.row_value1 = sheet_value.row_values(i)[0]  # 取表格里面的值
            self.row_value2 = sheet_value.row_values(i)[1]  # 取表格里面的值
            # self.row_value3 = sheet_value.row_values(i)[2]
            a.append(self.row_value1)
            b.append(self.row_value2)
            # c.append(self.row_value3)

            ELEMENT = dict(zip(a, b))
        # print('字典集合：', ELEMENT)
        return ELEMENT


config = {
    'host': '10.2.22.232',
    'port': 3306,
    'user': 'root',
    'password': 'stdgn',
    'db': 'android_auto_elements',
    'charset': 'utf8'
}


class DB(object):
    def __init__(self):
        self.db = pymysql.connect(**config)
        self.cursor = self.db.cursor()

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(e)
            print('sql语句执行失败')

    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()

    def get_element(self, table_name, ele_type):
        """
        :param ele_type: 需要获取元素模块类型，1-查公司，2-查老板， 3查关系， 4-查老赖，5-人员详情页，6-公司详情页，7-企业预核名'
        :param table_name: 数据库元素存放版本表（eg: elements_v11.8.0）
        :return: 字典类型：格式： {'元素名称': '元素'}
        """
        elements = {}
        sql = "SELECT ele_key, ele_value FROM `{}` WHERE `ele_mode`='{}';".format(table_name, ele_type)
        result = self.execute_sql(sql)
        self.close()
        for ele in result:
            elements[ele[0]] = ele[1]
        return elements


if __name__ == '__main__':
    # a = Read_Ex()
    # b = a.read_excel('Search_boss')
    # print(b)
    db = DB()
    print(db.get_element('elements_v11.8.0', '5'))
