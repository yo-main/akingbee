from typing import TypeVar, Type
import inspect

from akingbee.config import settings

DEFAULT_STORE = object()


class Injector:
    protocol = TypeVar("protocol")
    default_store_key = "current_env"
    _registry: dict = {}

    @classmethod
    def get(cls, protocol: Type[protocol], store: str = None) -> protocol:
        store = (store or getattr(settings, cls.default_store_key)).lower()
        handler_members = cls._registry.get(protocol)

        if not handler_members:
            raise NotImplementedError(f"Protocol {protocol} not managed")

        klass = handler_members.get(store) or handler_members.get(DEFAULT_STORE)

        if not klass:
            raise NotImplementedError(f"No binding found for protocol {protocol} and store {store}")

        instance = cls.inject(klass(), store)
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
        Injector.inject(self)
        super().__init__()
