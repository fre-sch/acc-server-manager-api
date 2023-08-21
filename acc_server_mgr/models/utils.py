import pydantic
from pydantic import validator


def list_from_iter(field_name):
    return validator(field_name, pre=True, allow_reuse=True)(list)


class AllOptional(pydantic.main.ModelMetaclass):
    def __new__(mcls, name, bases, namespaces, **kwargs):
        cls = super().__new__(mcls, name, bases, namespaces, **kwargs)
        for field in cls.__fields__.values():
            field.required=False
        return cls
