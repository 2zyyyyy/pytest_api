import pytest
import requests
from Untils.commonlib import get_test_data
import pprint
import sys

path = sys.path[0] + "/Data/Macwk/test_in_macsofts.yaml"
cases, list_params = get_test_data(path)


@pytest.fixture(scope='session')
def preparation():
    print("在数据库中准备测试数据")
    test_data = "在数据库中准备测试数据"
    yield test_data
    print("清理测试数据")


class TestInMacsofts(object):

    @pytest.mark.parametrize('case, http, expected', list(list_params), ids=cases)
    def test_in_theaters(self, env, case, http, expected):
        res = requests.request(http['method'],
                               url=env['host']['macwk'] + http['path'],
                               headers=http['headers'],
                               params=http['params'])
        response = res.json()
        pprint.pprint(response)
        assert response['data'][0]['language'][0] == expected['response']['language']
        assert response['data'][0]['title'] == expected['response']['title'], \
            "实际的名称是：{}".format(response['data'][0]['title'])
