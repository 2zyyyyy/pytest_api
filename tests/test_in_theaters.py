import requests
import pprint
import yaml


def get_test_data(test_data_path):
    cases = []
    http = []
    expected = []

    with open(test_data_path) as f:
        data = yaml.load(f.read(), Loader=yaml.SafeLoader)
        test_data = data['tests']
        for td in test_data:
            cases.append(td.get('case', ''))
            http.append(td.get('http', {}))
            expected.append(td.get('expected', {}))
    parameters = zip(cases, http, expected)
    return case, parameters


case, parameter = get_test_data("/Users/Tony/PycharmProjects/pytest_api/data/test_in_theaters.yaml")
list_params = list(parameter)


class TestInTheaters(object):

    def test_in_theaters(self):
        host = "http://api.douban.com"
        res = requests.request(list_params[0][1]['method'],
                               url=host + list_params[0][1]['path'],
                               headers=list_params[0][1]['headers'],
                               params=list_params[0][1]['params'])
        response = res.json()
        # pprint.pprint("res:" + str(response['total']))
        assert response['count'] == list_params[0][2]['response']['count']
        assert response['start'] == list_params[0][2]['response']['start']
        assert response['total'] == len(response['subjects'])
        assert response['title'] == list_params[0][2]['response']['title'], "实际的标题是：{}".format(response['title'])
