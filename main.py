# pip install backtrader pandas
# https://finance.yahoo.com/quote/GAZP.ME/history?p=GAZP.ME

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import pandas as pd
import datetime  # For datetime objects
# import os.path  # To manage paths
# import sys  # To find out the script name (in argv[0])


# Create a Strategy
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])


if __name__ == '__main__':

    data = pd.read_csv('GAZP_D1.csv', sep=',', index_col='Date')    # this data is from metatrader 5
    print(data)
    data = data.reset_index()
    data.rename(columns={'Date': 'datetime', 'Open': 'open', 'High': 'high',
                           'Low': 'low', 'Close': 'close', 'Volume': 'volume'},
                  inplace=True)  # Чтобы получить дату/время переименовываем колонки
    data.index = pd.to_datetime(data['datetime'])
    print(data)

    # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, 'GAZP.ME (1).csv')

    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    cerebro.broker.setcash(100000.0)

    # Create a Data Feed
    # data = bt.feeds.YahooFinanceCSVData(
    #     dataname='GAZP.ME (1).csv', # yahoo data downloaded from site
    #     # Do not pass values before this date
    #     fromdate=datetime.datetime(2022, 1, 1),
    #     # Do not pass values after this date
    #     todate=datetime.datetime(2022, 4, 1),
    #     reverse=False)

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.PandasData(dataname=data)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())