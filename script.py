from typing import Protocol
from typing import TypeVar, Any, Type, Generic, ClassVar, TYPE_CHECKING
import os
import inspect

if TYPE_CHECKING:
    Base = object
else:
    Base = Protocol


class Handler:
    protocol = TypeVar("protocol")
    default_store_key = "env"
    _registry: dict = {}

    @classmethod
    def build(cls, protocol: Type[protocol], store: str = None) -> protocol:
        store = store or cls.default_store_key
        env = os.environ.get(store)
        handler_members = cls._registry.get(protocol)

        if not handler_members:
            raise ValueError(f"No binding found for protocol {protocol} and store {store}")

        klass = handler_members.get(env)

        if not klass:
            raise NotImplementedError()

        instance = cls.inject(klass(), store)

        return instance

    @classmethod
    def inject(cls, instance, store: str = None):
        for attribute, _type in inspect.get_annotations(instance.__class__).items():
            if not getattr(_type, "_is_protocol", False):
                continue
            setattr(instance, attribute, cls.build(_type, store))
        return instance

    @classmethod
    def register(cls, protocol, env):
        def wrapper(klass):
            if protocol not in cls._registry:
                cls._registry[protocol] = {}
            cls._registry[protocol][env] = klass
            return klass

        return wrapper


class Printer(Base):
    def print(self, value):
        ...


@Handler.register(Printer, "stage")
class PrinterImpl:
    def print(self, value):
        print(value)


class ApplicationInit:
    def __init__(self, printer: Printer):
        self.printer = printer

    def test(self, value):
        self.printer.print(value)


class MyProto(Base):
    def test(self):
        ...


class MyProtoBis(Base):
    def test(self):
        ...


@Handler.register(MyProto, "dev")
class HereIGo:
    printer: Printer

    def test(self):
        self.printer.print("dev")


@Handler.register(MyProto, "stage")
class HereIGoStage:
    printer: Printer

    def test(self):
        self.printer.print("stage")


@Handler.register(MyProtoBis, "stage")
class HereIGoStageBis:
    printer: Printer

    def test(self):
        print(self)
        # self.printer.print("stage")


if __name__ == "__main__":
    # ApplicationInit(Printer()).test()
    appli = Handler.build(MyProto).test()
    appli = Handler.build(MyProtoBis).test()
