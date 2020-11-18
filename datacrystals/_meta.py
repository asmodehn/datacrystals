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

        if "__annotations__" not in attrs:
            attrs["__annotations__"] = {}

        # Resolving __annotations__
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


if __name__ == "__main__":

    class CrystalExample(metaclass=CrystalMeta):
        attr1: int = 42
        attr2: str
        attr3 = "bob"

        def some_method(self):
            return self.attr1

    print(CrystalExample)
