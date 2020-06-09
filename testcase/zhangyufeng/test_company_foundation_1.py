# -*- coding: utf-8 -*-
# @Time    : 2020-03-05 11:08
# @Author  : ZYF
# @File    : test_company_foundation_1.py
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Providers.logger import Logger
from common.MyTest import MyTest
from common.operation import Operation, getimage
from common.ReadData import Read_Ex
import unittest
from common.check_rules import *
from common.CreditIdentifier import UnifiedSocialCreditIdentifier
from Providers.account.account import Account
log = Logger("基金会").getlog()


def check_Assessment_level(value):
    """
    基金会评估等级字段校验是否正确
    :param value:展示的字段内容
    :return:成功-True，失败-False
    """
    Assessment_level = ['未参评', '1A', '2A', '3A', '4A', '5A']
    if value == "-":
        return True
    else:
        if value in Assessment_level:
            return True
        else:
            return False

def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文---基金会英文名称
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u"\u4e00" <= ch <= u"\u9fa5":
            return True
    return False

def is_all_zh(check_str):
    """
    判断字符串中是否只有中文字符
    :param check_str: 校验的字符串
    :return:只有中文返回 True，else False
    """
    if check_str == "-":
        return True
    else:
        for c in check_str:
            if not ('\u4e00' <= c <= '\u9fa5'):
                return False
            else:
                if len(check_str) >= 2:
                    return True
                return False

def check_num(str):
    """
    校验str是否为数字
    :param email: str
    :return:成功-True，失败-False
    """
    if str == "-":
        return True
    pattern = "\d+$"
    result = re.match(pattern, str)
    if result:
        return True
    else:
        return False

def check_dataSource(value):
    """
    基金会数据来源字段校验是否正确
    :param value:展示的字段内容
    :return:成功-True，失败-False
    """
    dataSource = ['年度工作报告', '基金会官网', '民政部门公告']
    if value == "-":
        return True
    else:
        if value in dataSource:
            return True
        else:
            return False

def check_scope(value):
    """
    基金会范围字段校验是否正确
    :param value:展示的字段内容
    :return:成功-True，失败-False
    """
    scope = ['地方', '全国']
    if value == "-":
        return True
    else:
        if value in scope:
            return True
        else:
            return False

def check_field(value):
    """
    基金会关注领域字段校验是否正确
    :param value:展示的字段内容
    :return:成功-True，失败-False
    """
    field = ['国际事务', '科学研究', '文化', '艺术', '儿童', '妇女', '', '三农', '教育', '青少年']
    if value == "-":
        return True
    else:
        if value in field:
            return True
        else:
            return False

def check_preferentialQualificationType(value):
    """
    基金会优惠资格类型字段校验是否正确
    :param value:展示的字段内容
    :return:成功-True，失败-False
    """
    preferentialQualificationType = ['公益性捐赠税前扣除资格', '非营利组织免税资格','公益性捐赠税前扣除资格, 非营利组织免税资格']
    if value == "-":
        return True
    else:
        if value in preferentialQualificationType:
            return True
        else:
            return False

def check_gender(value):
    """
    性别校验 男|女|'-'
    :param value: value
    :return:成功-True，失败-False
    """
    if value == "-":
        return True
    pattern = "(男|女)$"
    result = re.match(pattern, value)
    if result:
        return True
    else:
        return False

def check_funduse(value):
    """
    基金会-项目详情-资金用途 资金用途字段校验
    :param value:展示的字段内容
    :return:成功-True，失败-False
    """
    funduse = ['项目服务', '资助受益人', '资助第三方']
    if value == "-":
        return True
    else:
        if value in funduse:
            return True
        else:
            return False
def close_guide(self):
    loc = (By.ID, "com.tianyancha.skyeye:id/btn_close_guide")
    try:
        e = WebDriverWait(self.driver, 2, 0.5).until(
            EC.presence_of_element_located(loc)
        )
        e.click()
    except:
        pass


class Company_Foundation_1(MyTest, Operation):
    """基金会-企业背景"""

    a = Read_Ex()
    ELEMENT = a.read_excel("Company_foundation")

    def enter_official_information(self, company_name):
        """
        首页搜索公司名进入到公司官方信息页
        company_name : 公司名称
        :return: company_name 官方信息页
        """
        self.company_name = company_name
        self.new_find_element(By.ID, "com.tianyancha.skyeye:id/home_tab1").click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/txt_search_copy1"
        ).click()
        self.new_find_element(
            By.ID, "com.tianyancha.skyeye:id/search_input_et"
        ).send_keys(self.company_name)
        self.new_find_elements(By.ID, "com.tianyancha.skyeye:id/tv_company_name")[
            0
        ].click()
        log.info("进入公司 {} 官方信息页".format(self.company_name))

    @getimage
    def test_001_foundation_djxx_p0(self):
        """
        基金会-企业背景-登记信息
        """
        log.info(self.test_001_foundation_djxx_p0.__doc__)
        try:
            self.enter_official_information("上海文化发展基金会")
            # 进入登记信息模块
            self.new_find_element(By.XPATH, self.ELEMENT["registration"]).click()
            title_name = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(self.company_name, title_name, msg="登记信息跟所属公司不对应")
            # 获取基金会英文名称
            foundation_englishName = self.new_find_element(
                By.ID, self.ELEMENT["foundation_englishName"]
            ).text
            log.info("基金会英文名称：{}".format(foundation_englishName))
            self.assertFalse(is_contain_chinese(foundation_englishName))
            # 获取成立日期
            foundation_establish_time = self.new_find_element(
                By.ID, self.ELEMENT["foundation_establish_time"]
            ).text
            log.info("成立日期：{}".format(foundation_establish_time))
            a = check_time(foundation_establish_time, is_compare=True)
            self.assertTrue(a, msg="成立日期不符合规范")
            # 获取评估等级
            foundation_grade = self.new_find_element(
                By.ID, self.ELEMENT["foundation_grade"]
            ).text
            log.info("评估等级：{}".format(foundation_grade))
            grade = check_Assessment_level(foundation_grade)
            print(grade)
            self.assertTrue(grade)
            # 原始基数金额
            foundation_original_amount = self.new_find_element(
                By.ID, self.ELEMENT["foundation_original_amount"]
            ).text
            log.info("原始基金数额：{}".format(foundation_original_amount))
            b = is_bill_available(foundation_original_amount)
            self.assertTrue(b, msg="原始基金数额展示不符合规则")
            # 统一社会信用代码
            foundation_credit_code = self.new_find_element(
                By.ID, self.ELEMENT["foundation_credit_code"]
            ).text
            log.info("统一社会信用代码:{}".format(foundation_credit_code))
            U = UnifiedSocialCreditIdentifier()
            c = U.check_social_credit_code(foundation_credit_code)
            self.assertTrue(c, msg="统一社会信用代码-不符合规则")
            # 组织机构代码
            foundation_org_code = self.new_find_element(
                By.ID, self.ELEMENT["foundation_org_code"]
            ).text
            log.info("组织机构代码：{}".format(foundation_org_code))
            d = U.check_organization_code(foundation_org_code)
            self.assertTrue(d, msg="组织机构代码-不符合规则")
            # 业务主管单位
            foundation_business_unit = self.new_find_element(
                By.ID, self.ELEMENT["foundation_business_unit"]
            ).text
            log.info("业务主管单位:{}".format(foundation_business_unit))
            a = is_all_zh(foundation_business_unit)
            self.assertTrue(a)
            # 登记部门
            foundation_department = self.new_find_element(
                By.ID, self.ELEMENT["foundation_department"]
            ).text
            log.info("登记部门:{}".format(foundation_department))
            a = is_all_zh(foundation_department)
            self.assertTrue(a)
            # 理事长
            foundation_legal = self.new_find_element(
                By.ID, self.ELEMENT["foundation_legal"]
            ).text
            log.info("理事长:{}".format(foundation_legal))
            a = is_all_zh(foundation_legal)
            self.assertTrue(a)
            # 秘书长
            foundation_secretary = self.new_find_element(
                By.ID, self.ELEMENT["foundation_secretary"]
            ).text
            log.info("秘书长:{}".format(foundation_secretary))
            a = is_all_zh(foundation_secretary)
            self.assertTrue(a)
            # 对外联系人姓名
            foundation_contact_name = self.new_find_element(
                By.ID, self.ELEMENT["foundation_contact_name"]
            ).text
            log.info("对外联系人姓名:{}".format(foundation_contact_name))
            a = is_all_zh(foundation_contact_name)
            self.assertTrue(a)
            # 联系人职务
            foundation_contact_position = self.new_find_element(
                By.ID, self.ELEMENT["foundation_contact_position"]
            ).text
            log.info("联系人职务:{}".format(foundation_contact_position))
            a = is_all_zh(foundation_contact_position)
            self.assertTrue(a)
            # 联系人固话
            foundation_phone = self.new_find_element(
                By.ID, self.ELEMENT["foundation_phone"]
            ).text
            log.info("联系人固话:{}".format(foundation_contact_position))
            # TODO 联系人固话规则校验

            # 联系人传真
            foundation_fax = self.new_find_element(
                By.ID, self.ELEMENT["foundation_fax"]
            ).text
            log.info("联系人传真:{}".format(foundation_fax))
            # TODO 联系人传真规则校验

            # 联系人电子邮箱
            foundation_email = self.new_find_element(
                By.ID, self.ELEMENT["foundation_email"]
            ).text
            log.info("联系人电子邮箱:{}".format(foundation_email))
            a = check_email(foundation_email)
            self.assertTrue(a)
            # 负责人中国家工作人员数
            number_of_national_staff_in_charge = self.new_find_element(
                By.ID, self.ELEMENT["number_of_national_staff_in_charge"]
            ).text
            log.info("负责人中国家工作人员数:{}".format(number_of_national_staff_in_charge))
            a = check_num(number_of_national_staff_in_charge)
            self.assertTrue(a)
            self.swipeUp()
            # 负责人中担任过省部级工作人员数
            number_of_provincial = self.new_find_element(
                By.ID, self.ELEMENT["number_of_provincial"]
            ).text
            log.info("负责人中担任过省部级工作人员数:{}".format(number_of_provincial))
            a = check_num(number_of_provincial)
            self.assertTrue(a)
            # 全职员工数量
            foundation_employeeNumber = self.new_find_element(
                By.ID, self.ELEMENT["foundation_employeeNumber"]
            ).text
            log.info("全职员工数量:{}".format(foundation_employeeNumber))
            a = check_num(foundation_employeeNumber)
            self.assertTrue(a)
            # 志愿者数量
            foundation_volunteer_number = self.new_find_element(
                By.ID, self.ELEMENT["foundation_volunteer_number"]
            ).text
            log.info("志愿者数量:{}".format(foundation_volunteer_number))
            a = check_num(foundation_volunteer_number)
            self.assertTrue(a)
            # 数据来源
            data_sources = self.new_find_element(
                By.ID, self.ELEMENT["data_sources"]
            ).text
            log.info("数据来源:{}".format(data_sources))
            a = check_dataSource(data_sources)
            self.assertTrue(a)
            # 基金会范围
            foundation_scope = self.new_find_element(
                By.ID, self.ELEMENT["foundation_scope"]
            ).text
            log.info("基金会范围:{}".format(foundation_scope))
            a = check_scope(foundation_scope)
            self.assertTrue(a)
            # 关注领域
            foundation_field = self.new_find_element(
                By.ID, self.ELEMENT["foundation_field"]
            ).text
            log.info("关注领域:{}".format(foundation_field))
            a = check_field(foundation_field)
            self.assertTrue(a)
            # 专项基金数
            number_of_special_funds = self.new_find_element(
                By.ID, self.ELEMENT["number_of_special_funds"]
            ).text
            log.info("专项基金数:{}".format(number_of_special_funds))
            a = check_num(number_of_special_funds)
            self.assertTrue(a)
            # 机构官网
            foundation_website = self.new_find_element(
                By.ID, self.ELEMENT["foundation_website"]
            ).text
            log.info("机构官网:{}".format(foundation_website))
            # 基金会地址
            foundation_address = self.new_find_element(
                By.ID, self.ELEMENT["foundation_address"]
            ).text
            log.info("基金会地址:{}".format(foundation_address))
            # 邮政编码
            foundation_postal_code = self.new_find_element(
                By.ID, self.ELEMENT["foundation_postal_code"]
            ).text
            log.info("邮政编码:{}".format(foundation_postal_code))
            a = check_post_code(foundation_postal_code)
            self.assertTrue(a)
            # 宗旨
            foundation_purpose = self.new_find_element(
                By.ID, self.ELEMENT["foundation_purpose"]
            ).text
            log.info("宗旨:{}".format(foundation_purpose))
            # 业务范围
            foundation_business_scope = self.new_find_element(
                By.ID, self.ELEMENT["foundation_business_scope"]
            ).text
            log.info("业务范围:{}".format(foundation_business_scope))
            # 优惠资格类型
            qualification_type = self.new_find_element(
                By.ID, self.ELEMENT["qualification_type"]
            ).text
            log.info("优惠资格类型:{}".format(qualification_type))
            a = check_preferentialQualificationType(qualification_type)
            self.assertTrue(a)
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_002_foundation_lsh_p0(self):
        """
        基金会-企业背景-理事会
        """
        log.info(self.test_002_foundation_lsh_p0.__doc__)
        try:
            self.enter_official_information("上海文化发展基金会")
            # 获取理事会count
            count_value = self.new_find_element(
                By.XPATH, self.ELEMENT["council_count"]
            ).text
            log.info("理事会count：{}".format(count_value))
            # 进入理事会
            self.new_find_element(By.XPATH, self.ELEMENT["council"]).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(page_title, "理事会", msg="页面title不一致")
            # 姓名
            names = self.new_find_elements(By.ID, self.ELEMENT["people_name"])
            name = random.choice(names).text
            log.info("姓名：{}".format(name))
            a = is_all_zh(name)
            self.assertTrue(a)
            # 理事会职务
            council_member_positions = self.new_find_elements(
                By.ID, self.ELEMENT["council_member_position"]
            )
            council_member_position = random.choice(council_member_positions).text
            log.info("理事会职务：{}".format(council_member_position))
            a = is_all_zh(council_member_position)
            self.assertTrue(a)

            # 性别
            genders = self.new_find_elements(By.ID, self.ELEMENT["gender"])
            gender = random.choice(genders).text
            log.info("性别：{}".format(gender))
            a = check_gender(gender)
            self.assertTrue(a)
            # 年度会议次数
            meeting_counts = self.new_find_elements(
                By.ID, self.ELEMENT["meeting_count"]
            )
            meeting_count = random.choice(meeting_counts).text
            log.info("年度会议次数：{}".format(meeting_count))
            a = check_num(meeting_count)
            self.assertTrue(a)
            # 工作单位及职务
            comp_positions = self.new_find_elements(
                By.ID, self.ELEMENT["comp_position"]
            )
            comp_position = random.choice(comp_positions).text
            log.info("工作单位及职务：{}".format(comp_position))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_003_foundation_jsh_p0(self):
        """
        基金会-企业背景-监事会
        """
        log.info(self.test_003_foundation_jsh_p0.__doc__)
        try:
            self.enter_official_information("上海文化发展基金会")
            # 获取理事会count
            count_value = self.new_find_element(
                By.XPATH, self.ELEMENT["supervisors_count"]
            ).text
            log.info("监事会count：{}".format(count_value))
            # 进入监事会
            self.new_find_element(By.XPATH, self.ELEMENT["supervisors"]).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(page_title, "监事会", msg="页面title不一致")
            # 姓名
            supervisor_member_names = self.new_find_elements(
                By.ID, self.ELEMENT["supervisor_member_name"]
            )
            supervisor_member_name = random.choice(supervisor_member_names).text
            log.info("姓名：{}".format(supervisor_member_name))
            a = is_all_zh(supervisor_member_name)
            self.assertTrue(a)
            # 性别
            supervisor_member_genders = self.new_find_elements(
                By.ID, self.ELEMENT["supervisor_member_gender"]
            )
            supervisor_member_gender = random.choice(supervisor_member_genders).text
            log.info("性别：{}".format(supervisor_member_gender))
            a = check_gender(supervisor_member_gender)
            self.assertTrue(a)
            # 年度会议次数
            supervisor_member_meeting_counts = self.new_find_elements(
                By.ID, self.ELEMENT["supervisor_member_meeting_count"]
            )
            supervisor_member_meeting_count = random.choice(
                supervisor_member_meeting_counts
            ).text
            log.info("年度会议次数：{}".format(supervisor_member_meeting_count))
            a = check_num(supervisor_member_meeting_count)
            self.assertTrue(a)
            # 工作单位及职务
            supervisor_comp_positions = self.new_find_elements(
                By.ID, self.ELEMENT["supervisor_comp_position"]
            )
            supervisor_comp_position = random.choice(supervisor_comp_positions).text
            log.info("工作单位及职务：{}".format(supervisor_comp_position))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_004_foundation_xmxx_p0(self):
        """
        基金会-企业背景-项目信息
        """
        log.info(self.test_004_foundation_xmxx_p0.__doc__)
        try:
            self.enter_official_information("上海文化发展基金会")
            self.swipeUp(x1=0.5, y1=0.85, y2=0.65, t=500)
            # 获取项目信息count
            project_count = self.new_find_element(
                By.XPATH, self.ELEMENT["project_count"]
            ).text
            log.info("项目信息count：{}".format(project_count))
            # 进入项目信息
            self.new_find_element(By.XPATH, self.ELEMENT["project"]).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(page_title, "项目信息", msg="页面title不一致")
            # 项目标题
            item_headers = self.new_find_elements(By.ID, self.ELEMENT["item_header"])
            item_header = random.choice(item_headers)
            item_name = item_header.text
            log.info("项目标题：{}".format(item_name))
            # 年度收入（万元）
            item_content1s = self.new_find_elements(
                By.ID, self.ELEMENT["item_content1"]
            )
            item_content1 = random.choice(item_content1s).text
            log.info("年度收入（万元）：{}".format(item_content1))
            a = check_num(item_content1)
            self.assertTrue(a)
            # 年度支出（万元）
            item_content2s = self.new_find_elements(
                By.ID, self.ELEMENT["item_content2"]
            )
            item_content2 = random.choice(item_content2s).text
            log.info("年度支出（万元）：{}".format(item_content2))
            a = check_num(item_content2)
            self.assertTrue(a)
            # 关注领域
            item_content3s = self.new_find_elements(
                By.ID, self.ELEMENT["item_content3"]
            )
            item_content3 = random.choice(item_content3s).text
            log.info("关注领域：{}".format(item_content3))
            # 随机点击项目信息，页面跳转项目详情页
            item_header.click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(page_title, "项目详情", msg="页面title不一致")
            # 基本信息
            # 项目名称
            project_name = self.new_find_element(
                By.ID, self.ELEMENT["project_name"]
            ).text
            log.info("项目名称：{}".format(project_name))
            self.assertEqual(project_name, item_name)
            # 执行年度
            detail_year = self.new_find_element(By.ID, self.ELEMENT["detail_year"]).text
            log.info("执行年度：{}".format(detail_year))
            # todo 执行年度校验

            # 年度收入（万元）
            detail_income = self.new_find_element(
                By.ID, self.ELEMENT["detail_income"]
            ).text
            log.info("年度收入（万元）：{}".format(detail_income))
            a = check_num(detail_income)
            self.assertTrue(a)
            # 年度支出（万元）
            detail_expenditure = self.new_find_element(
                By.ID, self.ELEMENT["detail_expenditure"]
            ).text
            log.info("年度支出（万元）：{}".format(detail_expenditure))
            a = check_num(detail_expenditure)
            self.assertTrue(a)
            # 关注领域
            detail_field = self.new_find_element(
                By.ID, self.ELEMENT["detail_field"]
            ).text
            log.info("关注领域：{}".format(detail_field))
            # 覆盖地域
            detail_region = self.new_find_element(
                By.ID, self.ELEMENT["detail_region"]
            ).text
            log.info("关注领域：{}".format(detail_region))
            a = is_all_zh(detail_region)
            self.assertTrue(a)
            # 资金用途
            detail_fund_use = self.new_find_element(
                By.ID, self.ELEMENT["detail_fund_use"]
            ).text
            log.info("关注领域：{}".format(detail_fund_use))
            a = check_funduse(detail_fund_use)
            self.assertTrue(a)
            # 受益群体
            detail_group = self.new_find_element(
                By.ID, self.ELEMENT["detail_group"]
            ).text
            log.info("受益群体：{}".format(detail_group))
            # 项目简介
            detail_overview = self.new_find_element(
                By.ID, self.ELEMENT["detail_overview"]
            ).text
            log.info("项目简介：{}".format(detail_overview))
            # TODO 项目简介规则校验

            # 大额支付对象
            no_data = self.new_find_element(By.ID, self.ELEMENT["no_data"]).text
            log.info("大额支付对象：{}".format(no_data))
            # TODO 大额支付对象规则校验

        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_005_foundation_cwxx_p0(self):
        """
        基金会-企业背景-财务信息
        """
        log.info(self.test_005_foundation_cwxx_p0.__doc__)
        try:
            self.enter_official_information("上海文化发展基金会")
            self.swipeUp(x1=0.5, y1=0.85, y2=0.65, t=500)
            # 获取财务信息count
            financial_information_count = self.new_find_element(
                By.XPATH, self.ELEMENT["financial_information_count"]
            ).text
            log.info("项目信息count：{}".format(financial_information_count))
            # 进入财务信息
            self.new_find_element(
                By.XPATH, self.ELEMENT["financial_information"]
            ).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(page_title, "财务信息", msg="页面title不一致")
            # 进行年度筛选
            self.new_find_element(By.XPATH, self.ELEMENT["screening"]).click()
            screeningS = self.new_find_elements(By.XPATH, self.ELEMENT["screeningS"])
            screening = random.choice(screeningS)
            screening_value = screening.text
            log.info("选择筛选时间：{}".format(screening_value))
            screening.click()
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_006_foundation_cwnd_p0(self):
        """
        基金会-企业背景-财务年度
        """
        log.info(self.test_006_foundation_cwnd_p0.__doc__)
        try:
            self.enter_official_information("上海文化发展基金会")
            self.swipeUp(x1=0.5, y1=0.85, y2=0.65, t=500)
            # 获取财务年度count
            financial_year_count = self.new_find_element(
                By.XPATH, self.ELEMENT["financial_year_count"]
            ).text
            log.info("财务年度count：{}".format(financial_year_count))
            # 进入财务年度
            self.new_find_element(By.XPATH, self.ELEMENT["financial_year"]).click()
            financial_year_items = self.new_find_elements(By.ID, self.ELEMENT["financial_year_item"])
            num = len(financial_year_items)
            log.info('财务年度页item数量：{}'.format(num))
            self.assertEqual(num, int(financial_year_count))
            # 随机进入一个item
            financial_year_item = random.choice(financial_year_items)
            item_text = financial_year_item.text
            financial_year_item.click()
            # 进入到对应年度的详情页
            page_title = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(page_title, item_text, msg="页面title不一致")
            # 财务概况-字段展示
            # 净资产
            financial_situation_net_assets = self.new_find_element(By.ID, self.ELEMENT[
                "financial_situation_net_assets"]).text
            log.info("净资产：{}".format(financial_situation_net_assets))
            # 年度总收入
            financial_situation_annual_income = self.new_find_element(By.ID, self.ELEMENT[
                "financial_situation_annual_income"]).text
            log.info("年度总收入：{}".format(financial_situation_annual_income))
            # 年度总支出
            financial_situation_annual_expenditure = self.new_find_element(By.ID, self.ELEMENT[
                "financial_situation_annual_expenditure"]).text
            log.info("年度总支出：{}".format(financial_situation_annual_expenditure))
            # 资产负债表
            balance_sheet_group_more = self.new_find_element(By.ID, self.ELEMENT[
                "balance_sheet_group_more"]).text
            log.info("资产负债表：{}".format(balance_sheet_group_more))
            # 业务活动表
            buniness_group_more = self.new_find_element(By.ID, self.ELEMENT[
                "buniness_group_more"]).text
            log.info("业务活动表：{}".format(buniness_group_more))
            # 大额捐赠信息
            largedonation_group_more = self.new_find_element(By.ID, self.ELEMENT[
                "largedonation_group_more"]).text
            log.info("大额捐赠信息：{}".format(largedonation_group_more))
            # 委托理财去情况
            entrust_group_more = self.new_find_element(By.ID, self.ELEMENT[
                "entrust_group_more"]).text
            log.info("委托理财去情况：{}".format(entrust_group_more))
            # 点击「更多」按钮，页面跳转财务概况详情页
            self.new_find_element(By.ID, self.ELEMENT["item_overview_group_more"]).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(page_title, "财务概况详情", msg="页面title不一致")
            # 财务概况详情页展示
            # tv_title
            tv_title = self.new_find_element(By.ID, self.ELEMENT["tv_title"]).text
            log.info("财务概况详情页tv_title：{}".format(tv_title))
            # 净资产
            financial_situation_net_assets1 = self.new_find_element(By.ID, self.ELEMENT[
                "financial_situation_net_assets"]).text
            log.info("净资产：{}".format(financial_situation_net_assets1))
            self.assertEqual(financial_situation_net_assets1, financial_situation_net_assets)
            # 年度总收入
            financial_situation_annual_income1 = self.new_find_element(By.ID, self.ELEMENT[
                "financial_situation_annual_income"]).text
            log.info("年度总收入：{}".format(financial_situation_annual_income1))
            self.assertEqual(financial_situation_annual_income1, financial_situation_annual_income)
            # 投资收入
            situation_invest_income = self.new_find_element(By.ID, self.ELEMENT["situation_invest_income"]).text
            log.info("投资收入：{}".format(situation_invest_income))
            # 服务收入
            situation_service_income = self.new_find_element(By.ID, self.ELEMENT["situation_service_income"]).text
            log.info("服务收入：{}".format(situation_service_income))
            # 政府补贴收入
            situation_government_grants_income = self.new_find_element(By.ID, self.ELEMENT[
                "situation_government_grants_income"]).text
            log.info("政府补贴收入：{}".format(situation_government_grants_income))
            # 其他收入
            situation_other_income = self.new_find_element(By.ID, self.ELEMENT["situation_other_income"]).text
            log.info("其他收入：{}".format(situation_other_income))
            # 捐赠收入
            situation_donation_income = self.new_find_element(By.ID, self.ELEMENT["situation_donation_income"]).text
            log.info("捐赠收入：{}".format(situation_donation_income))
            # 年度总支出
            financial_situation_annual_expenditure1 = self.new_find_element(By.ID, self.ELEMENT[
                "financial_situation_annual_expenditure"]).text
            log.info("年度总支出：{}".format(financial_situation_annual_expenditure1))
            self.assertEqual(financial_situation_annual_expenditure1, financial_situation_annual_expenditure)
            # 用于公益事业的支出
            situation_public_welfare_expenditure = self.new_find_element(By.ID, self.ELEMENT[
                "situation_public_welfare_expenditure"]).text
            log.info("用于公益事业的支出：{}".format(situation_public_welfare_expenditure))
            # 工作人员工资福利支出
            situation_wages_expenditure = self.new_find_element(By.ID, self.ELEMENT["situation_wages_expenditure"]).text
            log.info("工作人员工资福利支出：{}".format(situation_wages_expenditure))
            # 行政办公支出
            situation_administration_expenditure = self.new_find_element(By.ID, self.ELEMENT[
                "situation_administration_expenditure"]).text
            log.info("行政办公支出：{}".format(situation_administration_expenditure))
            # 其他支出
            situation_other_expenditure = self.new_find_element(By.ID, self.ELEMENT["situation_other_expenditure"]).text
            log.info("其他支出：{}".format(situation_other_expenditure))
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception

    @getimage
    def test_007_foundation_dwtz_p0(self):
        """
        基金会-企业背景-对外投资
        """
        log.info(self.test_007_foundation_dwtz_p0.__doc__)
        try:
            # vip 账号登录登录
            account = Account()
            acc_vip_name = account.get_account('vip')
            acc_pwd = account.get_pwd()
            log.info("登录VIP账号：".format(acc_vip_name))
            self.login(acc_vip_name, acc_pwd)
            self.enter_official_information("上海文化发展基金会")
            self.swipeUp(x1=0.5, y1=0.85, y2=0.65, t=500)
            # 获取对外投资count
            foreign_investment_count = self.new_find_element(
                By.XPATH, self.ELEMENT["foreign_investment_count"]
            ).text
            log.info("对外投资count：{}".format(foreign_investment_count))
            # 进入对外投资
            self.new_find_element(By.XPATH, self.ELEMENT["foreign_investment"]).click()
            page_title = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(page_title, "对外投资", msg="页面title不一致")
            # 存长图
            save_long_figure = self.new_find_element(By.XPATH, self.ELEMENT["save_long_figure"])
            self.assertIsNotNone(save_long_figure)
            # 分享
            share = self.new_find_element(By.XPATH, self.ELEMENT["share"])
            self.assertIsNotNone(share)
            # 对外投资页-页面字段展示
            # 公司名称
            outinvest_company_name = self.new_find_elements(By.ID, self.ELEMENT["outinvest_company_name"])[1].text
            log.info("公司名称：{}".format(outinvest_company_name))
            # 法定代表人
            outinvest_legal = self.new_find_elements(By.ID, self.ELEMENT["outinvest_legal"])[1].text
            log.info("法定代表人：{}".format(outinvest_legal))
            # 经营状态
            outinvest_reg_capital = self.new_find_elements(By.ID, self.ELEMENT["outinvest_reg_capital"])[1].text
            log.info("经营状态：{}".format(outinvest_reg_capital))
            a = operating_check(1, outinvest_reg_capital)
            self.assertTrue(a)
            # 投资数额
            outinvest_amount = self.new_find_elements(By.ID, self.ELEMENT["outinvest_amount"])[1].text
            log.info("投资数额：{}".format(outinvest_amount))
            a = is_bill_available(outinvest_amount)
            self.assertTrue(a)
            # 投资比例
            outinvest_ratio = self.new_find_elements(By.ID, self.ELEMENT["outinvest_ratio"])[1].text
            log.info("投资比例：{}".format(outinvest_ratio))
            a = is_percentage_available(outinvest_ratio)
            self.assertTrue(a)
            # 成立日期
            outinverst_date = self.new_find_elements(By.ID, self.ELEMENT["outinverst_date"])[1].text
            log.info("成立日期：{}".format(outinverst_date))
            a = check_time(outinverst_date)
            self.assertTrue(a)
            # 公司的跳转
            self.new_find_elements(By.ID, self.ELEMENT["outinvest_company_name"])[1].click()
            comp_name = self.new_find_element(By.ID, self.ELEMENT["comp_name"]).text
            log.info("页面跳转后公司详情页name:{}".format(comp_name))
            self.assertEqual(comp_name, outinvest_company_name)
            self.driver.keyevent(4)
            # 人的跳转
            self.new_find_elements(By.ID, self.ELEMENT["outinvest_legal"])[1].click()
            close_guide(self)
            person_name = self.new_find_element(By.ID, self.ELEMENT["person_name"]).text
            # self.assertEqual(person_name, outinvest_legal)
            self.assertIn(outinvest_legal, person_name)
            self.driver.keyevent(4)
            # 股权机构的跳转
            self.new_find_elements(By.ID, self.ELEMENT["outinvest_title_right"])[1].click()
            title_name = self.new_find_element(By.ID, self.ELEMENT["title_name"]).text
            self.assertEqual(title_name, '股权结构')
            self.driver.keyevent(4)
            # 对外投资页count
            comp_count = self.all_count_compute_v1(By.ID, self.ELEMENT["outinvest_company_name"])
            log.info("对外投资页item展示数量：{}".format(comp_count))
            self.assertEqual(comp_count, int(foreign_investment_count))
            account.release_account(acc_vip_name, "vip")
        except AssertionError:
            raise self.failureException()
        except Exception as e:
            log.error(e)
            raise Exception


if __name__ == "__main__":
    unittest.main()

# try:
#
# except AssertionError:
#     raise self.failureException()
# except Exception as e:
#     log.error(e)
#     raise Exception
