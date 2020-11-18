import unittest
from dataclasses import asdict, fields
from typing import Any, Dict, List, Set, Tuple

import hypothesis.strategies as st
from hypothesis import Verbosity, assume, given, settings

# strategy to build dataclasses dynamically
from datacrystals._crystals import datacrystal


@st.composite
def st_dynclasses(
    draw,
    names=st.text(
        alphabet=st.characters(whitelist_categories=["Lu", "Ll"], max_codepoint=128),
        min_size=1,
        max_size=5,
    ),
    identifiers=st.lists(
        st.text(
            alphabet=st.characters(
                whitelist_categories=["Lu", "Ll"], max_codepoint=128
            ),
            min_size=1,
        ),
        min_size=5,
    ),
):  # TODO : text strategy for legal python identifier ??

    idtfrs = draw(identifiers)
    # No keyword in identifiers !
    for kw in ["if", "or", "as", "in", "is"]:
        assume(kw not in idtfrs)

    attrs = draw(
        st.dictionaries(
            keys=st.sampled_from(idtfrs),
            values=st.one_of(  # default values
                st.integers(),
                st.floats(),
                st.decimals(allow_nan=False, allow_infinity=False),
                st.text(),
                # etc. TODO support more...
            ),
        )
    )

    annots = draw(
        st.dictionaries(
            keys=st.sampled_from(idtfrs),
            values=st.sampled_from(  # annotations
                [
                    int,
                    float,
                    str,
                    Set,
                    List,
                    Dict,
                ]  # Tuple annoys pydantic currently (1.7.2 : cf https://github.com/samuelcolvin/pydantic/issues/2132)
                # etc. TODO support more... function type ??
            ),
        )
    )

    # reorder to put defaults at the end of the (ordered) dict
    attrs["__annotations__"] = {
        a: v for a, v in annots.items() if a not in attrs.keys()
    }
    attrs["__annotations__"].update(
        {a: v for a, v in annots.items() if a in attrs.keys()}
    )

    # returning tuple to use as argument of dynamic class constructor : type() or whatever your metaclass is.
    return "DynClass" + draw(names), (), attrs


class TestDataCrystal(unittest.TestCase):
    @given(dynclass=st_dynclasses(), data=st.data())
    # @settings(verbosity=Verbosity.verbose)
    def test_strategy(self, dynclass, data):
        dcls = datacrystal(type(*dynclass))
        # validating strategy
        dcinst = data.draw(dcls.strategy())

        assert isinstance(dcinst, dcls)
        assert type(dcinst) == dcls

    @given(dynclass=st_dynclasses(), data=st.data())
    def test_str(self, dynclass, data):
        dcls = datacrystal(type(*dynclass))
        # generating an instance of dcls
        dcinst = data.draw(dcls.strategy())

        dcstr = str(dcinst)

        assert type(dcinst).__name__ in dcstr

        for f in fields(dcinst):
            assert f"{f.name}: {getattr(dcinst, f.name)}" in dcstr

    @given(dynclass=st_dynclasses(), data=st.data())
    def test_dir(self, dynclass, data):
        dcls = datacrystal(type(*dynclass))
        # generating an instance of dcls
        dcinst = data.draw(dcls.strategy())

        expected = {f.name for f in fields(dcinst)}

        dcdir = dir(dcinst)

        assert {a for a in dcdir}.issuperset(expected), expected.difference(
            {a for a in dcdir}
        )

        # check no extra information is exposed
        assert {a for a in dcdir if not a.startswith("__")}.issubset(expected), {
            a for a in dcdir if not a.startswith("__")
        }.difference(expected)

    @given(dynclass=st_dynclasses(), data=st.data())
    def test_eq(self, dynclass, data):

        dclsA = datacrystal(type(*dynclass))
        # generating an instance of dcls
        dcA1inst = data.draw(dclsA.strategy())
        dcA2inst = data.draw(dclsA.strategy())

        a1f = asdict(dcA1inst)
        a2f = asdict(dcA2inst)

        # two instances of the same type are equal
        if dcA1inst == dcA2inst:
            # iff their dict is also equal
            assert a1f == a2f, f"{a1f} != {a2f}"
        else:
            assert a1f != a2f, f"{a1f} == {a2f}"

    @given(dynclassA=st_dynclasses(), dynclassB=st_dynclasses(), data=st.data())
    def test_neq(self, dynclassA, dynclassB, data):
        dclsA = datacrystal(type(*dynclassA))
        dclsB = datacrystal(type(*dynclassB))
        # generating an instance of dcls
        dcA1inst = data.draw(dclsA.strategy())
        dcB1inst = data.draw(dclsB.strategy())

        a1f = asdict(dcA1inst)
        b1f = asdict(dcB1inst)

        # two instances of different type are different
        assert dcA1inst != dcB1inst
        # BUT that says nothing on their dict.


if __name__ == "__main__":
    unittest.main()
