import inspect
from typing import Type
from typing import TypeVar

from aristaeus.config import settings

DEFAULT_STORE = object()


class Injector:
    protocol = TypeVar("protocol")
    default_store_key = "current_env"
    _registry: dict = {}

    @classmethod
    def get(cls, protocol: Type[protocol], store: str = None, kwargs: dict = None) -> protocol:
        store = (store or getattr(settings, cls.default_store_key)).lower()
        handlers = cls._registry.get(protocol)
        kwargs = kwargs or {}

        if not handlers:
            raise NotImplementedError(f"Protocol {protocol} not managed")

        klass = handlers.get(store) or handlers.get(DEFAULT_STORE)

        if not klass:
            raise NotImplementedError(f"No binding found for protocol {protocol} and store {store}")

        instance = cls.inject(klass(**kwargs), store)
        return instance

    @classmethod
    def inject(cls, instance, store: str = None):
        for attribute, _type in inspect.get_annotations(instance.__class__).items():
            if not getattr(_type, "_is_protocol", False):
                continue

            setattr(instance, attribute, cls.get(_type, store))

        return instance

    @classmethod
    def bind(cls, protocol, *stores):
        stores = stores or [DEFAULT_STORE]

        def wrapper(klass):
            if protocol not in cls._registry:
                cls._registry[protocol] = {}
            for store in stores:
                cls._registry[protocol][store] = klass
            return klass

        return wrapper


class InjectorMixin:
    def __init__(self):
        super().__init__()
        Injector.inject(self)
