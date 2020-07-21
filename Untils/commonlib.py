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
    return cases, parameters
