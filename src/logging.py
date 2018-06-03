def default_logger():
    class LoggingWrapper:
        def __init__(self, cls):
            print(f'Initalized an instance of {cls}')
            self.other_class = cls

        def __call__(self, *cls_ars):
            self.before_call(*cls_ars)
            return_value = self.other_class(*cls_ars)
            self.after_call(return_value, *cls_ars)
            return return_value

        def before_call(self, *args):
            # print(*args)
            pass

        def after_call(self, return_value, *args):
            print(return_value)
            # print(*args)

    return LoggingWrapper
