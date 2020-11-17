import functools
from collections.abc import Collection
from dataclasses import asdict, fields
from decimal import Decimal
from typing import List, Type

import hypothesis.strategies as st
import pandas as pd


# Attempting to make this functional, the easy way.
@functools.lru_cache(typed=True)
def _collection_from_class(_cls):
    """
    >>> from datacrystals import datacrystal
    >>> @datacrystal
    ... class Shard:
    ...     answer: int
    ...     question: str = "What is the answer ?"
    ...

    This  defines a type to be used as a collection of datacrystals
    >>> ShardCollection = _collection(Shard)
    >>> s1 = Shard(answer=42, question="What is it ??")
    >>> s2 = Shard(answer=51, question="No but really ??")

    >>> collec = ShardCollection(s1, s2)
    >>> print(collec)

    Important: creating a collection of a certain crystal is functional:
    >>> Collec2 = _collection(Shard)
    >>> Collec2 is ShardCollection
    True

    This keeps things simple and avoid to be overcrowded with identical data structures.
    BUT the creation of an instance of that type is NOT (as per python usual behavior)

    >>> collec2 = Collec2(s1, s2)
    >>> collec2 is collec
    False
    >>> collec2 == collec
    True

    """

    collection_attr = {}

    @st.composite
    def _collect_strategy(draw, cls, max_size=5):
        tl = draw(st.lists(elements=_cls.strategy(), max_size=max_size))
        return cls(*tl)

    collection_attr["strategy"] = classmethod(_collect_strategy)

    def init(self, *inners: _cls):
        # Reminder : this object is considered monotonic (only appending is possible via call)
        df = pd.DataFrame.from_records(
            [asdict(dc) for dc in inners],
            columns=[f.name for f in fields(_cls)],
        )

        self.Inner = _cls
        self._df = df

    collection_attr["__annotations__"] = {"Inner": Type, "_df": pd.DataFrame}
    collection_attr["__init__"] = init

    collection_attr["__cache__"] = {}

    # optimization interfacing with "lower compute libs"
    def optimize(slf):
        opt_copy = slf._df.copy(deep=True)
        if len(opt_copy):
            opt_copy.convert_dtypes()
            # also convert decimal to floats, losing precision
            for f in fields(_cls):
                if f.type is Decimal:
                    setattr(opt_copy, f, getattr(opt_copy, f).to_numpy("float64"))

        return opt_copy

    collection_attr["optimize"] = optimize

    # abc.Collection interface

    def contains(self, item: _cls):
        # relying on index behavior
        if len(self._df) > 0:
            # Note : we cannot rely on functional behavior here, methods like __iter__ create new instances...
            var = [getattr(self._df, f) == getattr(item, f) for f in fields(item)]
            return all(var)  # Note: This returns True if there is no field
        return False

    collection_attr["__contains__"] = contains

    def iter(self):
        for i in self._df.itertuples(index=True):
            # dropping index (needed in case class has no attrs, we technically still have an instance)
            attr = {a: v for a, v in i._asdict().items() if a != "Index"}
            yield _cls(
                **attr
            )  # TODO : functional behavior on instance creation to simplify things ???

    collection_attr["__iter__"] = iter

    def llen(self):
        return len(self._df)

    collection_attr["__len__"] = llen

    def _dir(slf) -> List[str]:

        exposed = ["strategy", "Inner", "optimize"]

        # and expose fields
        inner_fields = [f.name for f in fields(slf.Inner)]

        return exposed + inner_fields

    collection_attr["__dir__"] = _dir

    # However we may have more appropriate human display
    try:
        from tabulate import tabulate

        def strtab(slf):
            optdf = slf.optimize()

            # Human friendly display of dataclasses
            typename = type(slf).__name__
            lines = [f"{typename}", "-" * len(typename)]

            tablines = tabulate(optdf, headers="keys", tablefmt="psql")

            return "\n".join(lines) + "\n" + tablines

        collection_attr["__str__"] = strtab

    except ImportError:

        def strraw(slf):
            optdf = slf.optimize()

            # Human friendly display of dataclasses
            typename = type(slf).__name__
            lines = [f"{typename}", "-" * len(typename)]

            for i in optdf:
                lines.append(str(i))
            return "\n".join(lines)

        collection_attr["__str__"] = strraw

    def call(self, elem: _cls):
        self._df = self._df.append(asdict(elem))
        return self

    collection_attr["__call__"] = call

    # Collection interface is respected, but we dont want to inherit from collection (inheritance hierarchy not needed)
    Collec = type(_cls.__name__ + "Collection", (), collection_attr)

    return Collec


if __name__ == "__main__":
    import doctest

    doctest.testmod()
