import datacrystals


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

ohlc = OHLC(
    Candle(open=1, high=4, low=1, close=3), Candle(open=3, high=5, low=2, close=2)
)

if __name__ == "__main__":
    # interactive example
    import sys

    from ptpython.repl import embed

    sys.exit(embed(globals(), locals()))
