from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.CreditIdentifier import UnifiedSocialCreditIdentifier
from common.ReadData import Read_Ex
from Providers.logger import Logger
import re
import time
import random
from selenium.webdriver.support import expected_conditions as EC

#非vip——110-9999-5055

log = Logger("公司详情页-律所详情页").getlog()

class Law_office_detail_page(MyTest, Operation):
    """公司详情页-律所详情页"""

    def search_result(self, company, index=0):
        """进入关键词搜索结果列表第一家公司详情页"""
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/txt_search_copy1').click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/search_input_et').send_keys(company)
        self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name']")[index].click()

    def go_back(self):
        """页面返回"""
        self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_back').click()

    def title_name(self):
        """获取页面名称"""
        title_text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_name').text
        return title_text

    def login_page_check(self,way,element):
        '''判断是否在登录页面'''
        if way == 1:
            self.new_find_element(By.ID,element).click()
        elif way == 2:
            self.new_find_element(By.XPATH,element).click()
        result = self.isElementExist(By.ID,"com.tianyancha.skyeye:id/btv_title")
        text = self.new_find_element(By.ID,"com.tianyancha.skyeye:id/btv_title").text
        if text == '短信验证码登录':
            log.info('当前在短信验证码登录页面')
        elif text == '密码登录':
            log.info('当前在密码登录页面')
        return result

    def touch_tap(self, x, y, duration=100):  # 点击坐标  ,x1,x2,y1,y2,duration
        '''
        method explain:点击坐标
        parameter explain：【x,y】坐标值,【duration】:给的值决定了点击的速度
        Usage:
            device.touch_coordinate(277,431)      #277.431为点击某个元素的x与y值
        '''
        screen_width = self.driver.get_window_size()['width']  # 获取当前屏幕的宽
        screen_height = self.driver.get_window_size()['height']  # 获取当前屏幕的高
        a = (float(x) / screen_width) * screen_width
        x1 = int(a)
        b = (float(y) / screen_height) * screen_height
        y1 = int(b)
        self.driver.tap([(x1, y1), (x1, y1)], duration)

    def dimensionality(self):
        """律所详情页·企业背景-维度"""
        dimensionality_list = ["//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='登记信息']",
                               "//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='律师团队']",
                               "//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='代理客户']",
                               "//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='代理案件']",
                               "//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='对外投资']"]
        return dimensionality_list

    def check_personname(self,str):
        """校验人名称"""
        if len(str) > 1:
            return True
        else:
            return False

    def check_dates(self,str):
        """判断日期字符串格式是否为YYYY-MM-DD HH:MM:SS.0"""
        try:
            time.strptime(str,"%Y-%m-%d %H:%M:%S.0")
            return True
        except:
            return False

    def check_date(self, str):
        """判断日期字符串格式是否为YYYY-MM-DD"""
        try:
            time.strptime(str,"%Y-%m-%d")
            return True
        except:
            return False

    def check_chinese(self,check_str):
        """判断字符串中是否包含中文"""
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def check_num(self,str):
        '''校验字符串中是否只包含数字'''
        result = str.isdigit()
        return result

    @getimage
    def test_GSXQY_LS_0001(self):
        '''公司详情页-律所详情页01'''
        log.info(self.test_GSXQY_LS_0001.__doc__)
        company_list =['黑龙江太平洋律师事务所','浙江海宝律师事务所','重庆睿渝律师事务所','贵州贵达律师事务所']
        company_name = company_list[random.randint(0,len(company_list)-1)]
        self.search_result(company_name,0)

        goal_01 = ['律所头部信息展示负责人','注册资本','成立日期']
        log.info(goal_01)
        text_01_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_title_1').text
        text_01_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_title_2').text
        text_01_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_title_3').text
        self.assertEqual(text_01_01,'负责人',msg='错误——%s'%goal_01[0])
        self.assertEqual(text_01_02,'注册资本',msg='错误——%s'%goal_01[1])
        self.assertEqual(text_01_03,'成立日期',msg='错误——%s'%goal_01[2])

        goal_02 = ['企业背景包含维度「登记信息」','「律师团队」','「代理客户」','「代理案件」','「对外投资」']
        log.info(goal_02)
        result_02_01 = self.isElementExist(By.XPATH,self.dimensionality()[0])
        result_02_02 = self.isElementExist(By.XPATH,self.dimensionality()[1])
        result_02_03 = self.isElementExist(By.XPATH,self.dimensionality()[2])
        result_02_04 = self.isElementExist(By.XPATH,self.dimensionality()[3])
        result_02_05 = self.isElementExist(By.XPATH,self.dimensionality()[4])
        self.assertTrue(result_02_01,msg='错误——%s'%goal_02[0])
        self.assertTrue(result_02_02,msg='错误——%s'%goal_02[1])
        self.assertTrue(result_02_03,msg='错误——%s'%goal_02[2])
        self.assertTrue(result_02_04,msg='错误——%s'%goal_02[3])
        self.assertTrue(result_02_05,msg='错误——%s'%goal_02[4])

        goal_03 = '点击「登记信息」进入「登记信息」详情页'
        log.info(goal_03)
        self.new_find_element(By.XPATH,self.dimensionality()[0]).click()
        text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/item_expandable_group_title').text
        self.assertEqual(text_03, '登记信息', msg='错误——%s' % goal_03)
        self.go_back()

        goal_04 = '点击「律师团队」进入「律师团队」详情页'
        self.new_find_element(By.XPATH,self.dimensionality()[1]).click()
        test_04 = self.title_name()
        self.assertEqual(test_04,'律师团队',msg='错误——%s'%goal_04)
        self.go_back()

        goal_05 = '点击「代理客户」进入「代理客户」详情页'
        self.new_find_element(By.XPATH,self.dimensionality()[2]).click()
        test_05 = self.title_name()
        self.assertEqual(test_05,'代理客户',msg='错误——%s' % goal_05)
        self.go_back()

        goal_06 = '点击「代理案件」进入「代理案件」详情页'
        self.new_find_element(By.XPATH,self.dimensionality()[3]).click()
        test_06 = self.title_name()
        self.assertEqual(test_06,'代理案件',msg='错误——%s' % goal_06)

    @getimage
    def test_GSXQY_LS_0002(self):
        '''公司详情页-律所详情页02'''
        log.info(self.test_GSXQY_LS_0002.__doc__)
        company_name = '北京市中伦律师事务所'
        self.search_result(company_name, 0)

        goal = '点击「对外投资」进入「对外投资」详情页'
        count = 0
        while True:
            if not self.new_find_element(By.XPATH,self.dimensionality()[4]):
                if count <= 5:
                    self.swipeUp(x1=0.5, y1=0.50, y2=0.40,t=500)
                    count += 1
                else:
                    log.error("错误——未找到对外投资")
                    break
            else:
                break
        self.new_find_element(By.XPATH,self.dimensionality()[4]).click()
        text = self.title_name()
        self.assertEqual(text, '对外投资', msg='错误——%s' % goal)

    @getimage
    def test_GSXQY_LS_0003(self):
        '''律所详情页-登记信息校验字段名称'''
        log.info(self.test_GSXQY_LS_0003.__doc__)
        company_name = '广东法导律师事务所'
        fieldname_list = ['律所负责人','成立日期','执业状态','注册资本','统一社会信用代码','工商注册号','组织机构代码','税务登记号','信用等级',
                          '组织形式','主管机关','营业期限','总所/分所','律所人数','执业许可证号','发证日期','批准日期','地址','电话','业务特长',
                          '律所简介']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[0]).click()
        for i in range(len(fieldname_list)):
            result_01 = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i])
            log.info(fieldname_list[i])
            count = 1
            while True:
                if not self.new_find_element(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i]):
                    if count <= 3:
                        self.swipeUp(x1=0.5, y1=0.60, y2=0.40, t=500)
                        count += 1
                    else:
                        log.error("错误———未找到%s"%fieldname_list[i])
                        self.assertTrue(result_01,msg="错误———未找到%s"%fieldname_list[i])
                else:
                    break

    @getimage
    def test_GSXQY_LS_0004(self):
        '''律所详情页-登记信息校验字段内容'''
        log.info(self.test_GSXQY_LS_0004.__doc__)
        company_list = ['河北朗科律师事务所','北京卓孚律师事务所','北京京飞律师事务所','北京也迪律师事务所','广东瀚诚律师事务所']
        company_name = company_list[random.randint(0,len(company_list)-1)]
        #字段名称列表
        fieldname_list = ['律所负责人','成立日期','执业状态','注册资本','统一社会信用代码','工商注册号','组织机构代码','税务登记号','信用等级',
                          '组织形式','主管机关','营业期限','总所/分所','律所人数','执业许可证号','发证日期','批准日期','地址','电话','业务特长',
                          '律所简介']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[0]).click()

        #1律所负责人：校验人名称是否大于1个字符
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_legal_tv').text
        log.info('校验律所负责人:%s'%text_01)
        if text_01 != '-':
            if len(text_01)>1:
                result_01 = True
            else:
                result_01 = False
            self.assertTrue(result_01,msg="错误——%s"%fieldname_list[0])
        else:
            log.info("%s为空"%fieldname_list[0])

        #2成立日期：校验日期格式是否为YYYY-MM-DD
        test_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_time_tv').text
        log.info('校验成立日期:%s'%test_02)
        if test_02 != '-':
            result_02 = self.check_date(test_02)
            self.assertTrue(result_02,msg="错误——%s"%fieldname_list[1])
        else:
            log.info("%s为空"%fieldname_list[1])

        #3执业状态：校验执业状态in status_list
        status_list = ['正常','其他','吊销','未年检','未经年度考核','正常执业','注销','设立中','-']
        text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_org_num').text
        log.info('校验执业状态:%s'%text_03)
        if text_03 != '-':
            if text_03 in status_list:
                result_03 = True
            else:
                result_03 = False
            self.assertTrue(result_03,msg="错误——%s"%fieldname_list[2])
        else:
            log.info("%s为空" % fieldname_list[2])

        #4注册资本：校验人民币单位in units_list
        units_list = ['万','人民币','万人民币','-']
        str_04 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_reg_capital').text
        log.info('校验注册资本:%s'%str_04)
        if str_04 != '-':
            text_04 = ''.join(re.findall('[\u4e00-\u9fa5]',str_04))
            log.info(text_04)
            if text_04 in units_list:
                result_04 = True
            else:
                result_04 = False
            self.assertTrue(result_04, msg="错误——%s"%fieldname_list[3])
        else:
            log.info("%s为空"%fieldname_list[3])

        #5统一社会信用代码：校验长度为18位或10位或为空
        text_05 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_credit_num').text
        log.info('校验统一社会信用代码:%s'%text_05)
        log.info(len(text_05))
        if len(text_05) == 18 or len(text_05) == 10 or text_05 == '-':
            if text_05 == '-':
                log.info("%s为空"%fieldname_list[4])
            result_05 = True
        else:
            result_05 = False
        self.assertTrue(result_05,msg="错误——%s"%fieldname_list[4])

        #6工商注册号：库里无数据全部展示为"-"
        text_06 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_regist_no').text
        log.info('校验工商注册号:%s'%text_06)
        if text_06 == '-':
            log.info("%s为空"%fieldname_list[5])
            result_06 = True
        else:
            result_06 = False
        self.assertTrue(result_06,msg="错误——%s"%fieldname_list[5])

        #7组织机构代码：库里无数据全部展示为"-"
        text_07 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_organization_code').text
        log.info('校验组织机构代码:%s'%text_07)
        if text_07 == '-':
            log.info("%s为空" % fieldname_list[6])
            result_07 = True
        else:
            result_07 = False
        self.assertTrue(result_07, msg="错误——%s"%fieldname_list[6])

        #8税务登记号：校验不包含汉字
        text_08 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/law_office_organization_code').text
        log.info('校验税务登记号:%s'%text_08)
        if text_08 == '-':
            log.info("%s为空" % fieldname_list[7])
        result_08 = self.check_chinese(text_08)
        self.assertFalse(result_08,msg="错误——%s"%fieldname_list[7])

        #9信用等级：校验in grade_list
        grade_list = ['A','AA','AAA','AAA级','A级','B级','一级','二级','优','优秀','合格','良好','诚实信用','-']
        text_09 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_credit_grade').text
        log.info('校验信用等级:%s'%text_09)
        if text_09 in grade_list:
            if text_09 == '-':
                log.info("%s为空" % fieldname_list[8])
            result_09 = True
        else:
            result_09 = False
        self.assertTrue(result_09,msg="错误——%s"%fieldname_list[8])

        #10组织形式 无规则，判断无数据时用"-"展示
        text_10 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_org_shape').text
        log.info('校验组织形式:%s'%text_10)
        if text_10 != '':
            if text_10 == '-':
                log.info("%s为空" % fieldname_list[9])
            result_10 = True
        else:
            result_10 = False
        self.assertTrue(result_10,msg="错误——%s"%fieldname_list[9])

        #11主管机关：校验不包含数字
        text_11 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_com_organ').text
        log.info('校验主管机关:%s'%text_11)
        result_11 = self.check_num(text_11)
        self.assertFalse(result_11,msg="错误——%s"%fieldname_list[10])

        #12营业期限：校验全部展示为"-"（律所无营业执照无营业期限）
        text_12 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_operating_period').text
        log.info('校验营业期限:%s'%text_12)
        if text_12 == '-':
            log.info("%s为空"%fieldname_list[11])
            result_12 = True
        else:
            result_12 = False
        self.assertTrue(result_12,msg="错误——%s"%fieldname_list[11])

        #13总所/分所：校验in status_list
        level_list = ['分所','总所','-']
        text_13 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_all_substation').text
        log.info('校验总所/分所:%s'%text_13)
        if text_13 in  level_list:
            if text_13 == '-':
                log.info("%s为空"%fieldname_list[12])
            result_13 = True
        else:
            result_13 = False
        self.assertTrue(result_13,msg="错误——%s" % fieldname_list[12])

        #14律所人数：校验是否为数字
        text_14 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_person_count').text
        log.info('校验律所人数:%s'%text_14)
        result_14 = self.check_num(text_14)
        self.assertTrue(result_14,msg="错误——%s" % fieldname_list[13])

        self.swipeUp(x1=0.5, y1=0.80, y2=0.30, t=500)

        #15执业许可证号：校验是否为数字
        text_15 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_lic_num').text
        log.info('校验执业许可证号:%s'%text_15)
        if text_15 != '-':
            result_15 = self.check_num(text_15)
            self.assertTrue(result_15,msg="错误——%s"%fieldname_list[14])
        else:
            log.info("%s为空"%fieldname_list[14])

        #16发证日期：校验日期格式
        text_16 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_certificate_data').text
        log.info('校验发证日期:%s'%text_16)
        result_16_01 = self.check_date(text_16)
        result_16_02 = self.check_dates(text_16)
        if text_16 != '-':
            if result_16_01 == True:
                log.info('格式为YYYY-MM-DD')
                result_16 = True
            elif result_16_02 == True:
                result_16 = True
                log.info('格式为YYYY-MM-DD HH:MM:SS.0')
            else:
                result_16 = False
            self.assertTrue(result_16,msg="错误——%s"%fieldname_list[15])
        else:
            log.info("%s为空"%fieldname_list[15])

        #17批准日期：校验日期格式
        text_17 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_business_data').text
        log.info('校验批准日期:%s'%text_17)
        if text_17 != '-':
            result_17 = self.check_date(text_17)
            self.assertTrue(result_17,msg="错误——%s"%fieldname_list[16])
        else:
            log.info("%s为空"%fieldname_list[16])

        #18地址：校验是否可点击、点击后跳转到「公司地图」页面
        text_18_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_address').text
        log.info('校验地址:%s'%text_18_01)
        if text_18_01 != '-':
            result_18 = self.new_find_element(By.ID,"com.tianyancha.skyeye:id/law_office_address").is_enabled()
            if result_18 == True:
                self.new_find_element(By.ID, "com.tianyancha.skyeye:id/law_office_address").click()
                text_18_02 = self.title_name()
                self.assertEqual(text_18_02,'公司地图',msg='错误——跳转到「公司地图」页面')
                self.go_back()
            self.assertTrue(result_18,msg="地址不可点")
        else:
            log.info("%s为空"%fieldname_list[17])

        #19电话：校验是否可点击 是否只包含数字
        text_19 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_phone').text
        log.info('校验电话:%s'%text_19)
        if text_19 != '-':
            result_19_01 = self.new_find_element(By.ID,"com.tianyancha.skyeye:id/law_office_phone").is_enabled()
            if result_19_01 == True:
                num_01 = text_19.replace('-','')
                num_02 = num_01.replace(' ','')
                log.info(num_02)
                result_19_02 = self.check_num(num_02)
                self.assertTrue(result_19_02,msg="错误——%s"%fieldname_list[18])
            self.assertTrue(result_19_01,msg='电话不可点')
        else:
            log.info("%s为空"%fieldname_list[18])

        #20业务特长：校验不为空时字符大于1
        text_20 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_business_point').text
        log.info('校验业务特长:%s'%text_20)
        if text_20 != '-':
            if len(text_20)>1:
                result_20 = True
            else:
                result_20 = False
            self.assertTrue(result_20,msg="错误——%s"%fieldname_list[19])
        else:
            log.info("%s为空"%fieldname_list[19])

        #21律所简介：校验不为空时字符大于1
        text_21 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/law_office_briefing').text
        log.info('校验律所简介:%s' % text_21)
        if text_21 != '-':
            if len(text_21) > 1:
                result_21 = True
            else:
                result_21 = False
            self.assertTrue(result_21, msg="错误——%s" % fieldname_list[20])
        else:
            log.info("%s为空" % fieldname_list[20])

    @getimage
    def test_GSXQY_LS_0005(self):
        '''律所详情页-律师团队校验字段名称'''
        log.info(self.test_GSXQY_LS_0005.__doc__)
        company_list = ['张利民律师事务所', '贵州证道律师事务所', '湖南律畅律师事务所', '爱德律师事务所', '恒信长城律师事务所']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        #字段名称列表
        fieldname_list = ['执业机构','执业证号','执业年限','专长']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[1]).click()

        for i in range(len(fieldname_list)):
            result_01 = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i])
            log.info(fieldname_list[i])
            count = 1
            while True:
                if not self.new_find_element(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i]):
                    if count <= 3:
                        self.swipeUp(x1=0.5, y1=0.80, y2=0.30, t=500)
                        count += 1
                    else:
                        log.error("错误———未找到%s"%fieldname_list[i])
                        self.assertTrue(result_01,msg="错误———未找到%s"%fieldname_list[i])
                else:
                    break

    @getimage
    def test_GSXQY_LS_0006(self):
        '''律所详情页-律师团队校验字段内容'''
        log.info(self.test_GSXQY_LS_0006.__doc__)
        company_list = ['张利民律师事务所','贵州证道律师事务所','湖南律畅律师事务所','爱德律师事务所','恒信长城律师事务所']
        company_name = company_list[random.randint(0,len(company_list)-1)]
        #字段名称列表
        fieldname_list = ['执业机构','执业证号','执业年限','专长']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[1]).click()

        #1执业机构：校验是否和公司名称相等
        text_01 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_content_1']").text
        log.info('校验执业机构:%s'%text_01)
        self.assertEqual(text_01,company_name,msg="错误——%s" % fieldname_list[0])

        #2执业证号：校验不为空是是否纯数字及是否为17位
        text_02 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_content_2']").text
        log.info('校验执业证号:%s'%text_02)
        if text_02 != '-':
            result_02_01 = self.check_num(text_02)
            if result_02_01 == True:
                if len(text_02) == 17:
                    log.info(len(text_02))
                    result_02_02 = True
                else:
                    result_02_02 = False
                self.assertTrue(result_02_02,msg='错误——执业证号为17位')
            else:
                self.assertTrue(result_02_01,msg='错误——执业证号只包含数字')
        else:
            log.info("%s为空" % fieldname_list[1])

        #3执业年限：校验只包含数字
        text_03 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_content_3']").text
        log.info('校验执业年限:%s'%text_03)
        if text_03 != '-':
            result_03 = self.check_num(text_03)
            self.assertTrue(result_03,msg='错误——执业年限只包含数字')
        else:
            log.info("%s为空" % fieldname_list[2])

        #4专长：校验字数大于1（库里只有五条有数据）
        text_04 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_content_4']").text
        log.info('校验专长:%s'%text_04)
        if text_04 != '-':
            if len(text_04)>1:
                result_04 = True
            else:
                result_04 = False
            self.assertTrue(result_04,msg="错误——%s"%fieldname_list[3])
        else:
            log.info("%s为空" % fieldname_list[3])

    @getimage
    def test_GSXQY_LS_0007(self):
        '''律所详情页-代理客户校验字段名称'''
        log.info(self.test_GSXQY_LS_0007.__doc__)
        company_list = ['青海竞帆律师事务所', '重庆睿渝律师事务所', '重庆金雷律师事务所', '海南卫伦律师事务所', '海南林源律师事务所']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        #字段名称列表
        fieldname_list = ['客户名称：','客户法定代表人：','注册资本：','成立日期：','经营状态：']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[2]).click()

        for i in range(len(fieldname_list)):
            result_01 = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i])
            log.info(fieldname_list[i])
            count = 1
            while True:
                if not self.new_find_element(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i]):
                    if count <= 3:
                        self.swipeUp(x1=0.5, y1=0.80, y2=0.30, t=500)
                        count += 1
                    else:
                        log.error("错误———未找到%s"%fieldname_list[i])
                        self.assertTrue(result_01,msg="错误———未找到%s"%fieldname_list[i])
                else:
                    break

    @getimage
    def test_GSXQY_LS_0008(self):
        '''律所详情页-代理客户校验字段内容'''
        log.info(self.test_GSXQY_LS_0008.__doc__)
        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login(11099995055, "ef08beca")
        company_list = ['青海竞帆律师事务所', '重庆睿渝律师事务所', '重庆金雷律师事务所', '海南卫伦律师事务所', '海南林源律师事务所']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        #字段名称列表
        fieldname_list = ['客户名称：','客户法定代表人：','注册资本：','成立日期：','经营状态：']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[2]).click()

        #1客户名称：校验字符大于4、不为空时是否可点击、点击进入对应公司详情页
        text_01_01 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content1']").text
        log.info('校验客户名称:%s'%text_01_01)
        if text_01_01 != '-':
            if len(text_01_01) > 4:
                result_01_01 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content1']").is_enabled()
                self.assertTrue(result_01_01,msg="客户名称不可点")
                self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content1']").click()
                text_01_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/firm_detail_name_tv').text
                self.assertEqual(text_01_02,text_01_01,msg='客户名称与进入的公司详情页名称不相等')
            else:
                log.error('客户名称小于四个字')
        else:
            log.info("%s为空" % fieldname_list[0])
        self.go_back()

        #进入公司详情页拿到法人、注册资本、成立日期、经营状态
        self.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content1']").click()
        # 法定代表人
        person_name = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_value_1').text
        # 注册资本
        money = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_value_2').text
        # 成立日期
        date = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_value_3').text
        # 经营状态
        status = self.new_find_element(By.XPATH,'//android.view.ViewGroup/android.widget.LinearLayout/android.widget.TextView[1]').text
        self.go_back()

        #2客户法定代表人:校验是否与对应公司详情页法人相等、校验不为空时可点击、点击进入对应人员/公司详情页
        text_02_01 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content2']").text
        log.info("校验客户法定代表人：%s"%text_02_01)
        self.assertEqual(text_02_01,person_name,msg='法定代表人与对应公司详情页法定代表人不相等')
        if text_02_01 == person_name:
            if text_02_01 != '-':
                result_02_01 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content2']").is_enabled()
                self.assertTrue(result_02_01,msg='客户法定代表人不可点')
                self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content2']").click()
                consequence = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/radio_person_detail')
                if consequence == True:
                    text_02_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/person_name_tv').text
                    self.assertEqual(text_02_02,text_02_01,msg='客户法定代表人人员名称与进入的人员详情页名称不相等')
                else:
                    text_02_03 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/firm_detail_name_tv').text
                    self.assertEqual(text_02_03, text_02_01, msg='客户法定代表人公司名称与进入的公司详情页名称不相等')
            else:
                log.info("%s为空" % fieldname_list[1])
        self.go_back()

        #3注册资本:校验是否与对应公司详情页注册资本相等
        text_03 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content3']").text
        log.info('校验注册资本：%s'%text_03)
        self.assertEqual(text_03,money,msg='注册资本与对应公司详情页注册资本不相等')

        #4成立日期:校验是否与对应公司详情页成立日期相等、校验日期格式
        text_04 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content4']").text
        log.info('校验成立日期：%s'%text_04)
        if text_04 != '-':
            result_04 = self.check_date(text_04)
            self.assertTrue(result_04,msg='成立日期格式错误')
            num_01 = re.sub("\D", "", text_04)
            num_02 = re.sub("\D", "", date)
            self.assertEqual(num_01,num_02,msg='成立日期与对应公司详情页成立日期不相等')
        else:
            log.info("%s为空" % fieldname_list[3])

        #5经营状态：校验是否与对应公司详情页成立日期相等
        text_05 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content5']").text
        log.info('校验经营状态:%s'%text_05)
        self.assertEqual(text_05,status,msg='经营状态与对应公司详情页经营状态不相等')

        goal_01 = '点击整条item进入案件列表详情页'
        self.new_find_element(By.XPATH,"//androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]").click()
        text_06 = self.title_name()
        self.assertEqual(text_06,'案件列表',msg='错误——%s'%goal_01)

        goal_02 = '点击整条item进入法律诉讼详情页'
        self.new_find_element(By.XPATH,"//androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]").click()
        time.sleep(0.5)
        text_07 = self.title_name()
        self.assertEqual(text_07,'法律诉讼详情',msg='错误——%s'%goal_02)

        time.sleep(1)
        self.logout()

    @getimage
    def test_GSXQY_LS_0009(self):
        '''律所详情页-代理案件校验字段名称'''
        log.info(self.test_GSXQY_LS_0009.__doc__)
        company_list = ['青海竞帆律师事务所', '重庆睿渝律师事务所', '重庆金雷律师事务所', '海南卫伦律师事务所', '海南林源律师事务所']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        #字段名称列表
        fieldname_list = ['判决案号：','发布日期：','案件类型：']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[3]).click()

        for i in range(len(fieldname_list)):
            result_01 = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i])
            log.info(fieldname_list[i])
            count = 1
            while True:
                if not self.new_find_element(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i]):
                    if count <= 3:
                        self.swipeUp(x1=0.5, y1=0.80, y2=0.30, t=500)
                        count += 1
                    else:
                        log.error("错误———未找到%s"%fieldname_list[i])
                        self.assertTrue(result_01,msg="错误———未找到%s"%fieldname_list[i])
                else:
                    break

    @getimage
    def test_GSXQY_LS_0010(self):
        '''律所详情页-代理案件校验字段内容'''
        log.info(self.test_GSXQY_LS_0010.__doc__)
        company_list = ['青海竞帆律师事务所', '重庆睿渝律师事务所', '重庆金雷律师事务所', '海南卫伦律师事务所', '海南林源律师事务所']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        #字段名称列表
        fieldname_list = ['判决案号：','发布日期：','案件类型：']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[3]).click()

        goal_01 = '点击案件整条item跳转法律诉讼详情页'
        self.new_find_element(By.XPATH,
                              "//androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]").click()
        text = self.title_name()
        self.assertEqual(text,'法律诉讼详情',msg='错误——%s'%goal_01)

        #获取日期
        date = self.new_find_element(By.XPATH,"//android.view.View[@text='来源：']/following-sibling::android.view.View[3]").text
        #获取案号
        num = self.new_find_element(By.XPATH,"//android.view.View[@text='案号']/following-sibling::android.view.View[1]").text
        self.go_back()

        #1判决案号:校验与诉讼详情页案号是否相等
        text_01 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content1']").text
        log.info('校验判决案号：%s'%text_01)
        self.assertEqual(text_01,num,msg="错误——%s"%fieldname_list[0])

        #2发布日期：校验与诉讼详情页日期是否相等
        text_02 = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content2']").text
        log.info('校验发布日期：%s'%text_02)
        self.assertEqual(text_02,date,msg="错误——%s"%fieldname_list[1])

        #3案件类型：校验in type_list
        type_list = ['刑事案件','民事案件','行政案件','赔偿案件','其他案件']
        text_03 = self.ocr(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/tv_item_content3']")
        log.info('校验案件类型：%s'%text_03)
        self.assertIn(text_03,type_list,msg="错误——%s"%fieldname_list[2])

    @getimage
    def test_GSXQY_LS_0011(self):
        '''律所详情页-对外投资校验字段名称'''
        log.info(self.test_GSXQY_LS_0011.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()

        company_list = ['浙江商瑞律师事务所', '北京市中伦律师事务所']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        #字段名称列表
        fieldname_list = ['法定代表人','经营状态','投资数额','投资比例','成立日期']
        self.search_result(company_name, 0)
        self.new_find_element(By.XPATH,self.dimensionality()[4]).click()

        #LOGO
        element_01 = self.isElementExist(By.XPATH,"//android.widget.RelativeLayout/android.widget.FrameLayout")
        self.assertTrue(element_01,msg='无logo')

        #公司名称
        element_02 = self.isElementExist(By.ID,'com.tianyancha.skyeye:id/outinvest_company_name_tv')
        self.assertTrue(element_02,msg='无公司名称')

        #股权结构入口
        element_03 = self.isElementExist(By.ID,"com.tianyancha.skyeye:id/tv_outinvest_title_right")
        self.assertTrue(element_03,msg='无股权结构入口')

        for i in range(len(fieldname_list)):
            result = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i])
            log.info(fieldname_list[i])
            count = 1
            while True:
                if not self.new_find_element(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i]):
                    if count <= 3:
                        self.swipeUp(x1=0.5, y1=0.80, y2=0.30, t=500)
                        count += 1
                    else:
                        log.error("错误———未找到%s"%fieldname_list[i])
                        self.assertTrue(result,msg="错误———未找到%s"%fieldname_list[i])
                else:
                    break

        goal_01 = '未登录点击股权结构跳转登陆页'
        result_01 = self.login_page_check(1,'com.tianyancha.skyeye:id/tv_outinvest_title_right')
        self.assertTrue(result_01,msg='错误——%s'%goal_01)
        self.go_back()

        goal_02 = '未登录点击法定代表人跳转登陆页'
        result_02 = self.login_page_check(1,'com.tianyancha.skyeye:id/outinvest_legal_tv')
        self.assertTrue(result_02,msg='错误——%s'%goal_02)

    @getimage
    def test_GSXQY_LS_0012(self):
        '''律所详情页-对外投资校验字段内容'''
        log.info(self.test_GSXQY_LS_0012.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login('11099995055','ef08beca')

        company_list = ['浙江商瑞律师事务所','北京市中伦律师事务所']
        company_name = company_list[random.randint(0,len(company_list)-1)]
        log.info(company_name)

        # 字段名称列表
        fieldname_list = ['法定代表人', '经营状态', '投资数额', '投资比例', '成立日期']
        self.search_result(company_name, 0)
        count = 0
        while True:
            if not self.new_find_element(By.XPATH, self.dimensionality()[4]):
                if count <= 5:
                    self.swipeUp(x1=0.5, y1=0.50, y2=0.40, t=500)
                    count += 1
                else:
                    log.error("错误——未找到对外投资")
                    break
            else:
                break
        self.new_find_element(By.XPATH, self.dimensionality()[4]).click()

        #1公司名称：校验是否可点击，点击进入对应企业详情页
        result_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/outinvest_company_name_tv').is_enabled()
        self.assertTrue(result_01, msg='公司不可点')
        if result_01 == True:
            text_01_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/outinvest_company_name_tv').text
            log.info('校验公司名称:%s(可点击)'%text_01_01)
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/outinvest_company_name_tv').click()
            text_01_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/firm_detail_name_tv').text
            self.assertEqual(text_01_01,text_01_02,msg='公司名称不相等')

            #获取法人
            legal_representative = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_value_1').text
            #获取经营状态
            management_forms = self.new_find_element(By.XPATH,"//android.view.ViewGroup/android.widget.LinearLayout/android.widget.TextView[1]").text
            # 获取成立日期
            date = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_value_3').text
            date_num = re.sub("\D", "", date)
            #获取投资数额
            count = 1
            while True:
                if not self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='股东信息']"):
                    if count <= 3:
                        self.swipeUp(x1=0.5, y1=0.70, y2=0.30)
                        count += 1
                    else:
                        log.error("错误———未找到股东信息")
                else:
                    break
            self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='股东信息']").click()
            amount = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/holderinfo_name_tv' and @text='%s']/../../../following-sibling::android.widget.LinearLayout/android.widget.LinearLayout/*[@resource-id='com.tianyancha.skyeye:id/holder_capitalactl_amomon_tv']"%company_name).text
            #获取投资比例
            scale = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/holderinfo_name_tv' and @text='%s']/../../../following-sibling::android.widget.TextView[2]"%company_name).text

            self.go_back()
            self.go_back()

        #2股权结构：校验是否可点击，非vip点击提示开通vip
        result_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_outinvest_title_right').is_enabled()
        self.assertTrue(result_02,msg='股权结构不可点')
        if result_02 == True:
            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_outinvest_title_right').click()
            text_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_top_title').text
            self.assertEqual(text_02,'VIP会员可无限次查看股权结构',msg='未弹出开通vip弹框')

            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/iv_close').click()

        #3法定代表人：校验是否和被投资公司法定代表人相同
        text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/outinvest_legal_tv').text
        log.info('校验法定代表人:%s'%text_03)
        self.assertEqual(text_03,legal_representative,msg='与被投资公司法定代表人不同')

        #4经营状态：校验是否和被投资公司经营状态相同
        text_04 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/outinvest_reg_capital_tv').text
        log.info('校验经营状态:%s'%text_04)
        self.assertEqual(text_04,management_forms, msg='与被投资公司经营状态不同')

        #5投资数额：校验是否和被投资公司股东中此公司认缴出资额相同
        text_05 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_outinvest_amount').text
        log.info('校验投资数额:%s' % text_05)
        if '.' in amount:
            self.assertEqual(text_05, amount,msg='与被投资公司股东中此公司认缴出资额不同')
        else:
            text_05_01 = re.sub("\D", "", text_05)
            num_05_01 = re.sub("\D", "", amount)
            num_05_02 = num_05_01 + '00'
            self.assertEqual(text_05_01,num_05_02,msg='与被投资公司股东中此公司认缴出资额不同')

        #6投资比例：校验是否和被投资公司股东中此公司持股比例相同
        text_06 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_outinvest_ratio').text
        log.info('校验投资比例:%s' % text_06)
        if '.' in  scale:
            text_06_01 = re.sub("\D", "", scale)
            num_06_01 = re.sub("\D", "", text_06)
            num_06_02 = num_06_01 + '00'
            self.assertEqual(text_06_01, num_06_02, msg='与被投资公司股东中此公司投资比例不同')
        else:
            self.assertEqual(text_06, scale,msg='与被投资公司股东中此公司投资比例不同')

        #7成立日期：校验是否和被投资公司成立日期相同(格式不同为YYYY-MM-DD)
        text_07 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_outinverst_date').text
        log.info('校验成立日期:%s' % text_07)
        num_07 = re.sub("\D", "", text_07)
        self.assertEqual(num_07, date_num, msg='与被投资公司成立日期不同')
        result_07 = self.check_date(text_07)
        self.assertTrue(result_07,msg='格式非YYYY-MM-DD')

