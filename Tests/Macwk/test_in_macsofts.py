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
    @allure.story("Mac商店应用查询接口测试")  # allure.store:场景
    @pytest.mark.parametrize('case, http, expected', list(list_params), ids=cases)
    def test_in_macsofts(self, env, case, http, expected):
        # 步骤1：调用step函数
        login("wanli", "dingtax.cn")
        # 步骤2：step的参数打印在测试报告中
        with allure.step("准备发起请求"):
            allure.attach("attach可以打印一些附加信息~")
            allure.attach("请求方式：", http['method'], "请求地址：", env['host']['macwk'] + http['path'])
            allure.attach("请求参数：", http['params'])
        with allure.step("装载数据,发起请求"):
            res = requests.request(http['method'],
                                   url=env['host']['macwk'] + http['path'],
                                   headers=http['headers'],
                                   params=http['params'])
        with allure.step("获取返回结果"):
            response = res.json()
            allure.attach("log 输出返回结果数据")
            logging.info(response)
        with allure.step("断言"):
            assert response['data'][0]['language'][0] == expected['response']['language']
            assert response['data'][0]['title'] == expected['response']['title'], \
                "实际的名称是：{}".format(response['data'][0]['title'])

    @allure.story("商店详情接口测试")
    def test_macsofts_details(self):
        pass

    @pytest.mark.skip(reason="跳过本次执行")
    @allure.story("下载应用")
    def test_download(self):
        pass


@allure.step('Login')
# 将函数作为一个步骤，调用该函数，测试报告中将会输出该步骤（称为step函数）
def login(usr, pwd):
    logging.info(usr, pwd)
