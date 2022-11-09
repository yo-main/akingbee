class SingletonMeta(type):
    _registry: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._registry:
            instance = super().__call__(*args, **kwargs)
            cls._registry[cls] = instance

        return cls._registry[cls]
