import pytest


@pytest.mark.foo
class TestHam:
    """クラスにマーカーあり"""
    def test_spam_method(self):
        assert True

    def test_egg_method(self):
        assert True


class TestHoge:
    @pytest.mark.foo
    def test_spam_method(self):
        """このテストメソッドだけマーカーあり"""
        assert True

    def test_egg_method(self):
        assert True


class TestHogefoo:
    """テストクラス名に foo が含まれる"""
    def test_spam_method(self):
        assert True

    def test_egg_method(self):
        assert True


@pytest.mark.foo
def test_bar_function():
    """テスト関数にマーカーあり"""
    assert True


def test_foo_function():
    """テスト関数に foo が含まれる"""
    assert True


def test_baz_function():
    assert True
