Pytest使用allure生成测试报告

[TOC]

### 1.Allure测试报告介绍

​	[Allure](http://allure.qatools.ru/)是一款轻量级并且非常灵活的开源测试报告框架。 它支持绝大多数测试框架， 例如TestNG、Pytest、JUint等。它简单易用，易于集成。

### 2. 第三方库安装

#### 2.1 Pytest相关

- Pytest
  - Pytest测试框架，类似Unittest、TestNG;
    - `$ pip install pytest`
- Requests
  - 本文以 API 自动化测试为例，因此需要安装HTTP 的 client 包 requests;
    - `$ pip install requests`
- PyYAML
  - 测试数据存放在YAML文件中，读取 Yaml 文件，需要安装 PyYAML 包;
    - `$ pip install PyYaml`

#### 2.2 Allure相关

- Allure
  - macOS `$ brew install allure`

- Allure-Pytest
  - Allure Pytest Plugin
    - `$ pip install allure-pytest`

### 3. Pytest命名规则

​	Pytest 会在 `test_*.py` 或者 `*test.py` 文件中，寻找 class 外边的 test开头的函数，或者 Test 开头的 class 里面的 test_开头的方法，将这些函数和方法作为测试用例来管理。

- 文件
  - 文件以`test_`开头（或` _test`结尾）
  - 例：【`test_login.py`】或者【`login_test.py`】
- 类
  - 类以Test开头，且不能带有init方法
  - 例：【`Test_xxx`】【注意：不能带有init方法】
- 函数（方法）
  - 函数以`test_`开头
  - 例：【`test_login`】

#### 3.1 查看收集到的测试用例

​	我们可以通过`$ py.test --collect-only`命令，查看Pytes收集到的测试用例

```shell
=============================  test session starts ============================
platform darwin -- Python 3.8.4, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
rootdir: /Users/gilbert/PycharmProjects/pytest_api, inifile: pytest.ini
plugins: allure-pytest-2.8.36
collected 8 items
<Package /Users/gilbert/PycharmProjects/pytest_api/Tests>
  <Module test_marks.py>
    <Class TestMarks>
        <Function test_tag>
        <Function test_the_unknow>
        <Function test_skipif>
        <Function test_xfail>
        <Function test_xfail_not_run>
<Package /Users/gilbert/PycharmProjects/pytest_api/Tests/Douban>
  <Module test_in_theaters.py>
    <Class TestInTheaters>
        <Function test_in_theaters[验证响应中title和rate与请求中的参数一致]>
        <Function test_in_theaters[验证响应中第一条数据的title是"二十二"]>
<Package /Users/gilbert/PycharmProjects/pytest_api/Tests/Macwk>
  <Module test_in_macsofts.py>
    <Class TestInMacsofts>
        <Function test_in_macsofts[验证响应中title和language与预期结果一致]>
============================= no tests ran in 0.19s ===========================
```

#### 3.2 执行测试用例

​	在测试项目的目录下执行`$ py.test Tests/ `命令,如果想看明细的需要使用`$ py.test Test/ -v -s`命令

```shell
 ~/PycharmProjects/pytest_api master ±✚  py.test -v -s
================================ test session starts ============================
platform darwin -- Python 3.8.4, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /usr/local/bin/python3.8
cachedir: .pytest_cache
rootdir: /Users/gilbert/PycharmProjects/pytest_api, inifile: pytest.ini
plugins: allure-pytest-2.8.36
collected 8 items

Tests/test_marks.py::TestMarks::test_tag PASSED
Tests/test_marks.py::TestMarks::test_the_unknow SKIPPED
Tests/test_marks.py::TestMarks::test_skipif PASSED
Tests/test_marks.py::TestMarks::test_xfail XFAIL
Tests/test_marks.py::TestMarks::test_xfail_not_run XFAIL
Tests/Douban/test_in_theaters.py::TestInTheaters::test_in_theaters[验证响应中title和rate与请求中的参数一致] PASSED
Tests/Douban/test_in_theaters.py::TestInTheaters::test_in_theaters[验证响应中第一条数据的title是"二十二"] PASSED
Tests/Macwk/test_in_macsofts.py::TestInMacsofts::test_in_macsofts[验证响应中title和language与预期结果一致] PASSED

====================5 passed, 1 skipped, 2 xfailed in 1.32s======================
```



这边列举一些常用的执行测试用例的命令

<center>表1-1 Pytest常用测试命令</center>

| 命令                                  | 说明                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| `$ py.test`                           | *run all tests below current dir*                            |
| `$ py.test test_module.py`            | *run tests in module*                                        |
| `$ py.test somepath`                  | *run all tests below somepath*                               |
| `$ py.test -k stringexpr`             | *only run tests with names that match the*<br/>the "string expression", e.g. "MyClass and not method"*<br/>*will select TestMyClass.test_something*<br/>*but not TestMyClass.test_method_simple* |
| `$ py.test test_module.py::test_func` | *only run tests that match the "node ID",*<br/>*e.g "test_mod.py::test_func" will select*<br/>*only test_func in test_mod.py* |
|                                       |                                                              |

#### 3.3 Junit XML测试报告

​	Pytest 可以方便的生成测试报告，通过指定--junitxml 参数可以生成 XML 格式的测试报告，junitxml 是一种非常通用的标准的测试报告格式，可以用来与持续集成工具等很多工具集成（需要通过Jenkins安装插件查看测试报告）。

`$ py.test -s -q --junitxml=./report.xml Tests/`

### 4. 改造基于Pytest的测试用例

​	allure-pytest的[官方文档](https://docs.qameta.io/allure/#_pytest)中详细介绍了allure-pytest所具有的功能。这边我们从实际入手，介绍如何将其应用到自己的项目中。

#### 4.1 修改原有测试用例

```python
@allure.feature("Mac软件商店")  # allure.feature:产品需求
class TestInMacsofts(object):
    @allure.story("Mac商店应用查询接口测试")  # allure.store:针对产品需求的实际测试场景
    @allure.severity(allure.severity_level.NORMAL)  # allure.severity:标记测试用例级别
    @pytest.mark.parametrize('case, http, expected', list(list_params), ids=cases)
    def test_in_macsofts(self, env, case, http, expected):
        # 步骤1：调用step函数
        login("wanli", "dingtax.cn")
        # 步骤2：step的参数打印在测试报告中
        with allure.step("准备发起请求"):
            allure.attach("attach可以打印一些附加信息~")
            allure.attach("请求方式：", http['method'], "请求地址：", env['host']['macwk'] + http['path'])
            # allure.attach("请求参数：", http['params'])
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
```



#### 4.2 Allure 常用特性介绍

​	

<center>表4-1 Allure常用特性</center>

| 方法             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| @allure.feature  | 用于描述被测试产品需求                                       |
| @allure.story    | 用于描述feature的用户场景，即测试需求                        |
| @allure.Severity | 标记测试用例级别                                             |
| with allure.setp | 用于描述测试步骤，将会输出到报告中（在测试方法中）           |
| allure.attach    | 用于向测试报告中输入一些附加的信息，通常是一些测试数据，截图等 |
| @allure.step     | 用于将一些通用的函数作为测试步骤输出到报告（测试方法或者测试类前使用装饰器使用），调用此函数的地方会向报告中输出步骤 |
|                  |                                                              |

<center>表4-2 Severity级别枚举</center>

| 等级     | 说明                             |
| -------- | -------------------------------- |
| BLOCKER  | 阻塞缺陷(功能未实现，无法下一步) |
| CRITICAL | 严重缺陷（功能点缺陷）           |
| NORMAL   | 一般缺陷                         |
| MINOR    | 次要缺陷                         |
| TRIVIAL  | 轻微缺陷                         |
|          |                                  |

命令行参数allure-severities可以根据优先级选择需要运行的测试用例 

```powershell
# 只运行 severity=blocker、critical 的测试用例
$ pytest test_severity.py -sq --alluredir=./allure --allure-severities=blocker,critical
 
# 写法二
$ pytest test_severity.py -sq --alluredir=./allure --allure-severities blocker,critical
```



### 5、生成Allure测试报告

​	测试脚本中添加了Allure特性之后，通过两步，就可以展示出测试报告了。

#### 5.1 生成测试报告数据

​	第一步，生成测试报告的数据。在pytest执行测试的时候，指定—alluredir选项及结果数据保存的目录：

```powershell
$ pytest --alluredir results
=============================== test session starts ================================
platform darwin -- Python 3.8.4, pytest-5.4.3, py-1.10.0, pluggy-0.13.1
rootdir: /Users/gilbert/PycharmProjects/pytest_api, inifile: pytest.ini
plugins: allure-pytest-2.8.36
collected 10 items

Tests/Douban/test_in_theaters.py ..                                                                                                                                                                                                                                      [ 20%]
Tests/Macwk/test_in_macsofts.py ..s                                                                                                                                                                                                                                      [ 50%]
Tests/MarkDemo/test_marks.py .s.xx                                                                                                                                                                                                                                       [100%]

=============================== 6 passed, 2 skipped, 2 xfailed in 1.17s ============
```





`./results/`中保存了本次测试的结果数据。另外，还可以执行指定`features`或者`stories`执行一部分测试用例

```powershell
# 只运行 feature 名为 模块 的测试用例
pytest --allure-features=模块

# 只运行 story1、story2 的测试用例（也可以不用=号 空格就行了哦）
pytest --allure-stories story1,story2
```

#### 5.2 生成测试报告页面

​	第二部，生产测试报告页面。通过下面的命令将`./results/`目录下的测试数据生成测试报告页面

```powershell
$ allure generate ./results/ -o ./report/ --clean

Report successfully generated to report
```

- results：步骤一的结果数据存放目录（json格式的测试结果数据）
- report：将results的测试数据生成测试报告页面

- clean目的是先清空测试报告的目录（./report/），在重新生成新的测试报告

报告生成成功后，repost下面会生成对应的文件

```powershell
total 4392
-rw-r--r--   1 gilbert  staff   679K  3 22 20:33 app.js
drwxr-xr-x  12 gilbert  staff   384B  3 22 20:33 data
drwxr-xr-x   5 gilbert  staff   160B  3 22 20:33 export
-rw-r--r--   1 gilbert  staff    57B  3 22 20:33 favicon.ico
drwxr-xr-x   7 gilbert  staff   224B  3 22 20:33 history
-rw-r--r--   1 gilbert  staff   657B  3 22 20:33 index.html
drwxr-xr-x  11 gilbert  staff   352B  3 22 20:33 plugins
-rw-r--r--   1 gilbert  staff   1.5M  3 22 20:33 styles.css
drwxr-xr-x  16 gilbert  staff   512B  3 22 20:33 widgets
```



### 6、 解读测试报告

![image-20210322205622026](/Users/gilbert/Library/Application Support/typora-user-images/image-20210322205622026.png)

​	首页中展示了本次测试的测试用例数量，成功用例、失败用例、跳过用例的比例，测试环境，测试套（SUITES），特性场景（FEATURES BY STORIES）等基本信息，当与Jenkins做了持续置成后，趋势（TREND）区域还将显示历次测试的通过情况。
​	首页的左边栏，还从不同的维度展示测试报告的其他信息，大家可以自己点进去看看。

#### 6.1 功能（Behaviors）页面

![image-20210322210431106](/Users/gilbert/Library/Application Support/typora-user-images/image-20210322210431106.png)

​	进入Behaviors页面，这个页面按照FEATURES和 STORIES展示测试用例的执行结果

#### 6.2 测试套（Suits）页面

![image-20210322210549617](/Users/gilbert/Library/Application Support/typora-user-images/image-20210322210549617.png)

​	Allure测试报告将每一个测试脚本，作为一个Suite。在首页点击Suites区域下面的任何一条Suite，都将进入Suites页面。这个页面，以脚本的目录结构展示所有测试用例的执行情况。

#### 6.3 图表（Graphs）页面

![image-20210322210754406](/Users/gilbert/Library/Application Support/typora-user-images/image-20210322210754406.png)

​	这个页面展示了本次测试结果的统计信息，比如测试用例执行结果状态、测试用例重要等级分布、测试用例执行时间分布等。

#### 6.4 测试用例详情页

![image-20210322211505112](/Users/gilbert/Library/Application Support/typora-user-images/image-20210322211505112.png)

​	从这个页面可以看到测试用例执行的每一个步骤，以及每个步骤的执行结果，每一个步骤都可以添加附件，作为重要信息补充。从这里，对于失败的测试用例，可以一目了然看到原因。