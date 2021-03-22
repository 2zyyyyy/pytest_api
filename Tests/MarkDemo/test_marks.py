import sys
import pytest
import allure

"""
标记与分组
通过 pytest.mark 可以给测试用例打上标记，常见的应用场景是：针对某些还未实现的功能，
将测试用例主动跳过不执行。或者在某些条件下，测试用例跳过不执行。还有可以主动将测试用
例标记为失败等等。针对三个场景，pytest 提供了内置的标签
"""


@allure.feature("pytest标记与分组")
class TestMarks(object):
    # 自定义标签,运行时可以通过-m 标签名称过滤或者反过滤 py.test -m "tag" or "not tag" 运行会有警告 需要到pytest.ini文件注册标签
    @pytest.mark.tag
    def test_tag(self):
        """
        自定义标签：tag
        """
        assert 0

    @pytest.mark.skip(reason="not implementation")
    def test_the_unknow(self):
        """
        跳过不执行，逻辑暂未实现
        """
        assert 0

    @pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
    def test_skipif(self):
        """
        低于Python3.7版本不执行这条测试用例
        """
        assert 1

    @pytest.mark.xfail
    def test_xfail(self):
        """
        Indicate that you expect it to fail
        这条用例失败时，测试结果被标记为xfail（expected to fail），并且不打印错误信息。
        这条用例执行成功时，测试结果被标记为xpassed（unexpectedly passing）
        """
        assert 0

    @pytest.mark.xfail(run=False)
    def test_xfail_not_run(self):
        """
        run=False表示这条用例不执行
        """
        assert 0
