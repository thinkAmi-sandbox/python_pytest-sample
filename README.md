# python_pytest-sample

# Tested environment

## Mac

- Mac OS X 10.11.6
- Python 3.6.3
- pytest 3.2.3

　  
## Windows

tested only `e.g._double_underscore_prefix_module`

- Windows10 x64
- Python 3.6.0 32bit
- pytest 3.0.5

　  
# Examples

- `e.g._double_underscore_prefix_module/`
  - sample code: double underscore prefix module
  - run test by `e.g._double_underscore_prefix_module/ $ python -m pytest`

- `e.g._monkeypatch/`
  - sample code: usage pytest.monkeypatch
  - run test by `e.g._monkeypatch/ $ python -m pytest`
  
- `e.g._pytest_raises`
  - sample code: usage pytest.raise
  
- `e.g._k_option_and_marker`
  - tested by pytest 3.9.1
  - run test by `e.g._k_option_and_marker / $ python -m pytest -m foo -v` or `e.g._k_option_and_marker / $ python -m pytest -k foo -v` 

　  
# Related Blog (Written in Japanese)

- [Python + pytestで、プレフィクスがアンダースコア2つの関数(プライベート関数)をテストする - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2016/12/26/061252)
- [Python + pytestで、monkeypatch.setattr()を使ってみた - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2017/03/07/065903)
- [Python + pytestにて、pytest.raisesを使って例外をアサーションする時の注意点 - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2017/03/23/064016)
- [Python + pytestにて、pytestに独自のコマンドラインオプションを追加する - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2017/10/25/222551)
- [pytestのkオプションは、マーカー名でマッチしているものもテスト対象だった - メモ的な思考的な](http://thinkami.hatenablog.com/entry/2018/10/21/221055)
