import unittest
from dataclasses import fields

import hypothesis.strategies as st
from hypothesis import Verbosity, given, settings

# strategy to build dataclasses dynamically
from hypothesis.strategies import SearchStrategy

from datacrystals._collection import _collection_from_class
from datacrystals.tests.test_shards import shard, st_dynclasses


@st.composite
def st_collec(draw, max_size=5):

    # TODO : collection with datacrystal(type(...)) or with proper Metaclass ???
    # pick a type
    dcls = shard(type(*draw(st_dynclasses())))

    # get the matching collection type
    Collec = _collection_from_class(dcls)

    # create the collection type
    return Collec


class TestCollection(unittest.TestCase):

    # Same behavior as crystals
    @given(collec=st_collec(), data=st.data())
    # @settings(verbosity=Verbosity.verbose)
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

        # TODO :  fix this, some problems with strings (unicode, symbols and stuff...)
        # check all fields of all rows are shown
        # for r in dcinst:  # for each row
        #     for f in fields(r):
        #         assert str(getattr(r, f.name)) in dcstr, f"{getattr(r, f.name)} not in {dcstr}"

    @given(collec=st_collec(), data=st.data())
    def test_dir(self, collec, data):
        dcinst = data.draw(collec.strategy())

        inner_fields = {f.name for f in fields(dcinst.Inner)}
        expected = {"Inner", "strategy", "optimize", *inner_fields}

        dcdir = dir(dcinst)

        assert set(dcdir).issuperset(expected), expected.difference(set(dcdir))

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


if __name__ == "__main__":
    unittest.main()
