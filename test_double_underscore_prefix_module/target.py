def _single_underscore_function():
    return 'single'

def __double_underscore_function():
    return 'double'


class Target(object):
    def _single_underscore_method(self):
        return 'single'

    def __double_underscore_method(self):
        return 'double'