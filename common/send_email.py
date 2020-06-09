# -*- coding: utf-8 -*-
# @Time    : 2019-10-14 09:39
# @Author  : sunkai
# @Email   : sunkai@tianyancha.com
# @File    : send_email.py
# @Software: PyCharm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import zipfile
import os
import datetime
import time

sender = 'sunkai@tianyancha.com'
password = 'a7w3jSdDRHRGswe7'
rec_list = ['zhangyufeng@tianyancha.com', 'lijiaying@tianyancha.com', 'wanglixuan@tianyancha.com',
            'xusirui@tianyancha.com', 'wangwei@tianyancha.com', 'sunkai@tianyancha.com',
            'lijun@tianyancha.com']
receivers = ','.join(rec_list)


def sendmail(report_path, start_time, end_time, pass_num, failed_num, error_num):
    try:
        file_list = []
        zip_path = os.path.join(report_path, 'report.zip')
        for root, dirs, files in os.walk(report_path):
            for name in files:
                file_list.append(os.path.join(root, name))
        zf = zipfile.ZipFile(zip_path, "w", zipfile.zlib.DEFLATED)
        for tar in file_list:
            arcname = tar[len(report_path):]
            zf.write(tar, arcname)
        zf.extractall(report_path)
        zf.close()
        send_rar = open(zip_path, 'rb').read()
        # # 邮件内容
        msg = MIMEMultipart('mixed')
        # # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr(["sunkai", sender])
        # # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = receivers
        # # 邮件的主题
        msg['Subject'] = "App自动化测试报告"
        start = datetime.datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S.%f')
        end = datetime.datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S.%f')
        long = str(end_time - start_time)
        email_content = """
            <table class="tg" border="5" width="95%" cellpadding="10%" align="center">
        <tr>
            <th class="tg-0pky" colspan="2" align="center">APP自动化测试报告总览</th>
        </tr>
        <tr>
            <td class="tg-pky" width="30%" align="center">开始时间：</td>
            <td class="tg-2pky" align="center">{}</td>
        </tr>
        <tr>
            <td class="tg-1pky" width="30%" align="center">结束时间：</td>
            <td class="tg-3pky" align="center">{}</td>
        </tr>
        <tr>
            <td class="tg-4pky" width="30%" align="center">持续时间：</td>
            <td class="tg-5pky" align="center">{}</td>
        </tr>
        <tr>
            <td class="tg-6pky" width="30%" align="center">执行结果：</td>
            <td class="tg-7pky" align="center">通过：{}失败：{}错误：{}</td>
        </tr>
    </table>
            """.format(start, end, long, str(pass_num), str(failed_num), str(error_num))
        texthtml = MIMEText(email_content, 'html', 'utf-8')
        # # 将 alternative 加入 mixed 的内部
        msg.attach(texthtml)
        # # 附件内容
        att = MIMEText(send_rar, 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename=report.zip'
        msg.attach(att)
        # # SMTP服务器，腾讯企业邮箱端口是465，腾讯邮箱支持SSL(不强制)， 不支持TLS
        # # qq邮箱smtp服务器地址:smtp.qq.com,端口号：456
        # # 163邮箱smtp服务器地址：smtp.163.com，端口号：25
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        # # 登录服务器，括号中对应的是发件人邮箱账号、邮箱密码
        server.login(sender, password)
        # # 发送邮件，括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(sender, rec_list, msg.as_string())
        # # 关闭连接
        server.quit()
    except Exception as msg:
        print(msg)


if __name__ == '__main__':
    a = datetime.datetime.now()
    time.sleep(3)
    b = datetime.datetime.now()
    sendmail('/Users/sunkai/word_download/android-auto/report/HTML/2020-02-21', a, b, 233, 4, 45)
