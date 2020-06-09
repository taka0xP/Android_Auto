from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
from common.CreditIdentifier import UnifiedSocialCreditIdentifier

import re
import time
import random

log = Logger("公司详情页-事业单位详情页").getlog()

class Public_institution_detail_page(MyTest, Operation):
    """公司详情页-事业单位详情页"""

    def search_result(self, company, index=0):
        """进入关键词搜索结果列表第一家公司详情页"""
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/txt_search_copy1').click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/search_input_et').send_keys(company)
        self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name']")[index].click()

    def check_date(self, str):
        """判断日期字符串格式是否为YYYY-MM-DD"""
        try:
            time.strptime(str,"%Y-%m-%d")
            return True
        except:
            return False

    def check_date1(self, str):
        """判断日期字符串格式是否为YYYY.MM.DD"""
        try:
            time.strptime(str,"%Y.%m.%d")
            return True
        except:
            return False

    def go_back(self):
        self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_back').click()

    def title_name(self):
        title_text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_name').text
        return title_text

    @getimage
    def test_GSXQY_SYDW_0001(self):
        '''公司详情页-事业单位详情页头部信息'''
        log.info(self.test_GSXQY_SYDW_0001.__doc__)
        company_list = ['河源市河源中学','江门市新会区国有资产管理办公室','佛山市禅城区公有资产管理办公室','临泉县供销合作社联合社','武汉大学']
        company_name = company_list[random.randint(0,len(company_list)-1)]
        log.info(company_name)
        self.search_result(company_name)

        fieldname_list = ['法定代表人', '开办资金', '成立日期']#事业单位头部信息展示字段

        #校验事业单位头部信息字段名称
        sub_01 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_title_1').text
        sub_02 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_title_2').text
        sub_03 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_title_3').text
        self.assertEqual(sub_01, '法定代表人', msg='错误——%s' % fieldname_list[0])
        self.assertEqual(sub_02, '开办资金', msg='错误——%s' % fieldname_list[1])
        self.assertEqual(sub_03, '成立日期', msg='错误——%s' % fieldname_list[2])

        #进入工商信息取法定代表人名称、开办资金
        count = 1
        while True:
            if not self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='工商信息']"):
                if count <= 3:
                    self.swipeUp(x1=0.5, y1=0.60, y2=0.40)
                    count += 1
                else:
                    log.error("未找到工商信息")
            else:
                break
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='工商信息']").click()
        # 法定代表人
        person = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_detail_legal_content').text
        log.info('工商信息法定代表人为：%s'%person)
        # 开办资金
        capital = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/institution_reg_capital_tv').text
        log.info('工商信息开办资金为：%s'%capital)
        self.go_back()#返回详情页
        self.swipeDown(x1=0.5, y1=0.40, y2=0.60)#下拉页面

        #1法定代表人 校验单位校验与工商信息中是否相同
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_value_1').text
        log.info('法定代表人为：%s' % text_01)
        self.assertEqual(text_01,person,msg='法定代表人与工商信息中不同')

        #2开办资金 校验与工商信息中是否相同
        text_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_value_2').text
        log.info('开办资金为：%s' % text_02)
        self.assertEqual(text_02,capital,msg='开办资金与工商信息中不同')

        #3成立日期 校验日期格式为YYYY.MM.DD
        text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_value_3').text
        log.info('成立日期为：%s'%text_03)
        if text_03 != '-':
            result_03 = self.check_date1(text_03)
            self.assertTrue(result_03,msg='日期格式有误')
        else:
            log.info('成立日期为空')

    @getimage
    def test_GSXQY_SYDW_0002(self):
        '''事业单位-工商信息'''
        log.info(self.test_GSXQY_SYDW_0002.__doc__)
        company_list = ['河源市河源中学','江门市新会区国有资产管理办公室','佛山市禅城区公有资产管理办公室',
                        '临泉县供销合作社联合社','武汉大学','北京市统计局统计执法检查大队',
                        '北京市海淀区综合训练馆','上海市新闻出版局老干部活动室']
        company_name = company_list[random.randint(0,len(company_list)-1)]
        log.info(company_name)
        self.search_result(company_name)

        count = 1
        while True:
            if not self.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='工商信息']"):
                if count <= 3:
                    self.swipeUp(x1=0.5, y1=0.60, y2=0.40)
                    count += 1
                else:
                    log.error("未找到工商信息")
            else:
                break

        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='工商信息']").click()

        fieldname_list = ['法定代表人', '开办资金', '登记状态','原证书号','统一社会信用代码','有效期','经费来源','登记管理机关','举办单位','住所','宗旨和业务范围']
        for i in range(len(fieldname_list)):
            result = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i])
            log.info(fieldname_list[i])
            count = 1
            while True:
                if not self.new_find_element(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i]):
                    if count <= 3:
                        self.swipeUp(x1=0.5, y1=0.60, y2=0.40, t=500)
                        count += 1
                    else:
                        log.error("错误———未找到%s"%fieldname_list[i])
                        self.assertTrue(result,msg="错误———未找到%s"%fieldname_list[i])
                else:
                    break

        #1法定代表人：校验字符大于1
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_detail_legal_content').text
        log.info('校验法定代表人：%s'%text_01)
        if text_01 != '':
            if len(text_01)>1:
                result_01 = True
            else:
                result_01 = False
            self.assertTrue(result_01,msg='错误——%s'%fieldname_list[0])
        else:
            log.info('%s为空'%fieldname_list[0])

        #2开办资金：校验单位
        text_02 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/institution_reg_capital_tv').text
        units_list = ['万','万元']
        log.info('校验开办资金：%s' % text_02)
        if text_02 != '':
            unit = ''.join(re.findall('[\u4e00-\u9fa5]', text_02))
            self.assertIn(unit,units_list,msg='错误——%s' % fieldname_list[1])
        else:
            log.info('%s为空' % fieldname_list[1])

        #3登记状态：校验in status_list
        status_list = ['其他','正常','注销']
        text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/institution_reg_status_tv').text
        log.info('校验登记状态：%s' % text_03)
        if text_03 != '-':
            self.assertIn(text_03,status_list,msg='错误——%s' % fieldname_list[2])
        else:
            log.info('%s为空'%fieldname_list[2])

        #4原证书号：校验长度为16，格式为'事证第xxxxxxxxxxxx号'
        text_04 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/institution_old_cert_tv').text
        log.info('校验原证书号：%s'%text_04)
        if text_04 != '-':
            word = ''.join(re.findall('[\u4e00-\u9fa5]', text_04))
            self.assertEqual(word,'事证第号',msg='错误——%s' % fieldname_list[3])
        else:
            log.info('%s为空' % fieldname_list[3])

        #5统一社会信用代码：方法判断
        text_05 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/institution_us_credit_code_tv').text
        log.info('校验统一社会信用代码：%s' % text_05)
        u = UnifiedSocialCreditIdentifier()
        result_05 = u.check_social_credit_code(text_05)
        self.assertTrue(result_05,msg='错误——%s' % fieldname_list[4])



