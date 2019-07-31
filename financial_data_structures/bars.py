"""this modules implement all the different financial data structures (bars) described in Chapter 2"""
from abc import ABC, abstractmethod
from overrides import overrides
from typing import List, TypeVar, Optional
import pandas as pd
import logging
ColumnNames = List[str]

class Bars(ABC):
    """
    Bars are a table (pd.DataFrame) representation of extracted tick data.
    (https://www.investopedia.com/terms/t/tick.asp)

    This is a abstract base class for Bars extraction, the specific 
    extractions (Tick Bars, Volume Bars, Dollar Bars) are
    in the relative final classes. 

    FUTURE: for future contracts Bars data need to be rolled over
    (Rollover is when a trader moves his position from the 
    front month contract to a another contract further in the future. )
    The rollover is done in the abstract class since is common for 
    any Bars extraction.
    """

    def __init__(
            self, 
            tick_data_format,
            extraction_columns
            ):
        """
        tick_data_format is used to use different
        data format compared to the one used in testing,
        if your dataset's price column is called 'MyPriceXYZ'
        you can put '_Price':'MyPriceXYZ'
        """
        super(Bars, self).__init__()
        self.format = tick_data_format
        self.extraction_columns = extraction_columns

    @abstractmethod
    def extract_bars(self, tick_data):
        pass

    def rollover(self, bars):
        """
        To deal with this contract roll we use the book propose to 
        **take a cumsum of all this rollover gaps and subtract 
        it from the price series.** (The book implementation though 
        is terrible) One other observation made in the book is 
        that rolled price can become negative. So instead of 
        dealing with rolled prices you can use a price series 
        of a $1 investment.
        """
        return bars

    def bars(self, tick_data):
        """
        returns bars
        """
        bars = self.extract_bars(tick_data[self.extraction_columns])
        bars = self.rollover(bars)
        return bars


class TickBars(Bars):
    """
    the sample variables will be extracted
    each time a pre-defined number of
    transactions takes place
    """

    def __init__(self,
            extraction_columns : ColumnNames,
            tick_batch_size : int = 1000,
            tick_data_format : dict ={
                '_Symbol':'Symbol', 
                '_Date':'Date',
                '_Time':'Time',
                '_Price':'Price', 
                '_Volume':'Volume', 
                },
            ): 
        self.tick_batch_size = tick_batch_size
        super(TickBars, self).__init__(
                tick_data_format,
                extraction_columns
                )

    @overrides
    def extract_bars(self, tick_data) -> dict: 
        """
        returns OCLH over the extraction columns

        self.extraction_columns = ['price','volume']
        return: {
        'price': pd.DataFrame('Open','Close','High','Low')
        'volume': pd.DataFrame('Open','Close','High','Low')
        }
        """
        extracted_bars_dict:dict = {}
        for column in tick_data.columns:
            logging.info("TickBars: extracting bars for extraction column = {}".format(column))
            extraction_group = tick_data[column].groupby(tick_data.index // self.tick_batch_size)
            extracted_bars = pd.DataFrame({
                'Open' : extraction_group.first(),
                'Close' : extraction_group.last(),
                'High' : extraction_group.max(),
                'Low' : extraction_group.min(),
                })
            extracted_bars_dict[column] = extracted_bars
        return extracted_bars_dict
