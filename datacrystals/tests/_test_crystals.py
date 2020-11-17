import unittest
from dataclasses import asdict, fields

import hypothesis.strategies as st
from hypothesis import Verbosity, given, settings

# strategy to build dataclasses dynamically
from datacrystals._crystals import datacrystal


@st.composite
def st_dcls(
    draw,
    names=st.text(
        alphabet=st.characters(whitelist_categories=["Lu", "Ll"]),
        min_size=1,
        max_size=5,
    ),
):  # TODO : character strategy for legal python identifier ??

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

    dcls = datacrystal(type("DataCrystal_" + draw(names), (), attrs))

    return dcls


class TestDataCrystal(unittest.TestCase):
    @given(dcls=st_dcls(), data=st.data())
    @settings(verbosity=Verbosity.verbose)
    def test_strategy(self, dcls, data):
        # validating strategy
        dcinst = data.draw(dcls.strategy())

        assert isinstance(dcinst, dcls)
        assert type(dcinst) == dcls

    @given(dcls=st_dcls(), data=st.data())
    def test_str(self, dcls, data):
        # generating an instance of dcls
        dcinst = data.draw(dcls.strategy())

        dcstr = str(dcinst)

        assert type(dcinst).__name__ in dcstr

        for f in fields(dcinst):
            assert f"{f.name}: {getattr(dcinst, 'f.name')}" in dcstr

    @given(dcls=st_dcls(), data=st.data())
    def test_dir(self, dcls, data):
        # generating an instance of dcls
        dcinst = data.draw(dcls.strategy())

        expected = {f for f in fields(dcinst)}

        dcdir = dir(dcinst)

        assert {a for a in dcdir}.issuperset(expected), expected.difference(
            {a for a in dcdir}
        )

        # check no extra information is exposed
        assert {a for a in dcdir if not a.startswith("__")}.issubset(expected), {
            a for a in dcdir if not a.startswith("__")
        }.difference(expected)

    @given(dclsA=st_dcls(), dclsB=st_dcls(), data=st.data())
    def test_eq(self, dclsA, dclsB, data):

        # generating an instance of dcls
        dcA1inst = data.draw(dclsA.strategy())
        dcA2inst = data.draw(dclsA.strategy())

        a1f = asdict(dcA1inst)
        a2f = asdict(dcA2inst)
        assert (dcA1inst == dcA2inst) == (a1f == a2f)

        dcB1inst = dclsB(**{f: v for f, v in a1f.items() if f in fields(dclsB)})
        # always different, even if values are same (types are not) !
        assert dcA1inst != dcB1inst


if __name__ == "__main__":
    unittest.main()
