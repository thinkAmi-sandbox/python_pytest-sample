from target import __double_underscore_function
import target

class Main(object):
    def run_with_import_from(self):
        print(f'from import: {__double_underscore_function()}')
        # => NameError: name '_Main__double_underscore_function' is not defined

    def run_with_import(self):
        print(f'import: {target.__double_underscore_function()}')
        # => AttributeError: module 'target' has no attribute '_Main__double_underscore_function'

def main():
    print(f'from import: {__double_underscore_function()}')
    # => from import: double

    print(f'import: {target.__double_underscore_function()}')
    # => import: double

if __name__ == '__main__':
    m = Main()
    m.run_with_import_from()
    m.run_with_import()
    