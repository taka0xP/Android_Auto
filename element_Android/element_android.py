# -*- coding: utf-8 -*-
# @Time    : 2019-09-20 09:30
# @Author  : ZYF


from selenium.webdriver.common.by import By
from common.operation import Operation
import time

# from selenium.webdriver.support.select import Select


"""封装页面元素"""

ELEMENT = {
    # 首页元素
    '首页搜索框': (By.ID, 'com.tianyancha.skyeye:id/txt_search_copy1'),
    '查公司': (By.ID, 'com.tianyancha.skyeye:id/home_tab1'),
    '查老板1': (By.ID, 'com.tianyancha.skyeye:id/home_tab2'),
    '查关系': (By.ID, 'com.tianyancha.skyeye:id/home_tab3'),
    '分类搜索': (By.ID, 'com.tianyancha.skyeye:id/ibtn_home_all'),
    # 首页底部
    '首页': (By.ID, 'com.tianyancha.skyeye:id/tab_iv_1'),
    '查老板2': (By.ID, 'com.tianyancha.skyeye:id/tab_iv_2'),
    '商业头条': (By.XPATH,
             '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]/android.widget.ImageView'),
    '问大家': (By.ID, 'com.tianyancha.skyeye:id/tab_iv_3'),
    '我的': (By.ID, 'com.tianyancha.skyeye:id/tab_iv_5'),

    # 搜索页
    '查公司—搜索页搜索框': (By.ID, 'com.tianyancha.skyeye:id/search_input_et'),
    '查老板-搜索页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '差关系-搜索页搜索框': (By.ID, ''),

    # 分类搜索页
    '页面返回-分类搜索页': (By.ID, 'com.tianyancha.skyeye:id/become_vip_iv_back'),
    '天眼查-分类搜索页': (By.ID, 'com.tianyancha.skyeye:id/app_title_logo'),
    '商标注册': (By.ID, 'com.tianyancha.skyeye:id/iv_trademark_reg'),
    '附近公司': (By.ID, 'com.tianyancha.skyeye:id/ll_near_company'),
    '查税号': (By.ID, 'com.tianyancha.skyeye:id/search_rate'),
    '身边老板': (By.ID, 'com.tianyancha.skyeye:id/ll_side_boss'),
    '查老赖': (By.ID, 'com.tianyancha.skyeye:id/iv_search_deadbeat'),
    '地址电话': (By.ID, 'com.tianyancha.skyeye:id/phone1'),
    '招聘': (By.ID, 'com.tianyancha.skyeye:id/ll_search_jobs'),
    '''分类搜索'''
    '招投标': (By.ID, 'com.tianyancha.skyeye:id/ll_search_bid'),
    '债券': (By.ID, 'com.tianyancha.skyeye:id/ll_search_bond'),
    '中国香港企业': (By.ID, 'com.tianyancha.skyeye:id/search_hk_company'),
    '中国台湾企业': (By.ID, 'com.tianyancha.skyeye:id/search_taiwan_company'),
    '社会组织': (By.ID, 'com.tianyancha.skyeye:id/search_regime'),
    '律师事务所': (By.ID, 'com.tianyancha.skyeye:id/search_law'),
    '诉讼': (By.ID, 'com.tianyancha.skyeye:id/ll_search_lawsuit'),
    '''分类搜索'''
    '法院公告': (By.ID, 'com.tianyancha.skyeye:id/ll_search_court'),
    '''分类搜索'''
    '税务评级': (By.ID, 'com.tianyancha.skyeye:id/ll_search_tax_rating'),
    '''分类搜索'''
    '进出口信用': (By.ID, 'com.tianyancha.skyeye:id/search_outin_credit'),
    '''分类搜索'''
    '司法拍卖': (By.ID, 'com.tianyancha.skyeye:id/search_judicial_sale'),
    '''分类搜索'''
    '开庭公告': (By.ID, 'com.tianyancha.skyeye:id/search_court_notice'),
    '商标': (By.ID, 'com.tianyancha.skyeye:id/ll_search_brand'),
    '专利': (By.ID, 'com.tianyancha.skyeye:id/ll_search_patent'),
    '''分类搜索'''
    '著作权': (By.ID, 'com.tianyancha.skyeye:id/ll_search_copyright'),
    '网址': (By.ID, 'com.tianyancha.skyeye:id/ll_search_website'),

    # 附近公司页
    '附近公司返回': (By.ID, 'com.tianyancha.skyeye:id/app_title_back'),
    '全部行业': (By.ID, 'com.tianyancha.skyeye:id/select_date'),
    '距离': (By.ID, 'com.tianyancha.skyeye:id/select_category'),
    '更多筛选': (By.ID, 'com.tianyancha.skyeye:id/select_state'),
    '导出数据': (By.ID, 'com.tianyancha.skyeye:id/tv_export_data'),
    '邮箱输入框': (By.ID, 'com.tianyancha.skyeye:id/et_attention_add_title'),
    '邮箱确认': (By.ID, 'com.tianyancha.skyeye:id/btn_pos'),
    '导航': (By.XPATH,
           '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.RelativeLayout'),
    '附近公司第一家': (By.XPATH,
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.LinearLayout'),
    '全部行业list': (By.ID, 'com.tianyancha.skyeye:id/lv_oiIndustry_left'),
    # 查税号页
    '查税号页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '查税号页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 查老赖页
    '查老赖页面返回': (By.ID, 'com.tianyancha.skyeye:id/app_title_back'),
    '查老赖搜索框': (By.XPATH,
               '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.TextView'),
    '查老赖搜索': (By.ID, 'com.tianyancha.skyeye:id/search_input_et'),
    # 地址电话页
    '地址电话页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '地址电话页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 招聘页
    '招聘页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '招聘页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 招投标页
    '招投标页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '招投标页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 债券页
    '债券页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '债券页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 中国香港企业
    '中国香港企业页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '中国香港企业页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 中国台湾企业
    '中国台湾企业页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '中国台湾企业页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 社会组织
    '社会组织页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '社会组织页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 律师事务所
    '律师事务所页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '律师事务所页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 诉讼
    '诉讼页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '诉讼页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 法院公告
    '法院公告页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '法院公告页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 税务评级
    '税务评级页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '税务评级页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 进出口信用
    '进出口信用页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '进出口信用页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 司法拍卖
    '司法拍卖页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '司法拍卖页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 开庭公告
    '开庭公告页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '开庭公告页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 商标
    '商标页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '商标页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 专利
    '专利页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '专利页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 著作权
    '著作权页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '著作权页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    # 网址
    '网址页搜索框': (By.ID, 'com.tianyancha.skyeye:id/et_search_input'),
    '网址页搜索': (By.ID, 'com.tianyancha.skyeye:id/search_back_iv'),
    '': (),

    # 搜索结果页
    '搜索结果页第一家': (By.ID, 'com.tianyancha.skyeye:id/tv_company_name'),
    '': (),
    '': (),
    '': (''),

    '页面返回': (By.ID, 'com.tianyancha.skyeye:id/app_title_back'),
    'X': (By.ID, 'com.tianyancha.skyeye:id/iv_back'),
    # 我的
    '立即登录': (By.ID, 'com.tianyancha.skyeye:id/tv_user_reg'),
    '编辑': (By.ID, 'com.tianyancha.skyeye:id/tv_edit_user_info'),

    # 登录页
    '普通登录': (By.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.TextView'),
    '请输入手机号': (By.ID, 'com.tianyancha.skyeye:id/input_phone'),
    '请输入密码': (By.ID, 'com.tianyancha.skyeye:id/input_password'),
    '登录': (By.ID, 'com.tianyancha.skyeye:id/btn_login'),
    '': (),
    '': (),
    '': (),
    '': (),
    '': (),
    '': (),
    '': (),
    '': (),
    '': (),

    # 公司官方信息页
    '公司官方信息页返回': (By.ID, 'com.tianyancha.skyeye:id/app_title_back'),
    # 企业背景
    '工商信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="工商信息"]'),
    '主要人员': (By.XPATH, '//*[@class="android.widget.TextView" and @text="主要人员"]'),
    '股东信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="股东信息"]'),
    '对外投资': (By.XPATH, '//*[@class="android.widget.TextView" and @text="对外投资"]'),
    '股权结构': (By.XPATH, '//*[@class="android.widget.TextView" and @text="股权结构"]'),
    '最终受益人': (By.XPATH, '//*[@class="android.widget.TextView" and @text="最终受益人"]'),
    '实际控制人': (By.XPATH, '//*[@class="android.widget.TextView" and @text="实际控制人"]'),
    '实际控制权': (By.XPATH, '//*[@class="android.widget.TextView" and @text="实际控制权"]'),
    '财务简析': (By.XPATH, '//*[@class="android.widget.TextView" and @text="财务简析"]'),
    '企业关系': (By.XPATH, '//*[@class="android.widget.TextView" and @text="企业关系"]'),
    '变更记录': (By.XPATH, '//*[@class="android.widget.TextView" and @text="变更记录"]'),
    '企业年报': (By.XPATH, '//*[@class="android.widget.TextView" and @text="企业年报"]'),
    '企业公示': (By.XPATH, '//*[@class="android.widget.TextView" and @text="企业公示"]'),
    '附近同行': (By.XPATH, '//*[@class="android.widget.TextView" and @text="附近同行"]'),
    # 企业年报结果页
    '企业年报结果页第一条': (By.XPATH,
                   '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]'),

    # 风险信息
    '''风险信息'''
    '开庭公告': (By.XPATH, '//*[@class="android.widget.TextView" and @text="开庭公告"]'),
    '法律诉讼': (By.XPATH, '//*[@class="android.widget.TextView" and @text="法律诉讼"]'),
    '''风险信息'''
    '法院公告': (By.XPATH, '//*[@class="android.widget.TextView" and @text="法院公告"]'),
    '限制消费令': (By.XPATH, '//*[@class="android.widget.TextView" and @text="限制消费令"]'),
    '终本案件': (By.XPATH, '//*[@class="android.widget.TextView" and @text="终本案件"]'),
    '失信信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="失信信息"]'),
    '被执行人': (By.XPATH, '//*[@class="android.widget.TextView" and @text="被执行人"]'),
    '司法协助': (By.XPATH, '//*[@class="android.widget.TextView" and @text="司法协助"]'),
    '送达公告': (By.XPATH, '//*[@class="android.widget.TextView" and @text="送达公告"]'),
    '立案信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="立案信息"]'),
    '经营异常': (By.XPATH, '//*[@class="android.widget.TextView" and @text="经营异常"]'),
    '行政处罚': (By.XPATH, '//*[@class="android.widget.TextView" and @text="行政处罚"]'),
    '严重违法': (By.XPATH, '//*[@class="android.widget.TextView" and @text="严重违法"]'),
    '股权出质': (By.XPATH, '//*[@class="android.widget.TextView" and @text="股权出质"]'),
    '股权质押': (By.XPATH, '//*[@class="android.widget.TextView" and @text="股权质押"]'),
    '税收违法': (By.XPATH, '//*[@class="android.widget.TextView" and @text="税收违法"]'),
    '动产抵押': (By.XPATH, '//*[@class="android.widget.TextView" and @text="动产抵押"]'),
    '环保处罚': (By.XPATH, '//*[@class="android.widget.TextView" and @text="环保处罚"]'),
    '欠税公告': (By.XPATH, '//*[@class="android.widget.TextView" and @text="欠税公告"]'),
    '''风险信息'''
    '司法拍卖': (By.XPATH, '//*[@class="android.widget.TextView" and @text="司法拍卖"]'),
    '询价评估': (By.XPATH, '//*[@class="android.widget.TextView" and @text="询价评估"]'),
    '清算信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="清算信息"]'),
    '知识产权出质': (By.XPATH, '//*[@class="android.widget.TextView" and @text="知识产权出质"]'),
    '公示催告': (By.XPATH, '//*[@class="android.widget.TextView" and @text="公示催告"]'),
    '土地抵押': (By.XPATH, '//*[@class="android.widget.TextView" and @text="土地抵押"]'),
    '简易注销': (By.XPATH, '//*[@class="android.widget.TextView" and @text="简易注销"]'),

    # 企业发展
    '融资历程': (By.XPATH, '//*[@class="android.widget.TextView" and @text="融资历程"]'),
    '投资事件': (By.XPATH, '//*[@class="android.widget.TextView" and @text="投资事件"]'),
    '核心团队': (By.XPATH, '//*[@class="android.widget.TextView" and @text="核心团队"]'),
    '企业业务': (By.XPATH, '//*[@class="android.widget.TextView" and @text="企业业务"]'),
    '竞品信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="竞品信息"]'),
    '投资机构': (By.XPATH, '//*[@class="android.widget.TextView" and @text="投资机构"]'),
    '私募基金': (By.XPATH, '//*[@class="android.widget.TextView" and @text="私募基金"]'),

    # 经营信息
    '招聘信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="招聘信息"]'),
    '新闻舆情': (By.XPATH, '//*[@class="android.widget.TextView" and @text="新闻舆情"]'),
    '行政许可': (By.XPATH, '//*[@class="android.widget.TextView" and @text="行政许可"]'),
    '''经营信息'''
    '税务评级': (By.XPATH, '//*[@class="android.widget.TextView" and @text="税务评级"]'),
    '抽查检查': (By.XPATH, '//*[@class="android.widget.TextView" and @text="抽查检查"]'),
    '双随机抽查': (By.XPATH, '//*[@class="android.widget.TextView" and @text="双随机抽查"]'),
    '资质证书': (By.XPATH, '//*[@class="android.widget.TextView" and @text="资质证书"]'),
    '''经营信息'''
    '招投标': (By.XPATH, '//*[@class="android.widget.TextView" and @text="招投标"]'),
    '产品信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="产品信息"]'),
    '微信公众号': (By.XPATH, '//*[@class="android.widget.TextView" and @text="微信公众号"]'),
    '微博': (By.XPATH, '//*[@class="android.widget.TextView" and @text="微博"]'),
    '公告研报': (By.XPATH, '//*[@class="android.widget.TextView" and @text="公告研报"]'),
    '地块公示': (By.XPATH, '//*[@class="android.widget.TextView" and @text="地块公示"]'),
    '土地转让': (By.XPATH, '//*[@class="android.widget.TextView" and @text="土地转让"]'),
    '''经营信息'''
    '进出口信用': (By.XPATH, '//*[@class="android.widget.TextView" and @text="进出口信用"]'),
    '债券信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="债券信息"]'),
    '购地信息': (By.XPATH, '//*[@class="android.widget.TextView" and @text="购地信息"]'),
    '电信许可': (By.XPATH, '//*[@class="android.widget.TextView" and @text="电信许可"]'),
    '供应商': (By.XPATH, '//*[@class="android.widget.TextView" and @text="供应商"]'),
    '客户': (By.XPATH, '//*[@class="android.widget.TextView" and @text="客户"]'),

    # 知识产权
    '': (By.XPATH, '//*[@class="android.widget.TextView" and @text="环保处罚"]'),
    '': (By.XPATH, '//*[@class="android.widget.TextView" and @text="环保处罚"]'),
    '': (By.XPATH, '//*[@class="android.widget.TextView" and @text="环保处罚"]'),
    '': (By.XPATH, '//*[@class="android.widget.TextView" and @text="环保处罚"]'),
    '': (By.XPATH, '//*[@class="android.widget.TextView" and @text="环保处罚"]'),

    '''知识产权'''
    '著作权': (),

}


class pageMethod(Operation):

    def __init__(self, driver):
        self.driver = driver

    '''登录'''

    # def login(self, phone_num, password):
    #     self.phone_num = phone_num
    #     self.password = password
    #     self.find_element(*ELEMENT['我的']).click()
    #     self.find_element(*ELEMENT['立即登录']).click()
    #     self.find_element(*ELEMENT['普通登录']).click()
    #     self.find_element(*ELEMENT['请输入手机号']).send_keys(self.phone_num)
    #     self.find_element(*ELEMENT['请输入密码']).send_keys(self.password)
    #     self.find_element(*ELEMENT['登录']).click()

    # 分类搜索
    '''进入分类搜索页'''

    def classification_search(self):
        self.new_find_element(*ELEMENT['分类搜索']).click()

    '''商标注册'''

    def Trademark_registration(self):
        self.new_find_element(*ELEMENT['商标注册']).click()

    '''附近公司'''

    def near_company(self, email):
        self.email = email
        self.new_find_element(*ELEMENT['附近公司']).click()
        self.new_find_element(*ELEMENT['附近公司第一家']).click()
        self.new_find_element(*ELEMENT['公司官方信息页返回']).click()
        self.new_find_element(*ELEMENT['导出数据']).click()
        self.new_find_element(*ELEMENT['邮箱输入框']).send_keys(self.email)
        self.new_find_element(*ELEMENT['邮箱确认']).click()
        self.new_find_element(*ELEMENT['导航']).click()

    '''查税号'''

    def check_duty_number(self, value):
        self.value = value
        self.new_find_element(*ELEMENT['查税号']).click()
        self.new_find_element(*ELEMENT['查税号页搜索框']).send_keys(self.value)
        self.new_find_element(*ELEMENT['查税号页搜索']).click()

    '''身边老板'''

    def near_boss(self):
        self.new_find_element(*ELEMENT['身边老板']).click()

    '''查老赖'''

    def check_LaoLai(self, value):
        self.value = value
        self.new_find_element(*ELEMENT['查老赖']).click()
        self.new_find_element(*ELEMENT['查老赖搜索框']).click()
        self.new_find_element(*ELEMENT['查老赖搜索']).send_keys(self.value)

    '''地址电话'''

    def address_phone(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['地址电话']).click()
        self.new_find_element(*ELEMENT['地址电话页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['地址电话页搜索']).click()

    '''招聘'''

    def recruitment(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['招聘']).click()
        self.new_find_element(*ELEMENT['招聘页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['招聘页搜索']).click()

    '''招投标'''

    def bidding(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['''分类搜索'''
                                   '招投标']).click()
        self.new_find_element(*ELEMENT['招投标页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['招投标页搜索']).click()

    '''债券'''

    def bond(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['债券']).click()
        self.new_find_element(*ELEMENT['债券页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['债券页搜索']).click()

    '''中国香港企业'''

    def HongKong_enterprises(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['中国香港企业']).click()
        self.new_find_element(*ELEMENT['中国香港企业页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['中国香港企业页搜索']).click()

    '''中国台湾企业'''

    def Taiwan_enterprises(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['中国台湾企业']).click()
        self.new_find_element(*ELEMENT['中国台湾企业页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['中国台湾企业页搜索']).click()

    '''社会组织'''

    def social_organization(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['社会组织']).click()
        self.new_find_element(*ELEMENT['社会组织页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['社会组织页搜索']).click()

    '''律师事务所'''

    def law_firm(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['律师事务所']).click()
        self.new_find_element(*ELEMENT['律师事务所页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['律师事务所页搜索']).click()

    '''诉讼'''

    def litigation(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['诉讼']).click()
        self.new_find_element(*ELEMENT['诉讼页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['诉讼页搜索']).click()

    '''法院公告'''

    def court_announcement(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['''分类搜索'''
                                   '法院公告']).click()
        self.new_find_element(*ELEMENT['法院公告页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['法院公告页搜索']).click()

    '''税务评级'''

    def credit_rating(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['''分类搜索'''
                                   '税务评级']).click()
        self.new_find_element(*ELEMENT['税务评级页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['税务评级页搜索']).click()

    '''进出口信用'''

    def inout_credit(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['''分类搜索'''
                                   '进出口信用']).click()
        self.new_find_element(*ELEMENT['进出口信用页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['进出口信用页搜索']).click()

    '''司法拍卖'''

    def judicial_auction(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['''分类搜索'''
                                   '司法拍卖']).click()
        self.new_find_element(*ELEMENT['司法拍卖页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['司法拍卖页搜索']).click()

    '''开庭公告'''

    def hearing_announcement(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['''分类搜索'''
                                   '开庭公告']).click()
        self.new_find_element(*ELEMENT['开庭公告页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['开庭公告页搜索']).click()

    '''商标'''

    def trademark(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['商标']).click()
        self.new_find_element(*ELEMENT['商标页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['商标页搜索']).click()

    '''专利'''

    def patent(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['专利']).click()
        self.new_find_element(*ELEMENT['专利页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['专利页搜索']).click()

    '''著作权'''

    def copyright(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['''分类搜索'''
                                   '著作权']).click()
        self.new_find_element(*ELEMENT['著作权页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['著作权页搜索']).click()

    '''网址'''

    def url(self, company_name):
        self.company_name = company_name
        self.new_find_element(*ELEMENT['网址']).click()
        self.new_find_element(*ELEMENT['网址页搜索框']).send_keys(self.company_name)
        self.new_find_element(*ELEMENT['网址页搜索']).click()

    # 普通公司维度信息
    # 企业背景
    '''工商信息'''

    def gs_information(self):
        try:
            self.new_find_element(*ELEMENT['工商信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''主要人员'''

    def main_staff(self):
        try:
            self.new_find_element(*ELEMENT['主要人员']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''股东信息'''

    def shareholders_information(self):
        try:
            self.new_find_element(*ELEMENT['股东信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''对外投资'''

    def foreign_investment(self):
        try:
            self.new_find_element(*ELEMENT['对外投资']).click()
        except Exception as e:
            print(e)
            log.error(e)

    '''股权结构'''

    def equity_structure(self):
        try:
            self.new_find_element(*ELEMENT['股权结构']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''最终受益人'''

    def ultimate_beneficiary(self):
        try:
            self.new_find_element(*ELEMENT['最终受益人']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''实际控制人'''

    def actual_controller(self):
        try:
            self.new_find_element(*ELEMENT['实际控制人']).click()
        except Exception as e:
            print(e)
            log.error(e)

    '''实际控制权'''

    def actual_control(self):
        try:
            self.new_find_element(*ELEMENT['实际控制权']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''财务简析'''

    def financial_analysis(self):
        try:
            self.new_find_element(*ELEMENT['财务简析']).click()
            time.sleep(2)
        except Exception as e:
            print(e)
            log.error(e)

    '''企业关系'''

    def business_relationship(self):
        try:
            self.new_find_element(*ELEMENT['企业关系']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''变更记录'''

    def change_record(self):
        try:
            self.new_find_element(*ELEMENT['变更记录']).click()
        except Exception as e:
            print(e)
            log.error(e)

    '''企业年报'''

    def annual_reports(self):
        try:
            self.new_find_element(*ELEMENT['企业年报']).click()
            self.new_find_element(*ELEMENT['企业年报结果页第一条']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''企业公示'''

    def enterprise_public(self):
        try:
            self.new_find_element(*ELEMENT['企业公示']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''附近同行'''

    def near_counterpart(self):
        try:
            self.new_find_element(*ELEMENT['附近同行']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    # 风险信息
    '''开庭公告'''

    def hearing_announcement0(self):
        try:
            self.new_find_element(*ELEMENT['''风险信息'''
                                       '开庭公告']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''法律诉讼'''

    def Legal_action(self):
        try:
            self.new_find_element(*ELEMENT['法律诉讼']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''法院公告'''

    def court_announcement0(self):
        try:
            self.new_find_element(*ELEMENT['''风险信息'''
                                       '法院公告']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''限制消费令'''

    def consumption_restriction(self):
        try:
            self.new_find_element(*ELEMENT['限制消费令']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''终本案件'''

    def end_case(self):
        try:
            self.new_find_element(*ELEMENT['终本案件']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''失信信息'''

    def credibility_information(self):
        try:
            self.new_find_element(*ELEMENT['失信信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''被执行人'''

    def subjected_execution(self):
        try:
            self.new_find_element(*ELEMENT['被执行人']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''司法协助'''

    def Judicial_assistance(self):
        try:
            self.new_find_element(*ELEMENT['司法协助']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''送达公告'''

    def delivery_notice(self):
        try:
            self.new_find_element(*ELEMENT['送达公告']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''立案信息'''

    def file_information(self):
        try:
            self.new_find_element(*ELEMENT['立案信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''经营异常'''

    def abnormal_operation(self):
        try:
            self.new_find_element(*ELEMENT['经营异常']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''行政处罚'''

    def administrative_punishment(self):
        try:
            self.new_find_element(*ELEMENT['行政处罚']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''严重违法'''

    def serious_illegal(self):
        try:
            self.new_find_element(*ELEMENT['严重违法']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''股权出质'''

    def equity_pledge_out(self):
        try:
            self.new_find_element(*ELEMENT['股权出质']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''股权质押'''

    def equity_pledge_in(self):
        try:
            self.new_find_element(*ELEMENT['股权质押']).click()
        except Exception as e:
            print(e)
            log.error(e)

    '''税收违法'''

    def tax_illegal(self):
        try:
            self.new_find_element(*ELEMENT['税收违法']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''动产抵押'''

    def chattel_mortgage(self):
        try:
            self.new_find_element(*ELEMENT['动产抵押']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''环保处罚'''

    def environmental_penalties(self):
        try:
            self.new_find_element(*ELEMENT['环保处罚']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''欠税公告'''

    def taxes_announcement(self):
        try:
            self.new_find_element(*ELEMENT['欠税公告']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''司法拍卖'''

    def judicial_auction0(self):
        try:
            self.new_find_element(*ELEMENT['''风险信息'''
                                       '司法拍卖']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''询价评估'''

    def inquiry_assess(self):
        try:
            self.new_find_element(*ELEMENT['询价评估']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''清算信息'''

    def accounting_information(self):
        try:
            self.new_find_element(*ELEMENT['清算信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''知识产权出质'''

    def intellectual_property(self):
        try:
            self.new_find_element(*ELEMENT['知识产权出质']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''公示催告'''

    def public_notice(self):
        try:
            self.new_find_element(*ELEMENT['公示催告']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''土地抵押'''

    def land_mortgage(self):
        try:
            self.new_find_element(*ELEMENT['土地抵押']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''简易注销'''

    def simple_cancellation(self):
        try:
            self.new_find_element(*ELEMENT['简易注销']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    # 企业发展
    '''融资历程'''

    def finance_course(self):
        try:
            self.new_find_element(*ELEMENT['融资历程']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''投资事件'''

    def investment_event(self):
        try:
            self.new_find_element(*ELEMENT['投资事件']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''核心团队'''

    def core_team(self):
        try:
            self.new_find_element(*ELEMENT['核心团队']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''企业业务'''

    def enterprise_service(self):
        try:
            self.new_find_element(*ELEMENT['企业业务']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''竞品信息'''

    def Competing_information(self):
        try:
            self.new_find_element(*ELEMENT['竞品信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''投资机构'''

    def investment_institutions(self):
        try:
            self.new_find_element(*ELEMENT['投资机构']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''私募基金'''

    def private_equity(self):
        try:
            self.new_find_element(*ELEMENT['私募基金']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    # 经营信息
    '''招聘信息'''

    def recruitment_information(self):
        try:
            self.new_find_element(*ELEMENT['招聘信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''新闻舆情'''

    def news_opinion(self):
        try:
            self.new_find_element(*ELEMENT['新闻舆情']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''行政许可'''

    def administrative_licensing(self):
        try:
            self.new_find_element(*ELEMENT['行政许可']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''税务评级'''

    def credit_rating0(self):
        try:
            self.new_find_element(*ELEMENT['''经营信息'''
                                       '税务评级']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''抽查检查'''

    def spot_check(self):
        try:
            self.new_find_element(*ELEMENT['抽查检查']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''双随机抽查'''

    def double_random_check(self):
        try:
            self.new_find_element(*ELEMENT['双随机抽查']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''资质证书'''

    def qualification_certificate(self):
        try:
            self.new_find_element(*ELEMENT['资质证书']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''招投标'''

    def bidding0(self):
        try:
            self.new_find_element(*ELEMENT['''经营信息'''
                                       '招投标']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''产品信息'''

    def product_information(self):
        try:
            self.new_find_element(*ELEMENT['产品信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''微信公众号'''

    def WeChat_number(self):
        try:
            self.new_find_element(*ELEMENT['微信公众号']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''微博'''

    def weibo(self):
        try:
            self.new_find_element(*ELEMENT['微博']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''公告研报'''

    def announcement_report(self):
        try:
            self.new_find_element(*ELEMENT['公告研报']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''地块公示'''

    def place_public(self):
        try:
            self.new_find_element(*ELEMENT['地块公示']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''土地转让'''

    def land_transfer(self):
        try:
            self.new_find_element(*ELEMENT['土地转让']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''进出口信用'''

    def inout_credit0(self):
        try:
            self.new_find_element(*ELEMENT['''经营信息'''
                                       '进出口信用']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''债券信息'''

    def bond_information(self):
        try:
            self.new_find_element(*ELEMENT['债券信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''购地信息'''

    def purchase_information(self):
        try:
            self.new_find_element(*ELEMENT['购地信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''电信许可'''

    def telecommunications_license(self):
        try:
            self.new_find_element(*ELEMENT['电信许可']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''供应商'''

    def supplier(self):
        try:
            self.new_find_element(*ELEMENT['供应商']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''客户'''

    def customer(self):
        try:
            self.new_find_element(*ELEMENT['客户']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    # 知识产权
    '''商标信息'''

    def trademark_information(self):
        try:
            self.new_find_element(*ELEMENT['商标信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''专利信息'''

    def patent_information(self):
        try:
            self.new_find_element(*ELEMENT['专利信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''著作权'''

    def copyright0(self):
        try:
            self.new_find_element(*ELEMENT['''知识产权'''
                                       '著作权']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''网站备案'''

    def web_record(self):
        try:
            self.new_find_element(*ELEMENT['网站备案']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    # 历史信息VIP
    '''历史工商信息'''  # his_gs_information

    def his_gs_information(self):
        try:
            self.new_find_element(*ELEMENT['历史工商信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史股东'''  # his_shareholders_information

    def his_shareholders(self):
        try:
            self.new_find_element(*ELEMENT['历史股东']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史对外投资'''  # his_foreign_investment

    def his_foreign_investment(self):
        try:
            self.new_find_element(*ELEMENT['历史对外投资']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史开庭公告'''  # his_hearing_announcement

    def his_hearing_announcement(self):
        try:
            self.new_find_element(*ELEMENT['历史开庭公告']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史法律诉讼'''  # his_Legal_action

    def his_Legal_action(self):
        try:
            self.new_find_element(*ELEMENT['历史法律诉讼']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史法院公告'''  # his_court_announcement

    def his_court_announcement(self):
        try:
            self.new_find_element(*ELEMENT['历史法院公告']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史失信信息'''  # his_credibility_information

    def his_credibility_information(self):
        try:
            self.new_find_element(*ELEMENT['历史失信信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史被执行人'''  # his_subjected_execution

    def his_subjected_execution(self):
        try:
            self.new_find_element(*ELEMENT['历史被执行人']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史司法协助'''  # his_Judicial_assistance

    def his_Judicial_assistance(self):
        try:
            self.new_find_element(*ELEMENT['历史司法协助']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史经营异常'''  # his_abnormal_operation

    def his_abnormal_operation(self):
        try:
            self.new_find_element(*ELEMENT['历史经营异常']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史行政处罚'''  # his_administrative_punishment

    def his_administrative_punishment(self):
        try:
            self.new_find_element(*ELEMENT['历史行政处罚']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史股权出质'''  # his_equity_pledge_out

    def his_equity_pledge_out(self):
        try:
            self.new_find_element(*ELEMENT['历史股权出质']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史动产抵押'''  # his_simple_cancellation

    def his_simple_cancellation(self):
        try:
            self.new_find_element(*ELEMENT['历史动产抵押']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史行政许可'''  # his_simple_cancellation

    def his_simple_cancellation(self):
        try:
            self.new_find_element(*ELEMENT['历史行政许可']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史商标信息'''  # his_trademark_information

    def his_trademark_information(self):
        try:
            self.new_find_element(*ELEMENT['历史商标信息']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''历史网站备案'''  # his_web_record

    def his_web_record(self):
        try:
            self.new_find_element(*ELEMENT['历史网站备案']).click()
            time.sleep(1)
        except Exception as e:
            print(e)
            log.error(e)

    '''首页查公司'''

    def company_search(self, value):
        self.value = value
        try:
            self.new_find_element(*ELEMENT['查公司']).click()
            self.new_find_element(*ELEMENT['首页搜索框']).click()
            self.new_find_element(*ELEMENT['查公司—搜索页搜索框']).send_keys(self.value)
            self.new_find_element(*ELEMENT['搜索结果页第一家']).click()
            time.sleep(6)
        except:
            self.screenShot()

# if __name__ == '__main__':
#     d = Config_app().config_app()
#     o = Operation(d)
#     p = pageMethod(o)
#     p.company_search('百度')
