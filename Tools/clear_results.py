# -*- coding:utf-8 -*-

import os
from Config.conf import ALLURE_RESULTS
import sys

sys.path.append('.')


def clear_allure_results():
    var = True
    for i in os.listdir(ALLURE_RESULTS):
        new_path = os.path.join(ALLURE_RESULTS, i)
        if os.path.isfile(new_path):
            os.remove(new_path)
            print("删除{}成功!".format(new_path))
            var = False
        if var:
            print("暂无数据可以清理!")


if __name__ == '__main__':
    clear_allure_results()
