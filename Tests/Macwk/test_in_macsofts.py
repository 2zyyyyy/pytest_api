import pytest
import requests
from Untils.commonlib import get_test_data
import sys
import logging
import allure

path = sys.path[0] + "/Data/Macwk/test_in_macsofts.yaml"
cases, list_params = get_test_data(path)


@allure.feature("Mac软件商店")  # allure.feature:产品需求
class TestInMacsofts(object):
    @allure.story("Mac商店应用查询接口测试")  # allure.store:针对产品需求的实际测试场景
    @allure.severity(allure.severity_level.NORMAL)  # allure.severity:标记测试用例级别
    @allure.issue("www.google.com", name="搜索")
    @allure.testcase("www.testcase.com")
    @pytest.mark.parametrize('case, http, expected', list(list_params), ids=cases)
    def test_in_macsofts(self, env, case, http, expected):
        """
        描述信息
        :param env:环境
        :param case:测试用例
        :param http:接口请求地址
        :param expected:期望结果
        :return:pass
        """
        # 步骤1：调用step函数
        login("wanli", "dingtax.cn")
        # 步骤2：step的参数打印在测试报告中
        with allure.step("准备发起请求"):
            allure.attach(http['method'])
            allure.attach(env['host']['macwk'], http['path'])
            # allure.attach("请求参数：", http['params'])
        with allure.step("装载数据,发起请求"):
            res = requests.request(http['method'], url=env['host']['macwk'] + http['path'],
                                   headers=http['headers'], params=http['params'])
        with allure.step("获取返回结果"):
            response = res.json()
        allure.attach("log输出返回结果数据")
        logging.info(response)

        with allure.step("断言"):
            assert response['data'][0]['language'][0] == expected['response']['language']
        assert response['data'][0]['title'] == expected['response']['title'], \
            "实际的名称是：{}".format(response['data'][0]['title'])


@allure.story("商店详情接口测试")
@allure.severity(allure.severity_level.BLOCKER)
def test_macsofts_details():
    pass


@allure.severity(allure.severity_level.MINOR)
@pytest.mark.skip(reason="跳过本次执行")
@allure.story("下载应用")
def test_download():
    pass


@allure.step('Login')
# 将函数作为一个步骤，调用该函数，测试报告中将会输出该步骤（称为step函数）
def login(usr, pwd):
    logging.info(usr, pwd)
