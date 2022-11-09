from akb.injector import Injector


class BaseApplication:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Injector.inject(self)
