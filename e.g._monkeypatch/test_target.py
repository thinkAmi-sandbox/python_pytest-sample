import pytest
from target import Target
import platform
import outer_import
import outer_from_import
import functions
import sys
# プライベート関数はそのままではimportできないので、asを使って回避する
from functions import __private_function as pf
import datetime


# 同じディレクトリにテストコードとテスト対象コードが存在しているため、PYTHONPATHの設定を実行時に行うため、
# このテストは、`path/to/ex_monkeypatch $ python -m pytest`で実行する
# http://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada
class Test_target:
    def test_patch_standard_library(self, monkeypatch):
        expected = 'ham'
        # 差し替え対象のパッケージをimportして差し替える
        monkeypatch.setattr(platform, 'system', lambda: expected)
        sut = Target()
        actual = sut.get_platform()
        assert actual == expected

    def test_patch_no_import(self, monkeypatch):
        expected = 'ham'
        # テストファイルでimportしなくても差し替えられる
        monkeypatch.setattr('os.system', lambda: expected)
        sut = Target()
        actual = sut.get_os_system()
        assert actual == expected


    def test_patch_by_lambda(self, monkeypatch):
        expected = 'ham'
        monkeypatch.setattr(Target, 'get_const', lambda x: expected)
        sut = Target()
        actual = sut.get_const()
        assert actual == expected

    def test_patch_by_dummy_function(self, monkeypatch):
        def run_dummy(arg):
            # Target.get_constは引数selfがあるため、差し替えメソッドでも引数(arg)を用意
            return 'ham'
        monkeypatch.setattr(Target, 'get_const', run_dummy)
        sut = Target()
        actual = sut.get_const()
        assert actual == 'ham'


    def test_const(self, monkeypatch):
        expected = 'ham'
        monkeypatch.setattr(Target, 'CONST_VALUE', expected)
        sut = Target()
        assert sut.CONST_VALUE == expected

    
    def test_function_multi_args1(self, monkeypatch):
        expected = 'ham'
        # 引数self, foo, barをlambdaでも用意
        monkeypatch.setattr(Target, 'get_multi_args', lambda x, y, z: expected)
        sut = Target()
        actual = sut.get_multi_args('foo', 'bar')
        assert actual == expected

    def test_function_multi_args2(self, monkeypatch):
        expected = 'ham'
        # 引数の定義が面倒な時は可変長引数でも良い
        monkeypatch.setattr(Target, 'get_multi_args', lambda *_: expected)
        sut = Target()
        actual = sut.get_multi_args('foo', 'bar')
        assert actual == expected


    def test_patch_private_function(self, monkeypatch):
        # プライベートメソッドはマングリングした表現で指定する
        # 差し替えしないと、プライベートメソッドでraiseしているExceptionが発生
        monkeypatch.setattr(Target, '_Target__run_complex', lambda x: None)
        sut = Target()
        actual = sut.call_private_function()
        assert actual == 'foo'


    def test_patch_multi_return_values(self, monkeypatch):
        # 複数の戻り値がある場合は、タプルなどを返す
        monkeypatch.setattr(Target, 'get_multi_return_values', lambda x: ('ham', 'spam'))
        sut = Target()
        actual1, actual2 = sut.get_multi_return_values()
        assert actual1 == 'ham'
        assert actual2 == 'spam'


    def test_patch_exception(self, monkeypatch):
        # ジェネレータ式のthrow()を使って、lambdaにてワンライナーで例外を出す
        # http://stackoverflow.com/questions/8294618/define-a-lambda-expression-that-raises-an-exception
        # https://docs.python.jp/3/reference/expressions.html#generator.throw
        monkeypatch.setattr(Target, 'raise_exception', lambda x: (_ for _ in ()).throw(AssertionError('ham')))
        sut = Target()
        # 差し替えた例外AssertionErrorが発生したかをチェック
        with pytest.raises(AssertionError) as excinfo:
            sut.raise_exception()
        assert 'ham' == str(excinfo.value)


    def test_patch_import(self, monkeypatch):
        expected = 'ham'
        monkeypatch.setattr(outer_import, 'FOO', expected)
        sut = Target()
        actual = sut.get_outer_import()
        assert actual == expected

    def test_patch_from_import(self, monkeypatch):
        expected = 'ham'
        # targetでfrom...importしているため、元々のouter_from_import.BARを差し替えは意味ない
        #=> 実行結果：差し替わっていない
        #   E       assert 'baz' == 'ham'
        #   E         - baz
        #   E         + ham
        # monkeypatch.setattr(outer_from_import, 'BAR', expected)
        
        # from...import時は、from...importしてtarget.pyに追加されたオブジェクト(BAR)を差し替える
        monkeypatch.setattr('target.BAR', expected)
        sut = Target()
        actual = sut.get_outer_from_import()
        assert actual == expected


    def test_patch_stdout(self, monkeypatch, capsys):
        # pytestのcapsysを併用した例
        # http://doc.pytest.org/en/latest/capture.html
        def print_dummy(arg):
            print('ham')
        # python3ではprintは式なので、lambdaに指定可能
        monkeypatch.setattr(Target, 'write_stdout', lambda x: print('ham'))
        # python2ではprintは文なので、lamdbaに指定できないことから、ダミー関数を使う
        # monkeypatch.setattr(Target, 'write_stdout', print_dummy)
        sut = Target()
        actual = sut.write_stdout()
        actual, _ = capsys.readouterr()
        assert actual == 'ham\n'

    @pytest.mark.skip('標準出力にcp932で出した場合、capsysでもうまく取れない')
    def test_stdout_cp932(self, capsys):
        sut = Target()
        actual = sut.write_cp932_stdout()
        actual, _ = capsys.readouterr()
        assert actual == 'ほげ\n'.encode('cp932')
        # E assert "b'\\x82\\xd9\\x82\\xb0'\n" == b'\x82\xd9\x82\xb0\n'
        # E  +  where b'\x82\xd9\x82\xb0\n' = <built-in method encode of str object at 0x101bb4990>('cp932')
        # E  +    where <built-in method encode of str object at 0x101bb4990> = 'ほげ\n'.encode


    def test_standard_function(self, monkeypatch):
        expected = 'ham'
        monkeypatch.setattr(functions, 'standard_function', lambda: expected)
        actual = functions.standard_function()
        assert actual == expected


    def test_private_function(self, monkeypatch):
        expected = 'ham'
        # プライベート関数は現在実行中のモジュールにimportされている
        # そのため、sys.modules[__name__]を使って現在のオブジェクトを取得し、差し替える
        # http://stackoverflow.com/questions/1676835/python-how-do-i-get-a-reference-to-a-module-inside-the-module-itself
        monkeypatch.setattr(sys.modules[__name__], 'pf', lambda: expected)
        actual = pf()
        assert actual == expected

    
    @pytest.mark.skip('sys.exc_infoを差し替えるとpytestの結果表示がおかしくなるので、やめること')
    def test_do_not_patch_exc_info(self, monkeypatch):
        expected = ('ham', 'spam', 'egg')
        def patch_exc_info(arg):
            return expected
        monkeypatch.setattr(sys, 'exc_info', patch_exc_info)
        sut = Target()
        actual = get_sys_exc_info()
        # テストは通るが、以下のエラーが出て、pytestの結果が乱れる
        # test_monkeypatch.py ...............
        # ========================== 15 passed in 0.09 seconds ===========================
        # ...
        # Traceback (most recent call last):
        #   TypeError: patch_exc_info() missing 1 required positional argument: 'arg'
        #   During handling of the above exception, another exception occurred:
        assert actual == expected
        
    
    def test_patch_datetime(self, monkeypatch):
        # http://stackoverflow.com/questions/20503373/how-to-monkeypatch-pythons-datetime-datetime-now-with-py-test
        # http://stackoverflow.com/questions/35431476/why-pythons-monkeypatch-doesnt-work-when-importing-a-class-instead-of-a-module
        # pytestに限らない場合
        # http://stackoverflow.com/questions/4481954/python-trying-to-mock-datetime-date-today-but-not-working
        expected = datetime.datetime.now()
        class PatchedDatetime(datetime.datetime):
            @classmethod
            def now(cls):
                return expected
        monkeypatch.setattr('datetime.datetime', PatchedDatetime)
        sut = Target()
        actual = sut.get_current_datetime()
        assert actual == expected

    @pytest.mark.skip('C拡張の組込型はmonkeypatchできない')
    def test_cannot_patch_datetime(self, monkeypatch):
        expected = datetime.datetime.now()
        # monkeypatchしようとすると、C拡張の組込型はエラーになる
        # E TypeError: can't set attributes of built-in/extension type 'datetime.datetime'
        # http://qiita.com/youhei/items/7502d161aecdd59030b9
        monkeypatch.setattr('datetime.datetime.now', lambda: expected)
        sut = Target()
        actual = sut.get_current_datetime()
        assert actual == expected

