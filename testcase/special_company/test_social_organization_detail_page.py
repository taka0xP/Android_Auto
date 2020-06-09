from common.operation import Operation, getimage
from selenium.webdriver.common.by import By
from common.MyTest import MyTest
from common.ReadData import Read_Ex
from Providers.logger import Logger
from common.CreditIdentifier import UnifiedSocialCreditIdentifier
import re
import time
import random

#非vip——110-9999-5056

log = Logger("公司详情页-社会组织详情页").getlog()

class Social_organization_detail_page(MyTest, Operation):
    """公司详情页-社会组织详情页"""

    def search_result(self, company, index=0):
        """进入关键词搜索结果列表第一家公司详情页"""
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/txt_search_copy1').click()
        self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/search_input_et').send_keys(company)
        self.new_find_elements(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/tv_company_name']")[index].click()

    def go_back(self):
        '''页面返回'''
        self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_back').click()

    def title_name(self):
        """获取页面名称"""
        title_text = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/app_title_name').text
        return title_text

    def check_date1(self, str):
        """判断日期字符串格式是否为YYYY.MM.DD"""
        try:
            time.strptime(str,"%Y.%m.%d")
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
    def check_num(self,str):
        '''校验字符串中是否只包含数字'''
        result = str.isdigit()
        return result

    def check_chinese(self,check_str):
        """判断字符串中是否包含中文"""
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

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

    def test_GSXQY_SHZZ_0001(self):
        '''公司详情页-社会组织详情页01'''
        log.info(self.test_GSXQY_SHZZ_0001.__doc__)

        company_list = ['中国煤炭工业协会', '横店社团经济企业联合会', '海南省企业家协会', '国电靖远发电有限公司集体资产管理协会', '贵州省中小企业服务中心']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        log.info(company_name)
        self.search_result(company_name)

        fieldname_list = ['法定代表人', '注册资本', '成立登记日期']  # 社会组织头部信息展示字段

        # 校验事业单位头部信息字段名称
        sub_01 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_title_1').text
        sub_02 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_title_2').text
        sub_03 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_title_3').text
        self.assertEqual(sub_01, '法定代表人', msg='错误——%s' % fieldname_list[0])
        self.assertEqual(sub_02, '注册资本', msg='错误——%s' % fieldname_list[1])
        self.assertEqual(sub_03, '成立登记日期', msg='错误——%s' % fieldname_list[2])

        #进入登记信息取法定代表人名称、注册资本、成立登记日期
        count = 1
        while True:
            if not self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='登记信息']"):
                if count <= 3:
                    self.swipeUp(x1=0.5, y1=0.60, y2=0.40)
                    count += 1
                else:
                    log.error("未找到登记信息")
            else:
                break
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='登记信息']").click()
        # 法定代表人
        person = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_detail_legal_content').text
        log.info('登记信息法定代表人为：%s'%person)
        # 注册资本
        capital = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_registered_capital').text
        log.info('登记信息开办资金为：%s'%capital)
        # 成立登记日期
        date = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_establish_data').text
        log.info('登记信息成立登记日期为：%s'%date)
        self.go_back()#返回详情页
        self.swipeDown(x1=0.5, y1=0.40, y2=0.60)#下拉页面

        #1法定代表人:校验与工商信息中是否相同
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_value_1').text
        log.info('法定代表人为：%s' % text_01)
        self.assertEqual(text_01,person,msg='法定代表人与登记信息中不同')

        #2开办资金:校验与工商信息中是否相同
        text_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_value_2').text
        log.info('开办资金为：%s' % text_02)
        self.assertEqual(text_02,capital,msg='开办资金与登记信息中不同')

        #3成立登记日期:校验日期格式为YYYY.MM.DD
        text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_des_sub_value_3').text
        log.info('成立登记日期为：%s'%text_03)
        if text_03 != '-':
            num_01 = re.sub("\D", "", date)
            num_02 = re.sub("\D", "", text_03)
            self.assertEqual(num_01,num_02,msg='成立登记日期与登记信息中不同')
        else:
            log.info('成立登记日期为空')

    def test_GSXQY_SHZZ_0002(self):
        '''社会组织·登记信息`'''
        log.info(self.test_GSXQY_SHZZ_0002.__doc__)

        company_list = ['深圳市劳动和社会保障学会', '淄博市博山离退休科技工作者协会', '中国意大利商会', '赛思健康科学研究院', '上饶市新学堂科技研究中心']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        log.info(company_name)
        self.search_result(company_name)

        #进入登记信息
        count = 1
        while True:
            if not self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='登记信息']"):
                if count <= 3:
                    self.swipeUp(x1=0.5, y1=0.60, y2=0.40)
                    count += 1
                else:
                    log.error("未找到登记信息")
            else:
                break
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='登记信息']").click()

        fieldname_list = ['法定代表人/负责人','成立登记日期','登记状态','注册资本','统一社会信用代码','社会组织类型',
                          '登记证号','证书有效期','登记管理机关','业务类型','业务主管单位','业务范围','住所']  # 登记信息展示字段
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
        self.swipeDown(x1=0.5, y1=0.60, y2=0.40, t=500)

        #1 法定代表人/负责人:校验法人有数据时包含logo，无数据时无logo，人名称大于1
        logo = self.isElementExist(By.XPATH, '//android.widget.FrameLayout/android.widget.TextView')
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_detail_legal_content').text
        log.info('校验法定代表人/负责人：%s'%text_01)
        if text_01 != '-':
            self.assertTrue(logo, msg='未找到logo')
            if len(text_01)>1:
                result_01 = True
            else:
                result_01 = False
            self.assertTrue(result_01,msg='错误————%s'%fieldname_list[0])
        else:
            self.assertFalse(logo, msg='错误——无法人时无logo')
            log.info('%s为空'%fieldname_list[0])

        #2 成立登记日期:校验格式为YYYY-MM-DD
        text_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_establish_data').text
        log.info('校验成立登记日期：%s' % text_02)
        if text_02 != '-':
            result_02 = self.check_date(text_02)
            self.assertTrue(result_02,msg='错误————%s'%fieldname_list[1])
        else:
            log.info('%s为空' % fieldname_list[1])

        #3 登记状态:校验in status_list
        status_list = ['名称核准不通过','名称核准发起中','名称核准通过','在册','已成立','已成立事先报批','已撤销','已注销',
                       '成立','成立中','成立事先报批中','成立事先报批申请未通过','成立审批未通过','撤销','新申请用户',
                       '暂无','正常','注销','注销中']
        text_03 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_registered_status').text
        log.info('校验登记状态：%s' % text_03)
        if text_03 != '-':
            self.assertIn(text_03,status_list,msg='错误————%s'%fieldname_list[2])
        else:
            log.info('%s为空' % fieldname_list[2])

        #4 注册资本:校验单位in units_list
        units_list = ['万','元','万元','单位元万元']
        text_04 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/organizationcom_registered_capital').text
        log.info('校验注册资本：%s' % text_04)
        if text_04 != '-':
            unit = ''.join(re.findall('[\u4e00-\u9fa5]',text_04))
            self.assertIn(unit,units_list,msg='错误————%s' % fieldname_list[3])
        else:
            log.info('%s为空' % fieldname_list[3])

        #5 统一社会信用代码:方法校验
        text_05 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/organizationcom_unify_credit').text
        log.info('校验统一社会信用代码：%s' % text_05)
        if text_05 != '-':
            u = UnifiedSocialCreditIdentifier()
            result_05 = u.check_social_credit_code(text_05)
            self.assertTrue(result_05, msg='错误————%s' % fieldname_list[4])
        else:
            log.info('%s为空' % fieldname_list[4])

        #6 社会组织类型:校验 in type_list
        types_list = ['事业法人','事业非法人','体育事业','其它','劳动事业','卫生事业','国际性社团','基金会','外国商会','工会法人',
                      '教育事业','文化事业','机关法人','机关非法人','民办非企业','民办非企业单位','民政事业','民非','法律服务事业',
                      '涉外基金会','社会团体','社团','社团法人','社团非法人','科研事业','非公募基金会']
        text_06 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_type').text
        log.info('校验社会组织类型：%s' % text_06)
        if text_06 != '-':
            self.assertIn(text_06,types_list,msg='错误————%s' % fieldname_list[5])
        else:
            log.info('%s为空' % fieldname_list[5])

        #7 登记证号:校验格式是否为纯数字或者包含'X'case:北京环亚善扑推广中心
        text_07 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/organizationcom_register_numer').text
        log.info('校验登记证号：%s' % text_07)
        if text_07 != '-':
            if 'X' in text_07:
                result_07_01 = True
            elif 'X' not in text_07:
                result_07_01 = self.check_num(text_07)
            else:
                result_07_01 = False
            self.assertTrue(result_07_01, msg='错误————%s' % fieldname_list[6])
        else:
            log.info('%s为空' % fieldname_list[6])

        #8 证书有效期:校验格式是否为'YYYY-MM-DD'或'YYYY-MM-DD 至 YYYY-MM-DD' case:深圳市松泉中学
        text_08 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/organizationcom_validity_period').text
        log.info('校验证书有效期：%s' % text_08)
        if text_08 != '-':
            result_08_01 = self.check_date(text_08)
            if result_08_01 == False:
                split = text_08.split()
                split_01 = self.check_date(split[0])
                split_02 = self.check_date(split[2])
                if split_01 and split_02 == True:
                    result_08 = True
                else:
                    result_08 = False
                self.assertTrue(result_08, msg='错误————%s' % fieldname_list[7])
            else:
                self.assertTrue(result_08_01,msg='错误————%s' % fieldname_list[7])
        else:
            log.info('%s为空' % fieldname_list[7])

        #9 登记管理机关:校验文本是否只包含汉字
        text_09 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_register_office').text
        log.info('校验登记管理机关：%s' % text_09)
        if text_09 != '-':
            result_09 = self.check_chinese(text_09)
            self.assertTrue(result_09,msg='错误————%s'%fieldname_list[8])
        else:
            log.info('%s为空' % fieldname_list[8])

        #10 业务类型:库里无数据校验全部为'-'
        text_10 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_business_type').text
        log.info('校验业务类型：%s' % text_10)
        self.assertEqual(text_10, '-', msg='错误————%s' % fieldname_list[9])
        log.info('%s为空' % fieldname_list[9])

        #11 业务主管单位:校验不为空时字符大于一
        text_11 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/organizationcom_satrap').text
        log.info('校验业务主管单位：%s' % text_11)
        if text_11 != '-' and text_11 != '无':
            if len(text_11)>1:
                result_11 = True
            else:
                result_11 = False
            self.assertTrue(result_11, msg='错误————%s' % fieldname_list[10])
        else:
            log.info('%s为空' % fieldname_list[10])

        #12 业务范围:校验不为空时文本大于1
        text_12 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_scope').text
        log.info('校验业务范围：%s' % text_12)
        if text_12 != '-':
            if len(text_12)>1:
                result_12 = True
            else:
                result_12 = False
            self.assertTrue(result_12,msg='错误————%s'%fieldname_list[11])
        else:
            log.info('%s为空' % fieldname_list[11])

        #13 住所:校验不为空时文本大于1
        text_13 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/organizationcom_residence').text
        log.info('校验住所：%s' % text_13)
        if text_13 != '-':
            if len(text_13)>1:
                result_13 = True
            else:
                result_13 = False
            self.assertTrue(result_13,msg='错误————%s'%fieldname_list[12])
        else:
            log.info('%s为空' % fieldname_list[12])

    def test_GSXQY_SHZZ_0003(self):
        '''社会组织·主要负责人'''
        log.info(self.test_GSXQY_SHZZ_0003.__doc__)

        company_list = ['安徽外国语学院', '昆明地区离退休人员协会', '中国意大利商会', '赛思健康科学研究院','中国公共关系协会']
        company_name = company_list[random.randint(0, len(company_list) -1)]
        log.info(company_name)
        self.search_result(company_name)
        #获取法人名称
        person = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_value_1').text
        #主要负责人
        count = 1
        while True:
            if not self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='主要负责人']"):
                if count <= 3:
                    self.swipeUp(x1=0.5, y1=0.60, y2=0.40)
                    count += 1
                else:
                    log.error("未找到主要负责人")
            else:
                break

        goal = '点击「主要负责人」进入「主要负责人」进入详情页'
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='主要负责人']").click()
        title_name = self.title_name()
        self.assertEqual(title_name,'主要负责人',msg='错误——%s'%goal)

        goal_01 = '主要负责人名称和详情页头部信息法人相同'
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_name').text
        log.info('校验主要负责人:%s'%text_01)
        self.assertEqual(text_01,person,msg='错误——%s'%goal_01)

        goal_02 = '展示「法定代表人」'
        text_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/tv_role').text
        self.assertEqual(text_02,'法定代表人',msg='错误——%s'%goal_02)

    def test_GSXQY_SHZZ_0004(self):
        '''社会组织·成立公示'''
        log.info(self.test_GSXQY_SHZZ_0004.__doc__)

        company_list = ['广东省海运集装箱物流协会', '赛思健康科学研究院', '广东省新的社会阶层人士联合会', '广州誉德莱国际学校']
        company_name = company_list[random.randint(0, len(company_list) -1)]
        log.info(company_name)
        self.search_result(company_name)
        fieldname_list = ['办结日期：','业务类型：']

        #成立公示
        count = 1
        while True:
            if not self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='成立公示']"):
                if count <= 3:
                    self.swipeUp(x1=0.5, y1=0.60, y2=0.40)
                    count += 1
                else:
                    log.error("未找到成立公示")
            else:
                break

        goal = '点击「成立公示」进入「成立公示」进入详情页'
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='成立公示']").click()
        title_name = self.title_name()
        self.assertEqual(title_name,'成立公示',msg='错误——%s'%goal)

        for i in range(len(fieldname_list)):
            result = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']"%fieldname_list[i])
            log.info(fieldname_list[i])
            self.assertTrue(result,msg='未找到——%s'%fieldname_list[i])

        #1 办结日期：校验格式是否为YYYY-MM-DD
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/establish_time_tv').text
        log.info('校验办结日期：%s'%text_01)
        if text_01 != '-':
            result_01 = self.check_date(text_01)
            self.assertTrue(result_01,msg='错误——%s'%fieldname_list[0])
        else:
            log.info('%s为空' % fieldname_list[0])

        #2 业务类型:校验in types_list
        types_list = ['社会组织成立','成立登记']
        text_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/establish_type_tv').text
        self.assertIn(text_02,types_list,msg='错误——%s'%fieldname_list[1])

    def test_GSXQY_SHZZ_0005(self):
        '''社会组织·注销公示'''
        log.info(self.test_GSXQY_SHZZ_0005.__doc__)

        company_list = ['福建省医学装备协会', '福建省国际科技合作协会', '福建省二轻工业协会', '福建省美术家协会', '福建省摄影家协会']
        company_name = company_list[random.randint(0, len(company_list)-1)]
        log.info(company_name)
        self.search_result(company_name)
        fieldname_list = ['办结日期：', '业务类型：']

        #注销公示
        count = 1
        while True:
            if not self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='注销公示']"):
                if count <= 3:
                    self.swipeUp(x1=0.5, y1=0.60, y2=0.40)
                    count += 1
                else:
                    log.error("未找到注销公示")
            else:
                break

        goal = '点击「注销公示」进入「注销公示」进入详情页'
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='注销公示']").click()
        title_name = self.title_name()
        self.assertEqual(title_name, '注销公示', msg='错误——%s' % goal)

        for i in range(len(fieldname_list)):
            result = self.isElementExist(By.XPATH,"//*[@class='android.widget.TextView' and @text='%s']" % fieldname_list[i])
            log.info(fieldname_list[i])
            self.assertTrue(result, msg='未找到——%s' % fieldname_list[i])

        # 1 办结日期：校验格式是否为YYYY-MM-DD
        text_01 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/cancel_time_tv').text
        log.info('校验办结日期：%s' % text_01)
        if text_01 != '-':
            result_01 = self.check_date(text_01)
            self.assertTrue(result_01, msg='错误——%s' % fieldname_list[0])
        else:
            log.info('%s为空' % fieldname_list[0])

        # 2 业务类型:校验in types_list
        types_list = ['注销登记']
        text_02 = self.new_find_element(By.ID,'com.tianyancha.skyeye:id/cancel_type_tv').text
        self.assertIn(text_02, types_list, msg='错误——%s' % fieldname_list[1])

    @getimage
    def test_GSXQY_SHZZ_0006(self):
        '''社会组织·对外投资'''
        log.info(self.test_GSXQY_SHZZ_0006.__doc__)

        login_status = self.is_login()
        if login_status == True:
            self.logout()
        self.login('11099995056','ef08beca')

        company_list = ['四川省政府国有资产监督管理委员会', '横店社团经济企业联合会', '延庆县福利企业集体资产管理协会', '东阳市影视旅游促进会', '中国有色金属工业协会']
        company_name = company_list[random.randint(0, len(company_list) - 1)]
        log.info(company_name)
        self.search_result(company_name)
        fieldname_list = ['法定代表人', '经营状态','投资数额','投资比例','成立日期']

        # 对外投资
        count = 1
        while True:
            if not self.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='对外投资']"):
                if count <= 3:
                    self.swipeUp(x1=0.5, y1=0.60, y2=0.40)
                    count += 1
                else:
                    log.error("未找到对外投资")
            else:
                break

        goal = '点击「对外投资」进入「对外投资」进入详情页'
        self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='对外投资']").click()
        title_name = self.title_name()
        self.assertEqual(title_name, '对外投资', msg='错误——%s' % goal)

        for i in range(len(fieldname_list)):
            result = self.isElementExist(By.XPATH,
                                         "//*[@class='android.widget.TextView' and @text='%s']" % fieldname_list[i])
            log.info(fieldname_list[i])
            self.assertTrue(result, msg='未找到——%s' % fieldname_list[i])

        # 1公司名称：校验是否可点击，点击进入对应企业详情页
        result_01 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/outinvest_company_name_tv').is_enabled()
        self.assertTrue(result_01, msg='公司不可点')
        if result_01 == True:
            text_01_01 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/outinvest_company_name_tv').text
            log.info('校验公司名称:%s(可点击)' % text_01_01)
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/outinvest_company_name_tv').click()
            text_01_02 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/firm_detail_name_tv').text
            self.assertEqual(text_01_01, text_01_02, msg='公司名称不相等')

            # 获取法人
            legal_representative = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_value_1').text
            # 获取经营状态
            management_forms = self.new_find_element(By.XPATH,"//android.view.ViewGroup/android.widget.LinearLayout/android.widget.TextView[1]").text
            # 获取成立日期
            date = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_des_sub_value_3').text
            date_num = re.sub("\D", "", date)
            # 获取投资数额
            count = 1
            while True:
                if not self.new_find_element(By.XPATH,
                                             "//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='股东信息']"):
                    if count <= 3:
                        self.swipeUp(x1=0.5, y1=0.70, y2=0.30)
                        count += 1
                    else:
                        log.error("错误———未找到股东信息")
                else:
                    break
            self.new_find_element(By.XPATH, "//*[@resource-id='com.tianyancha.skyeye:id/item_company_module_name_tv' and @text='股东信息']").click()
            amount = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/holderinfo_name_tv' and @text='%s']/../../../following-sibling::android.widget.LinearLayout/android.widget.LinearLayout/*[@resource-id='com.tianyancha.skyeye:id/holder_capitalactl_amomon_tv']" % company_name).text
            # 获取投资比例
            scale = self.new_find_element(By.XPATH,"//*[@resource-id='com.tianyancha.skyeye:id/holderinfo_name_tv' and @text='%s']/../../../following-sibling::android.widget.TextView[2]" % company_name).text

            self.go_back()
            self.go_back()

        # 2股权结构：校验是否可点击，非vip点击提示开通vip
        result_02 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_outinvest_title_right').is_enabled()
        self.assertTrue(result_02, msg='股权结构不可点')
        if result_02 == True:
            self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_outinvest_title_right').click()
            text_02 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_top_title').text
            self.assertEqual(text_02, 'VIP会员可无限次查看股权结构', msg='未弹出开通vip弹框')

            self.new_find_element(By.ID,'com.tianyancha.skyeye:id/iv_close').click()

        # 3法定代表人：校验是否和被投资公司法定代表人相同
        text_03 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/outinvest_legal_tv').text
        log.info('校验法定代表人:%s' % text_03)
        self.assertEqual(text_03, legal_representative, msg='与被投资公司法定代表人不同')

        # 4经营状态：校验是否和被投资公司经营状态相同
        text_04 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/outinvest_reg_capital_tv').text
        log.info('校验经营状态:%s' % text_04)
        self.assertEqual(text_04, management_forms, msg='与被投资公司经营状态不同')

        # 5投资数额：校验是否和被投资公司股东中此公司认缴出资额相同
        text_05 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_outinvest_amount').text
        log.info('校验投资数额:%s' % text_05)
        if '.' in amount:
            self.assertEqual(text_05, amount, msg='与被投资公司股东中此公司认缴出资额不同')
        else:
            text_05_01 = re.sub("\D", "", text_05)
            num_05_01 = re.sub("\D", "", amount)
            num_05_02 = num_05_01 + '00'
            self.assertEqual(text_05_01, num_05_02, msg='与被投资公司股东中此公司认缴出资额不同')

        # 6投资比例：校验是否和被投资公司股东中此公司持股比例相同
        text_06 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_outinvest_ratio').text
        log.info('校验投资比例:%s' % text_06)
        if '.' in scale:
            text_06_01 = re.sub("\D", "", scale)
            num_06_01 = re.sub("\D", "", text_06)
            num_06_02 = num_06_01 + '00'
            self.assertEqual(text_06_01, num_06_02, msg='与被投资公司股东中此公司投资比例不同')
        else:
            self.assertEqual(text_06, scale, msg='与被投资公司股东中此公司投资比例不同')

        # 7成立日期：校验是否和被投资公司成立日期相同(格式不同为YYYY-MM-DD)
        text_07 = self.new_find_element(By.ID, 'com.tianyancha.skyeye:id/tv_outinverst_date').text
        log.info('校验成立日期:%s' % text_07)
        num_07 = re.sub("\D", "", text_07)
        self.assertEqual(num_07, date_num, msg='与被投资公司成立日期不同')
        result_07 = self.check_date(text_07)
        self.assertTrue(result_07, msg='格式非YYYY-MM-DD')

    # # :校验
        # text_0 = self.new_find_element(By.ID,'').text
        # log.info('校验：%s' % text_0)
        # if text_0 != '-':
        #     self.assertTrue(result,msg='错误————%s'%fieldname_list[0])
        # else:
        #     log.info('%s为空' % fieldname_list[0])


















