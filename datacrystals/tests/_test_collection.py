import unittest
from dataclasses import fields

import hypothesis.strategies as st
from hypothesis import Verbosity, given, settings

# strategy to build dataclasses dynamically
from hypothesis.strategies import SearchStrategy

from datacrystals._collection import _collection_from_class
from datacrystals.tests._test_crystals import st_dcls


@st.composite
def st_collec(draw, elems_type: SearchStrategy=st_dcls(), max_size=5):

    # pick a type
    dcls = draw(elems_type)

    # get the matching collection type
    Collec = _collection_from_class(dcls)

    # create the collection type
    return Collec


class TestCollection(unittest.TestCase):

    # Same behavior as crystals
    @given(collec=st_collec(), data=st.data())
    @settings(verbosity=Verbosity.verbose)
    def test_strategy(self, collec, data):
        # validating strategy
        cinst = data.draw(collec.strategy())

        assert isinstance(cinst, collec)
        assert type(cinst) == collec

    @given(collec=st_collec(), data=st.data())
    def test_str(self, collec, data):
        # generating an instance of dcls
        dcinst = data.draw(collec.strategy())

        dcstr = str(dcinst)

        assert type(dcinst).__name__ in dcstr

        # check all headers are there
        for f in fields(dcinst.Inner):
            assert f"{f.name}" in dcstr

        # check all fields of all rows are shown
        for r in dcinst:  # for each row
            for f in fields(r):
                assert f"{getattr(r, f'{f.name}')}" in dcstr

    @given(collec=st_collec(), data=st.data())
    def test_dir(self, collec, data):
        dcinst = data.draw(collec.strategy())

        inner_fields = {f for f in fields(dcinst.Inner)}
        expected = {'Inner', 'strategy', 'optimize', *inner_fields}

        dcdir = dir(dcinst)

        assert {a for a in dcdir}.issuperset(expected), expected.difference(
            {a for a in dcdir}
        )

        # check no extra information is exposed
        assert {a for a in dcdir if not a.startswith("__")}.issubset(expected), {
            a for a in dcdir if not a.startswith("__")
        }.difference(expected)


    # specific collection behavior

    @given(collec=st_collec(), data=st.data())
    def test_collection(self, collec, data):

        cinst = data.draw(collec.strategy())

        decount = len(cinst)  # __len__ test

        for e in cinst:  # __iter__ test
            assert e in cinst  # __contain__ test
            decount -= 1

        assert decount == 0

    @given(collec=st_collec(), data=st.data())
    def test_optimize(self, collec, data):

        cinst = data.draw(collec.strategy())

        copt = cinst.optimize()

        for f in fields(cinst.Inner):
            if f.type == "":
                assert ""

    # TODO : maybe separate it ? growable collection can be separated...
    # @given(collec=st_collec(), data=st.data())
    # def test_call(self, collec, data):
    #     raise NotImplementedError


if __name__ == '__main__':
    unittest.main()
