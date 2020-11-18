from __future__ import annotations

import functools
import typing
import unittest


class CrystalMeta(type):
    """
    Defining here a base type for all datacrystals.
    This is based on named tuple and implements algebraicity for datacrystals.
    """

    def __new__(
        mcls,
        typename: str,
        bases: typing.Optional[typing.Tuple] = None,
        attrs: typing.Optional[typing.Dict] = None,
    ):

        # dropping attributs that are from core python if present, they will be recreated appropriately anyway:
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

    def __eq__(cls, other: CrystalMeta):
        return type(cls) is type(other) and {
            ca: ct
            for ca, ct in vars(cls).items()
            if ca not in ["__dict__", "__weakref__"]
        } == {
            oa: ot
            for oa, ot in vars(other).items()
            if oa not in ["__dict__", "__weakref__"]
        }

    def __setattr__(self, key, value):
        raise TypeError("Classes built via CrystalMeta are immutable !")


if __name__ == "__main__":

    class CrystalExample(metaclass=CrystalMeta):
        attr1: int = 42
        attr2: str
        attr3 = "bob"

        def some_method(self):
            return self.attr1

    print(CrystalExample)
