from unittest.mock import patch, MagicMock
import pytest
from pytest_raises import Target

class Test_Target(object):
    def test_mock_patch(self):
        """patchだけを使う

        例外を送出するメソッドをモックに差し替えたので、例外の送出がなくなった
        """
        mock_run = MagicMock()
        with patch('pytest_raises.Validator.run', mock_run):
            sut = Target()
            actual = sut.target_method()
            assert mock_run.call_count == 1


    def test_mistake_usage_pytest_raises(self):
        """patchとraisesを使う

        ただし、pytest.raisesの使い方が間違っている
        コンテキストが例外を送出するメソッドで終わっていない
        """
        mock_run = MagicMock(side_effect=AssertionError)
        with patch('pytest_raises.Validator.run', mock_run), \
                pytest.raises(AssertionError):
            sut = Target()
            actual = sut.target_method()
            assert mock_run.call_count == 1


    def test_mistake_usage_pytest_raises_but_test_pass(self):
        """patchとraisesを使う

        コンテキストが例外を送出するメソッドで終わっていないため、
        テストもパスしてしまう
        """
        mock_run = MagicMock(side_effect=AssertionError)
        with patch('pytest_raises.Validator.run', mock_run), \
                pytest.raises(AssertionError):
            sut = Target()
            actual = sut.target_method()
            assert mock_run.call_count == 2


    @pytest.mark.xfail
    def test_correct_usage_pytest_raises_and_test_fail(self):
        """patchとraisesを使う

        pytest.raisesの正しい使い方
        コンテキストが例外を送出するメソッドで終わっている
        """
        mock_run = MagicMock(side_effect=AssertionError)
        with patch('pytest_raises.Validator.run', mock_run):
            with pytest.raises(AssertionError):
                sut = Target()
                actual = sut.target_method()
            assert mock_run.call_count == 2
