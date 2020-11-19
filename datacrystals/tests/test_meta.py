import unittest
from types import MethodType
from typing import Any, Dict, List, Set, Tuple

import hypothesis.strategies as st
from hypothesis import Verbosity, given, settings

from .._meta import CrystalMeta, _crystal_key
from .test_shards import st_dynclasses


class TestCrystalKey(unittest.TestCase):
    """This tests the equality semantics on classes"""

    @given(dynclass=st_dynclasses(), data=st.data())
    def test_crystal_key(self, dynclass, data):

        cls = CrystalMeta(*dynclass)

        k1 = _crystal_key(cls)
        k2 = _crystal_key(cls)
        assert k1 == k2

        other_cls = CrystalMeta(*data.draw(st_dynclasses()))

        k3 = _crystal_key(other_cls)

        # different if there is any difference on annotations
        if other_cls.__annotations__ != cls.__annotations__:
            assert (
                k3 != k1
            ), f"ERROR: {k3} == {k1} but {other_cls.__annotations__} != {cls.__annotations__}"
        else:
            # different if there is any difference on class attributes
            # except a few that remain different by nature

            attrs3 = {
                a: v
                for a, v in vars(other_cls).items()
                if a not in ["__dict__", "__weakref__"]
            }
            attrs1 = {
                a: v
                for a, v in vars(cls).items()
                if a not in ["__dict__", "__weakref__"]
            }

            if attrs3 != attrs1:
                assert k3 != k1
            else:
                assert k3 == k1


class TestMeta(unittest.TestCase):
    @given(dynclass=st_dynclasses())
    @settings(verbosity=Verbosity.verbose)
    def test_strategy(self, dynclass):

        cls = CrystalMeta(*dynclass)
        assert isinstance(cls, CrystalMeta)
        assert type(cls) == CrystalMeta

    @given(dynclass=st_dynclasses())
    # @settings(verbosity=Verbosity.verbose)
    def test_equality_hash(self, dynclass):

        cls = CrystalMeta(*dynclass)
        clsdup = CrystalMeta(*dynclass)

        # we have reflexivity
        assert cls is cls
        assert cls == cls
        assert hash(cls) == hash(cls)

        assert clsdup is clsdup
        assert clsdup == clsdup
        assert hash(clsdup) == hash(clsdup)

        # But these are NOT THE SAME underneath, # TODO : should they be ??
        #  and we will not enforce functional behavior this deep.
        assert clsdup is not cls

        # This is reflected at the user level, via the crystal_key that checks many attributes:
        assert clsdup != cls
        assert hash(clsdup) != hash(cls)

    @given(dynclass=st_dynclasses())
    def test_annotations(self, dynclass):
        cls = CrystalMeta(*dynclass)
        for f in vars(cls):  # TODO : rely on dataclasses for this behavior...
            # making sure all existing class values are present in annotations
            if (
                not f.startswith("__") and type(getattr(cls, f)) != MethodType
            ):  # TODO : better typing of methods...
                assert f in cls.__annotations__, f"{f} not in {cls.__annotations__}"

    @given(dynclass=st_dynclasses())
    def test_repr(self, dynclass):
        cls = CrystalMeta(*dynclass)
        assert cls.__module__ in repr(cls)
        assert cls.__qualname__ in repr(cls)
        # making sure all annotations are displayed in repr (we aim to enforce types)
        for f, t in cls.__annotations__.items():
            assert f"{f}: {t}" in repr(cls)


if __name__ == "__main__":
    unittest.main()
