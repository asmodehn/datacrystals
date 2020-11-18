from __future__ import annotations

import functools
import typing
import unittest
from types import MappingProxyType


def _crystal_key(cls):
    """Deterministic function to compute the 'signature' or 'key' of a 'crystal'.
    This is used for equality checking and hashing on the class/type itself.
    We cannot cache this, so the code has to be unambiguous, deterministic, and fast enough...
    """
    # Note: a different __module__, __name__ or __doc__ is enough to get a different type.
    dtyp = {
        a: t
        for a, t in cls.__annotations__.items()
        if a not in ["__dict__", "__weakref__"]
    }
    # Annotations must not appear in values, as the dict is not hashable... # TODO : maybe make this a mapping proxy to prevent mutation ?
    dflt = {
        a: d
        for a, d in vars(cls).items()
        if a not in ["__dict__", "__weakref__", "__annotations__"]
    }

    # gathering all keys (with value defined or not)
    attrs = set(dtyp.keys()).union(set(dflt.keys()))

    # If an attributes is in __annotations__, but does not have default => we take hte key with None as value
    # To make his existence count, but without any value...
    # Obviously this will create conflict with None as default value -> it is !TEMPORARY!
    # TODO : FIX IT (with some void/missing/empty custom type, or by checking if type is Optional[])
    return tuple(
        (a, dflt.get(a, None), dtyp.get(a, type(dflt.get(a, None)))) for a in attrs
    )
    # Note this relies on the logic "if there is no type declared, there *has to be* a value"


class CrystalMeta(type):
    """
    Defining here a base type ('metaclass' in python speak) for all datacrystals.
    This aims to implement algebraicity for datacrystals, eventually.
    """

    def __new__(
        mcls,
        typename: str,
        bases: typing.Optional[typing.Tuple] = None,
        attrs: typing.Optional[typing.Union[typing.Dict, MappingProxyType]] = None,
    ):
        # dropping attributs that are from core python if present, they will be recreated appropriately anyway:
        if isinstance(attrs, MappingProxyType):
            attrs = {
                a: t for a, t in attrs.items() if a not in ["__dict__", "__weakref__"]
            }
        else:
            attrs.pop("__dict__", None)
            attrs.pop("__weakref__", None)

        # __module__ and __doc__ should be there already

        # making sure we have __annotations__
        if "__annotations__" not in attrs:
            attrs["__annotations__"] = {}

        # Resolving __annotations__ for all attributes that are not prefixed by '__'
        for a in attrs:
            if not a.startswith("__") and a not in attrs.get("__annotations__"):
                # TODO : for a function/method, we should get the actual function type...
                attrs.get("__annotations__")[a] = (
                    type(attrs[a]) if a in attrs else typing.Any
                )

        return super(CrystalMeta, mcls).__new__(mcls, typename, (), attrs)

    def __repr__(cls):
        base_repr = f"<class '{cls.__module__}.{cls.__qualname__}'>"
        attr_str = ", ".join([f"{a}: {t}" for a, t in cls.__annotations__.items()])
        if attr_str:
            return base_repr[:-2] + f"[{attr_str}]'>"
        else:
            return base_repr

    def __hash__(cls):
        """ hash definition to identify classes with same behavior"""
        k = _crystal_key(cls)
        try:
            return hash(k)
        except TypeError as te:
            raise te

    def __eq__(cls, other: CrystalMeta):
        if isinstance(other, CrystalMeta):
            return _crystal_key(cls) == _crystal_key(other)
        raise NotImplementedError  # we need to be very cautious here...

    def __setattr__(cls, key, value):
        # This allows us to cache the class via its hash !
        raise TypeError("Classes built via CrystalMeta are immutable !")


if __name__ == "__main__":

    class CrystalExample(metaclass=CrystalMeta):
        attr1: int = 42
        attr2: str
        attr3 = "bob"

        def some_method(self):
            return self.attr1

    print(CrystalExample)
