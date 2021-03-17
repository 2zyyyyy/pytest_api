import os

import pytest
import yaml

'''
pytest_addoption Hook函数，可以接受命令行选项的参数
pytest_addoption 的含义是，接收命令行选项--env 选项的值，存到 environment 变量中，如果不指定命令行选项，
environment 变量默认值是 test。将上面代码也放入 conftest.py 中，并修改 env 函数，将 os.path.join 中的
"test"替换为 request.config.getoption("environment")，这样就可以通过命令行选项来控制读取的配置文件了。
比如执行 test 环境的测试，可以指定--env test：
'''


def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     dest="environment",
                     default="test",
                     help="environment: test or prod")


@pytest.fixture(scope="session")
def env(request):
    # request.config.rootdir表示pytest.ini配置文件所在的目录
    config_path = os.path.join(request.config.rootdir,
                               "Config",
                               request.config.getoption('environment'),
                               "config.yaml")
    with open(config_path) as f:
        env_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    return env_config
