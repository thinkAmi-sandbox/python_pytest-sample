import platform
import os
import outer_import
from outer_from_import import BAR
import sys
import datetime

class Target(object):
    CONST_VALUE = 'foo'

    def get_platform(self):
        return platform.system()

    def get_os_system(self):
        return os.system()

    def get_const(self):
        return self.CONST_VALUE

    def get_multi_args(self, foo, bar):
        return ''.join([foo, bar])

    def call_private_function(self):
        self.__run_complex()
        return self.CONST_VALUE

    def __run_complex(self):
        # 何行も続いて、最後にうまくいってないときはraiseする
        # さらに戻り値は返さないという、面倒なプライベートメソッド
        raise Exception

    def get_multi_return_values(self):
        return ('foo', 'bar')

    def raise_exception(self):
        raise RuntimeError('foo')

    def get_outer_import(self):
        return outer_import.FOO
    
    def get_outer_from_import(self):
        return BAR

    def write_stdout(self):
        print('foo')

    def write_cp932_stdout(self):
        print('ほげ'.encode('cp932'))

    def get_sys_exc_info(self):
        return sys.exc_info()

    def get_current_datetime(self):
        return datetime.datetime.now()