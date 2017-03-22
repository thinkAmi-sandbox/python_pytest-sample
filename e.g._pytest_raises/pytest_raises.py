from pytest_raises_library import Validator

class Target(object):
    def target_method(self):
        """テスト対象のメソッド"""
        validator = Validator()
        validator.run()
