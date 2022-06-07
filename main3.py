from datetime import datetime
from backtrader import Cerebro, TimeFrame
from BackTraderQuik.QKStore import QKStore  # Хранилище QUIK

import backtrader as bt


class SMAStrategy(bt.Strategy):
    params = (
        ('period', 10),
        ('onlydaily', False),
    )

    def __init__(self):
        self.sma_small_tf = bt.indicators.SMA(self.data, period=self.p.period)
        if not self.p.onlydaily:
            self.sma_large_tf = bt.indicators.SMA(self.data1, period=self.p.period)

    def nextstart(self):
        print('nextstart called with len', len(self))
        for data in self.datas:
            ticker = data._dataname
            self.log(f'{ticker} - {bt.TimeFrame.Names[data.p.timeframe]} {data.p.compression} - Open={data.open[0]:.2f}, High={data.high[0]:.2f}, Low={data.low[0]:.2f}, Close={data.close[0]:.2f}, Volume={data.volume[0]:.0f}',
                bt.num2date(data.datetime[0]))

        super(SMAStrategy, self).nextstart()

    def next(self):
        print('next called with len', len(self))
        for data in self.datas:
            ticker = data._dataname
            self.log(f'{ticker} - {bt.TimeFrame.Names[data.p.timeframe]} {data.p.compression} - Open={data.open[0]:.2f}, High={data.high[0]:.2f}, Low={data.low[0]:.2f}, Close={data.close[0]:.2f}, Volume={data.volume[0]:.0f}',
                bt.num2date(data.datetime[0]))

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(
            self.datas[0].datetime[0]) if dt is None else dt  # Заданная дата или дата последнего бара первого тикера ТС
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    cerebro = Cerebro()  # Инициируем "движок" BackTrader

    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.01)

    tframes = dict(daily=bt.TimeFrame.Days, weekly=bt.TimeFrame.Weeks, monthly=bt.TimeFrame.Months)

    symbols = ('TQBR.AFKS', 'TQBR.SBER', )  # Кортеж тикеров 'TQBR.GAZP', 'TQBR.GMKN', 'TQBR.LKOH',
    store = QKStore()  # Хранилище QUIK (QUIK на локальном компьютере)
    # store = QKStore(Host='<Ваш IP адрес>')  # Хранилище QUIK (К QUIK на удаленном компьютере обращаемся по IP или названию)
    for symbol in symbols:  # Пробегаемся по всем тикерам
        data = store.getdata(dataname=symbol, timeframe=TimeFrame.Minutes, compression=60, fromdate=datetime(2000, 1, 1),
                             LiveBars=False)  # Исторические и новые бары по первому тикеру
        cerebro.adddata(data)  # Добавляем данные

        data2 = store.getdata(dataname=symbol, timeframe=TimeFrame.Days, compression=1, fromdate=datetime(2000, 1, 1),
                             LiveBars=False)  # Исторические и новые бары по первому тикеру
        cerebro.adddata(data2)  # Добавляем данные

        # cerebro.resampledata(data, timeframe=tframes['daily'], compression=1)

    # cerebro.addstrategy(ts.TestStrategy01, name="One Ticker", symbols=('TQBR.SBER',))  # Добавляем торговую систему по одному тикеру
    # cerebro.addstrategy(ts.TestStrategy01, name="Two Tickers", symbols=('TQBR.GAZP', 'TQBR.LKOH',))  # Добавляем торговую систему по двум тикерам
    # cerebro.addstrategy(ts.TestStrategy01, name="All Tickers")  # Добавляем торговую систему по всем тикерам

    cerebro.addstrategy(SMAStrategy, period=50, onlydaily=False)  # Добавляем торговую систему по всем тикерам

    cerebro.run()  # Запуск торговой системы

    print('Стоимость портфеля: %.2f' % cerebro.broker.getvalue())
    print('Свободные средства: %.2f' % cerebro.broker.get_cash())

    cerebro.plot(style='candle')  # Рисуем график. Требуется matplotlib версии 3.2.2 (pip install matplotlib==3.2.2)
