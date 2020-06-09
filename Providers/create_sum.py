#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/21
# @Author  : Soner
# @version : 1.0.0

import os
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import re
from Data.model_map_name import mapping
import datetime


def create_summary(report_path, start, end):
    """
    解析子case测试报告并且在入参目录生成聚合报告
    :param report_path: 子用例运行报告存储目录
    :param start:用例开始执行时间
    :param end:用例结束执行时间
    :return: None
    """
    all_data = []
    name_data = []
    e_charts = []
    pass_num = 0
    failed_num = 0
    error_num = 0
    template_path = os.path.abspath(os.path.dirname(__file__))
    if os.path.isdir(report_path):
        all_case_reports = os.listdir(report_path)
        all_case_reports.sort()
        num = 1  # 具体case序号
        no = 1  # 模块序号
        # 从全部报告解析结果基础数据
        for file in all_case_reports:
            item = {
                'case_num': None,
                'case_name': None,
                'start_time': None,
                'run_time': None,
                'run_result': {
                    '通过': 0,
                    '失败': 0,
                    '错误': 0
                }
            }
            item.update({'case_num': str(num)})
            item.update({'case_name': os.path.splitext(file)[0]})
            file_path = os.path.join(report_path, file)
            soup = BeautifulSoup(open(file_path, 'rb'), 'lxml')
            start_time_tag = soup.select('#div_base > div.page-header > p:nth-child(2)')[0]
            start_time = start_time_tag.get_text()
            item.update({'start_time': start_time[6:]})
            run_time_tag = soup.select('#div_base > div.page-header > p:nth-child(3)')[0]
            run_time = run_time_tag.get_text()
            item.update({'run_time': run_time[6:]})
            run_num_tag = soup.select('#div_base > div.page-header > p:nth-child(4)')[0]
            run_num = run_num_tag.get_text()[4:]
            patten = re.compile('\d+')
            match_result = patten.findall(run_num)
            if len(match_result) == 3:
                item['run_result']['通过'] = int(match_result[0])
                item['run_result']['失败'] = int(match_result[1])
                item['run_result']['错误'] = int(match_result[2])
            if len(match_result) == 2:
                if '通过' in run_num and '失败' in run_num:
                    item['run_result']['通过'] = int(match_result[0])
                    item['run_result']['失败'] = int(match_result[1])
                elif '通过' in run_num and '错误' in run_num:
                    item['run_result']['通过'] = int(match_result[0])
                    item['run_result']['错误'] = int(match_result[1])
                else:
                    item['run_result']['失败'] = int(match_result[0])
                    item['run_result']['错误'] = int(match_result[1])
            if len(match_result) == 1:
                if '通过' in run_num:
                    item['run_result']['通过'] = int(match_result[0])
                elif '失败' in run_num:
                    item['run_result']['失败'] = int(match_result[0])
                else:
                    item['run_result']['错误'] = int(match_result[0])
            all_data.append(item)
            num += 1
        # 计算总体运行结果
        for data in all_data:
            pass_num = pass_num + data['run_result']['通过']
            failed_num = failed_num + data['run_result']['失败']
            error_num = error_num + data['run_result']['错误']
        # 计算模块对应负责人结果
        for rules in mapping:
            mid_compute = {
                'num': no,
                'file': None,
                'people': None,
                'count': 0,
                'failed': 0,
                'error': 0
            }
            for model in all_data:
                if model['case_name'].startswith(rules['rules']):
                    mid_compute.update({'file': rules['model']})
                    mid_compute.update({'people': rules['name']})
                    mid_compute.update({'count': mid_compute['count'] +
                                        model['run_result']['通过'] +
                                        model['run_result']['失败'] +
                                        model['run_result']['错误']})
                    mid_compute.update({'failed': mid_compute['failed'] + model['run_result']['失败']})
                    mid_compute.update({'error': mid_compute['error'] + model['run_result']['错误']})
            if mid_compute['file'] and mid_compute['people']:
                name_data.append(mid_compute)
            no += 1
        # print(name_data)
        for people in ['孙凯', '许思瑞', '张宇峰', '李佳颖', '王立轩', '李君']:
            mid_chart = {
                'value': 0, 'name': None
            }
            for chart in name_data:
                if chart['people'] == people:
                    mid_chart.update({'name':people})
                    mid_chart.update({'value': mid_chart['value'] + chart['failed'] + chart['error']})
            e_charts.append(mid_chart)
        # print(e_charts)
        # start = datetime.datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f')
        # end = datetime.datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S.%f')
        take_time = str(end - start)
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template('SummaryTemplate.html')
        with open(os.path.join(report_path, 'index.html'), 'w+') as f:
            html_content = template.render(pass_num=pass_num,
                                           failed_num=failed_num,
                                           error_num=error_num,
                                           all_data=all_data,
                                           mapping_data=name_data,
                                           charts_data=e_charts,
                                           start_time=str(start)[0:19],
                                           end_time=str(end)[0:19],
                                           take_time=str(take_time)[0:7])
            f.write(html_content)
    else:
        raise OSError('传入报告路径参数不存在，请确认！！！！')
    return pass_num, failed_num, error_num


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    import time
    time.sleep(3)
    end_time = datetime.datetime.now()
    create_summary('/Users/sunkai/word_download/android-auto/report/HTML/2020-05-26-105700', start_time, end_time)
