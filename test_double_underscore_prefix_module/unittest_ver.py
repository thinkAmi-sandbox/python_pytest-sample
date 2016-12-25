import unittest
from target import _single_underscore_function
from target import __double_underscore_function
import target
from target import __double_underscore_function as double_underscore_function


class Test_function(unittest.TestCase):
    def test_single_underscore_prefix_function_using_from_import(self):
        self.assertEqual(_single_underscore_function(), 'single')
        # => pass

    @unittest.expectedFailure
    def test_double_underscore_prefix_function_using_from_import(self):
        self.assertEqual(__double_underscore_function(), 'double')
        # => NameError: name '_Test_function__double_function' is not defined

    @unittest.expectedFailure
    def test_double_undersocre_prefix_function_using_import(self):
        assert target.__double_underscore_function() == 'double'
        # => AttributeError: module 'target' has no attribute '_Test_function__double_underscore_function'

    def test_double_undersocre_prefix_function_using_from_import_alias(self):
        self.assertEqual(double_underscore_function(), 'double')
        # => pass


if __name__ == '__main__':
    unittest.main()
