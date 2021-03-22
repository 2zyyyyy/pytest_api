import pytest
import requests
from Tests.Macwk.test_in_macsofts import login
from Untils.commonlib import get_test_data
import sys
import logging
import allure

path = sys.path[0] + "/Data/Douban/test_in_theaters.yaml"
cases, list_params = get_test_data(path)


# @pytest.fixture(scope='function')
# 模拟一个准备和清理测试数据的 fixture 函数 preparation，scope 设置为 function
# def preparation():
#     print("在数据库中准备测试数据")
#     test_data = "在数据库中准备测试数据"
#     yield test_data
#     print("清理测试数据")

@allure.feature("豆瓣")
class TestInTheaters(object):

    @allure.story("电影分类查询")
    @allure.severity("BLOCKER")
    @pytest.mark.parametrize('case, http, expected', list(list_params), ids=cases)
    def test_in_theaters(self, env, case, http, expected):
        login("douban", "123456~")
        allure.attach("发起请求...")
        res = requests.request(http['method'],
                               url=env['host']['douban'] + http['path'],
                               headers=http['headers'],
                               params=http['params'])
        with allure.step("获取返回结果"):
            response = res.json()
            logging.info(response)
        assert response['data'][0]['url'] == expected['response']['url']
        assert response['data'][0]['rate'] == expected['response']['rate']
        assert response['data'][0]['title'] == expected['response']['title'], \
            "实际的电影是：{}".format(response['data'][0]['title'])
