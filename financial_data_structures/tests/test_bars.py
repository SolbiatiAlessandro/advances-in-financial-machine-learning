import pytest
from bars import TickBars
import pandas as pd

def test_tickbars():
    tick_data = pd.read_csv("./data/ES_Trades.csv")
    tick_batch_size = 2000
    extraction_columns = ['Price']
    tick_bars = TickBars(
            extraction_columns = extraction_columns ,
            tick_batch_size = tick_batch_size
            )
    bars = tick_bars.bars(tick_data)
    assert bars
    assert not bars[extraction_columns[0]].empty
    O = bars[extraction_columns[0]]['Open']
    assert not O.empty
    assert not bars[extraction_columns[0]]['Close'].empty
    assert not bars[extraction_columns[0]]['High'].empty
    assert not bars[extraction_columns[0]]['Low'].empty
    assert ((len(O) - 1) * tick_batch_size <\
            len(tick_data) < len(O) * tick_batch_size)
