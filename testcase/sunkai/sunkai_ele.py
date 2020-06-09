# -*- coding: utf-8 -*-
# # @Time    : 2020-06-01 10:52
# # @Author  : sunkai
# # @Email   : sunkai@tianyancha.com
# # @File    : sunkai_ele.py
# # @Software: PyCharm

elements = {
    'banner': 'com.tianyancha.skyeye:id/sdv_banner',
    'title': 'com.tianyancha.skyeye:id/app_title_name',
    'search_button': "//*[@text='天眼一下']",
    'default_result': "//*[@text='北京赚他一个亿网络科技有限公司']",
    'city': "//*[contains(@text, '城市')]/../../android.view.View[2]",
    'hot_city': "//*[@resource-id='_precheck_city']/android.view.View[3]/android.view.View",
    'city_search': "android.widget.EditText",
    'city_search_input': "//*[@resource-id='_city_input']",
    'city_search_result': "//*[@resource-id='_precheck_city_search']/android.view.View",
    'name_input': "//*[contains(@text, '字号')]/../../android.view.View[2]/android.widget.EditText",
    'name_input_one_key_clear': "//*[contains(@text, '字号')]/../../android.view.View[2]/android.view.View",
    'industry_select': "//*[contains(@text, '行业')]/../../android.view.View[2]",
    'assert_industry_page': "//*[@text='选择行业']",
    'every_industry': "//*[@text='{}']",
    'company_friend_style': "//*[@text='合伙公司']",
    'friend_company_result': "//*[@text='北京赚他一个亿网络科技合伙公司']",
    'sensitive_words_toast': "//*[contains(@text, '敏感词')]",
    'friendship_tips': "//*[contains(@text, '出现了特殊词语')]",
    'name_no_chinese_toast': "//*[contains(@text, '支持汉字')]",
    'in_china': "//*[@text='在全国']",
    'in_city': "//*[@text='在全国']/../../android.view.View[2]",
    'name_same': "//*[contains(@text, '字号相同')]",
    'name_like': "//*[contains(@text, '字号相似')]",
    'name_read_same': "//*[contains(@text, '字号读音')]",
    'trademark_register': "//*[contains(@text, '注册了')]",
    'company_item': "//*[contains(@text,'有限公司') and @index='6']",
    'company_detail_mark': "com.tianyancha.skyeye:id/radio_firm_detail",
    'no_result': "//*[@text='没有与您检测的名称相同或相似的公司']",
    'name_same_all_result': "//*[contains(@text,'字号相同')]/../following-sibling::android.view.View[3]",
    'name_like_all_result': "//*[contains(@text,'字号相似')]/../following-sibling::android.view.View[3]",
    'name_read_same_all_result': "//*[contains(@text,'字号读音')]/../following-sibling::android.view.View[3]",
    'trademark_register_all_result': "//*[contains(@text,'注册了')]/../following-sibling::android.view.View[3]",
    'all_results_all_items': "android.view.View",
    'want_register_company_banner': "//*[@text='app_reminder_banner']",
    'tyc-service_buy_title': "com.tianyancha.skyeye:id/app_title_name",
    'page_bottom_banner_company_register': "//*[@text='app_company_register']",
    'page_bottom_banner_address_register': "//*[@text='app_company_location_register']",
    'page_bottom_banner_bank_open': "//*[@text='app_bank_account']",
    'country_name_like_count': "//*[contains(@text, '字号相似')]/../android.view.View[2]",
    'country_read_same_count': "//*[contains(@text, '字号读音')]/../android.view.View[2]",
    'country_name_Like_items': "//*[contains(@text, '字号相似')]/following-sibling::android.view.View",
    'country_read_same_items': "//*[contains(@text, '字号读音')]/following-sibling::android.view.View",
    'all_style': "//*[@resource-id='com.tianyancha.skyeye:id/tv_name' and @text='全部']",
    'company_name_check_in_all': "//*[@text='企业核名']"
}
