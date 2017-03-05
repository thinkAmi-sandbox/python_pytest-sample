import pytest
from target import _single_underscore_function
from target import __double_underscore_function
import target
from target import __double_underscore_function as double_underscore_function
from target import Target



def test_double_underscore_prefix_function_using_from_import():
    assert __double_underscore_function() == 'double'
    # => pass


class Test_function(object):
    def test_single_underscore_prefix_function_using_from_import(self):
        assert _single_underscore_function() == 'single'
        # => pass

    @pytest.mark.xfail(raises=NameError)
    def test_double_underscore_prefix_function_using_from_import(self):
        assert __double_underscore_function() == 'double'
        # => NameError: name '_Test_function__double_function' is not defined

    @pytest.mark.xfail(raises=AttributeError)
    def test_double_undersocre_prefix_function_using_import(self):
        assert target.__double_underscore_function() == 'double'
        # => AttributeError: module 'target' has no attribute '_Test_function__double_underscore_function'

    def test_double_undersocre_prefix_function_using_from_import_alias(self):
        assert double_underscore_function() == 'double'
        # => pass


class Test_class(object):
    def test_single_underscore_prefix_function_using_from_import(self):
        sut = Target()
        assert sut._single_underscore_method() == 'single'
        # => pass

    def test_double_underscore_prefix_function_using_from_import(self):
        sut = Target()
        assert sut._Target__double_underscore_method() == 'double'
        # => pass
