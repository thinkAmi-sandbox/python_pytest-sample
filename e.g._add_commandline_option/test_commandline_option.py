import pytest


def test_fruit(favorite_fruit, is_season):
    print(f'\nfruit:{favorite_fruit}, is_season:{is_season}')
    assert True


def test_no_marker():
    print('apple')
    assert True


@pytest.mark.test_number(1)
def test_with_marker():
    print('grape')
    assert True


@pytest.mark.parametrize('kind, code', [
    pytest.param('banana', '123', marks=pytest.mark.test_number(2)),
    pytest.param('pear', '456', marks=pytest.mark.test_number(3)),
])
def test_parameterize_with_marker(kind, code):
    print(f'\n{kind}: {code}')
    assert True
