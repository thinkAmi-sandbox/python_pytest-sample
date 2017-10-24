import pytest


def pytest_addoption(parser):
    """add commandline options"""
    parser.addoption('--fruit', action='store', default='ham',
                     help='fruit name: apple, grape, banana, etc')
    parser.addoption('--season', action='store_true',
                     help='fruit season now')
    parser.addoption('--target', action='store',
                     help='if commandline args match test decorator, run test. if not, skip it')


def pytest_configure(config):
    """add custom marker"""
    config.addinivalue_line('markers', 'test_number(number): test case number')


@pytest.fixture
def favorite_fruit(request):
    return request.config.getoption('--fruit')


@pytest.fixture
def is_season(request):
    return request.config.getoption('--season')


@pytest.fixture
def my_target(request):
    return request.config.getoption('--target')


def pytest_runtest_setup(item):
    """decide skip or run testcase"""
    marker = item.get_marker('test_number')
    if marker is None:
        return

    opt = item.config.getoption('target')
    if opt is None:
        return

    targets = opt.split(',')
    test_number = str(marker.args[0])
    if test_number not in targets:
        pytest.skip('it is non-target testcase. skip it.')
