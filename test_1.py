import pandas as pd
import datetime
import webbrowser
import backtrader as bt
import quantstats as qs
import yfinance as yf

class SmaCross(bt.SignalStrategy):
    params = dict(
    pfast=50, # период быстрой средней, 50 свечей
    pslow=200 # 200 свечей для медленной средней
    )

    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=self.p.pfast), bt.ind.SMA(period=self.p.pslow) # используем простые скользящие средние
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:  # если позиция не открыта системой
            if self.crossover > 0:  # если быстрая SMA пересекает медленную вверх
                self.buy()  # открываем длинную позицию

            elif self.crossover < 0:  # во всех остальных случаях закрываем открытую позицию
                self.close()

# data = bt.feeds.PandasData(dataname=yf.download('MSFT', '2007-02-02', '2021-09-01', auto_adjust=True)) # в качестве примера берём MSFT, 2008 год тоже торгуем

data = pd.read_csv("csv\\TQBR.GAZP_D1.csv", sep=',') #, index_col='datetime')
# data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M')
print(data)
print(data.dtypes)

# data = data.reset_index()
# print(data)
data.rename(columns={'datetime': 'Date', 'open': 'Open', 'high': 'High',
                       'low': 'Low', 'close': 'Close', 'volume': 'Volume'},
              inplace=True)  # Чтобы получить дату/время переименовываем колонки

data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date')

# data.index = data['Date']
# data = data.drop('Date', 1)

# data = yf.download('MSFT', '2007-02-02', '2021-09-01', auto_adjust=True)

print(data)
print(data.dtypes)
print(data.index.dtype)

data = bt.feeds.PandasData(dataname=data) # в качестве примера берём MSFT, 2008 год тоже торгуем

cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000) # начальный депозит 10 000 денег
cerebro.addsizer(bt.sizers.FixedSize, stake=10) # размер позиции 10 лотов
cerebro.adddata(data)
cerebro.addstrategy(SmaCross)
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio') # PyFolio, но quantstats его тоже отрендерит
results = cerebro.run()

#cerebro.plot()

strat = results[0]
portfolio_stats = strat.analyzers.getbyname('PyFolio')
returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
returns.index = returns.index.tz_convert(None)

print(returns)

qs.reports.html(returns, 'GAZP.ME', output='stats.html', title='SMA Cross') # формируем репорт в quantstats, вместо бенчмарка SPY используем buy&hold MSFT
# webbrowser.open('quantstats-tearsheet.html') # рендерим репорт в html и открываем в новой вкладке