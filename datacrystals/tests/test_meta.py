import unittest
from typing import Any, Dict, List, Set, Tuple

import hypothesis.strategies as st
from hypothesis import Verbosity, given, settings

from .._meta import CrystalMeta, _crystal_key


@st.composite
def st_crystalclasses(
    draw,
    names=st.text(
        alphabet=st.characters(whitelist_categories=["Lu", "Ll"]),
        min_size=1,
        max_size=5,
    ),
):  # TODO : character strategy for legal python identifier ??
    """
     This is a simple strategy creating a class dynamically from a random dictionnary of attributes.
    using our metaclass.
    """
    attrs = draw(
        st.dictionaries(
            keys=st.text(min_size=1),  # identifier
            values=st.one_of(  # default values
                st.integers(),
                st.floats(),
                st.decimals(
                    allow_nan=False, allow_infinity=False
                ),  # CAREFUL NaN is not hashable !
                st.text(),
                # etc. TODO support more... st.functions() ??
            ),
        )
    )

    annots = draw(
        st.dictionaries(
            keys=st.text(min_size=1),  # identifier
            values=st.sampled_from(  # annotations
                [int, float, str, Set, Tuple, List, Dict, Any]
                # etc. TODO support more... function type ??
            ),
        )
    )

    attrs["__annotations__"] = annots

    return CrystalMeta(draw(names), (), attrs)


class TestCrystalKey(unittest.TestCase):
    """This tests the equality semantics on classes"""

    @given(cls=st_crystalclasses(), data=st.data())
    def test_crystal_key(self, cls, data):

        k1 = _crystal_key(cls)
        k2 = _crystal_key(cls)
        assert k1 == k2

        other_cls = data.draw(st_crystalclasses())

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
    @given(cls=st_crystalclasses())
    @settings(verbosity=Verbosity.verbose)
    def test_strategy(self, cls):

        assert isinstance(cls, CrystalMeta)
        assert type(cls) == CrystalMeta

    @given(cls=st_crystalclasses())
    # @settings(verbosity=Verbosity.verbose)
    def test_equality_hash(self, cls):

        clsdup = CrystalMeta(cls.__qualname__, (), vars(cls))

        assert isinstance(clsdup, CrystalMeta)
        assert type(clsdup) == CrystalMeta

        # Actual NOT THE SAME underneath (python will be python),
        # we wont enfoce functional behavior this deep...
        assert clsdup is not cls

        # However overridden type equality is True (assumption: same content => same behavior)
        # REMINDER: This remain True only as long as class doesnt mutate !!
        assert clsdup == cls
        assert hash(clsdup) == hash(cls)

    @given(cls=st_crystalclasses())
    def test_setattr(self, cls):
        with self.assertRaises(TypeError):
            cls.new_stuff = 42

    @given(cls=st_crystalclasses())
    def test_annotations(self, cls):
        for f in vars(cls):
            # making sure all existing class values are present in annotations
            if not f.startswith("__"):
                assert f in cls.__annotations__

    @given(cls=st_crystalclasses())
    def test_repr(self, cls):
        assert cls.__module__ in repr(cls)
        assert cls.__qualname__ in repr(cls)
        # making sure all annotations are displayed in repr (we aim to enforce types)
        for f, t in cls.__annotations__.items():
            assert f"{f}: {t}" in repr(cls)


if __name__ == "__main__":
    unittest.main()
