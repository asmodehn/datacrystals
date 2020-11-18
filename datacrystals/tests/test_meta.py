import unittest

import hypothesis.strategies as st
from hypothesis import Verbosity, given, settings

from .._meta import CrystalMeta


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
            keys=st.text(),
            values=st.one_of(  # default values
                st.integers(),
                st.floats(),
                st.decimals(),
                st.text(),
                # etc. TODO support more...
            ),
        )
    )

    return CrystalMeta(draw(names), (), attrs)


class TestMeta(unittest.TestCase):
    @given(cls=st_crystalclasses())
    @settings(verbosity=Verbosity.verbose)
    def test_strategy(self, cls):

        assert isinstance(cls, CrystalMeta)
        assert type(cls) == CrystalMeta

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
