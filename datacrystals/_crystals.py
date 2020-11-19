# frozen dataclass (pydantic for type check)
# Basic record type. Non Empty set of attributes (order shouldn't matter, unicity enforced)
import functools
from collections.abc import Collection
from dataclasses import asdict, fields
from decimal import Decimal
from types import FunctionType
from typing import Any, Callable, List, Optional, Tuple, Type, TypeVar, Union

import hypothesis.strategies as st  # type: ignore
from hypothesis import infer

ShardType = TypeVar("ShardType")


def _str(slf: ShardType) -> str:
    # Human friendly display of dataclasses
    typename = type(slf).__name__
    lines = [f"{typename}", "-" * len(typename)]
    for f in fields(slf):
        lines.append(f"{f.name}: {getattr(slf,f.name)}")

    return "\n".join(lines)


def _dir(slf: ShardType) -> List[str]:
    # only expose fields
    return [f.name for f in fields(slf)]


def _strategy(cls: Type[ShardType]) -> st.SearchStrategy:
    # Strategie inferring attributes from type hints by default

    params = {}

    for f in fields(cls):
        if f.name:  # to pass as param we need to have a keyword
            if f.type is float:
                strat = st.floats(
                    allow_nan=False
                )  # Nans are not equals to themselves !
            elif f.type is Decimal:
                strat = st.decimals(
                    allow_nan=False
                )  # Nans are not equals to themselves !
            else:
                strat = infer
            params.update({f.name: strat})

    # calling the functional factory...
    return st.builds(cls, **params)


try:
    from pydantic.dataclasses import dataclass  # type: ignore

    print("pydantic detected: Enabling runtime dynamic typechecking.")
except ImportError as ie:
    from dataclasses import dataclass


def _make_shard(
    _cls: Type[Any],
    order: bool,
) -> Type[ShardType]:

    cls = dataclass(
        init=True,
        repr=True,
        eq=True,
        order=order,
        unsafe_hash=False,
        frozen=True,
    )(
        _cls
    )  # calling it as a decorator to make mypy happy.

    # extras for cleaner 'record' class
    setattr(cls, "__str__", _str)
    setattr(cls, "__dir__", _dir)

    # to generate elements pseudo-randomly
    setattr(cls, "strategy", classmethod(_strategy))

    # TODO : somewhere else ?? (to keep this minimal, and testing independent enough...)
    # # to build collection type from the element description
    # setattr(cls, "Collection", _collection_from_class(cls))  # collection type registered as part of this type.
    # setattr(cls, "collection", cls.Collection())  # collection instance to store created class instances

    return cls


def shard(
    _cls: Optional[Type[Any]] = None,
    *,
    order: bool = False,
) -> Union[Callable[[Type[ShardType]], Type[ShardType]], Type[ShardType]]:
    """
    Decorator to wrap a dataclass declaration.
    Relies on Pydantic to provide type verification.

    This is usable as python's dataclass decorator, but also provide more features, along with more strictness
    >>> import decimal
    >>> @shard
    ... class SampleDataCrystal:
    ...      attr_int: int
    ...      attr_dec: decimal.Decimal
    ...

    >>> SampleDCInstance = SampleDataCrystal(attr_int= 42, attr_dec=decimal.Decimal("3.1415"))

    datacrystal() provides, on top of pydantic's or python's dataclass:

    Machine output:
    >>> print(repr(SampleDCInstance))
    SampleDataCrystal(attr_int=42, attr_dec=Decimal('3.1415'))

    Human output:
    >>> print(str(SampleDCInstance))
    SampleDataCrystal
    -----------------
    attr_int: 42
    attr_dec: 3.1415

    attributes for introspection retrieving only the declared fields (without potential custom validator)
    >>> dir(SampleDCInstance)
    ['attr_dec', 'attr_int']

    Important: Just as with dataclasses, constructing equal instances is possible,
    and no effort is made here to make __init__ functional.
    >>> sdc1 = SampleDataCrystal(attr_int= 42, attr_dec=decimal.Decimal("3.1415"))
    >>> sdc2 = SampleDataCrystal(attr_int= 42, attr_dec=decimal.Decimal("3.1415"))
    >>> sdc1 is sdc2
    False
    >>> sdc1 == sdc2
    True
    """

    def wrap(cls: Type[Any]) -> Type[ShardType]:
        return _make_shard(cls, order=order)

    if _cls is None:
        return wrap

    return wrap(_cls)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
