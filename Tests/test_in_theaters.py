import pytest
import requests
from Untils.commonlib import get_test_data
import pprint

cases, list_params = get_test_data("/Users/gilbert/PycharmProjects/pytest_api/Data/test_in_theaters.yaml")


@pytest.fixture(scope='session')
def preparation():
    print("在数据库中准备测试数据")
    test_data = "在数据库中准备测试数据"
    yield test_data
    print("清理测试数据")


class TestInTheaters(object):

    @pytest.mark.parametrize('case, http, expected', list(list_params), ids=cases)
    def test_in_theaters(self, env, case, http, expected):
        res = requests.request(http['method'],
                               url=env['host']['douban'] + http['path'],
                               headers=http['headers'],
                               params=http['params'])
        response = res.json()
        pprint.pprint(response)
        assert response['data'][0]['url'] == expected['response']['url']
        assert response['data'][0]['rate'] == expected['response']['rate']
        assert response['data'][0]['title'] == expected['response']['title'], "实际的电影是：{}".format(response['title'])
