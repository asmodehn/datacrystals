import datacrystals
from datacrystals._crystals import ShardType


@datacrystals.crystalize
class Candle:
    """
    OHLC as a datacrystal example.
    OHLC as a concept, is a directed container, and therefore a good candidate for a datacrystal example.
    """

    open: int
    high: int
    low: int
    close: int


# TRY 1 : define OHLC from Candle as Inner Type
OHLC = datacrystals.collection(Candle)


# TODO : this should be specified when constructing the collection type...
def as_candle(self):
    return Candle(
        open=self._df.iloc[0].open,
        high=max(self._df.high),
        low=min(self._df.low),
        close=self._df.iloc[-1].close,
    )


setattr(OHLC, "as_candle", as_candle)

c1 = Candle(open=1, high=4, low=1, close=3)
c2 = Candle(open=3, high=5, low=2, close=2)
ohlc = OHLC(c1, c2)


# TRY 2 : define collection from parameters passed
import pydantic


@classmethod
@pydantic.validate_arguments
def mycollection(cls, *elems: ShardType) -> datacrystals.Collection[ShardType]:

    # create the collection as usual (cf original `set()`) to get smthg working...
    Collec = datacrystals.collection(cls)

    return Collec(*elems)


if __name__ == "__main__":
    # interactive example
    import sys

    from ptpython.repl import embed

    sys.exit(embed(globals(), locals()))
