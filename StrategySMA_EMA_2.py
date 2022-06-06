import backtrader as bt
from collections import defaultdict  # для списков в словарях
import functions
import talib as ta
import numpy as np


class TestStrategy01(bt.Strategy):
    """
    - Отображает статус подключения
    - При приходе нового бара отображает его цены/объем
    - Отображает статус перехода к новым барам
    """
    params = (  # Параметры торговой системы
        ('name', ''),  # Название торговой системы
        ('symbols', ''),  # Список торгуемых тикеров. По умолчанию торгуем все тикеры
        ('Percent', 20),
        ('lots', ''),
    )

    def __init__(self):
        """Инициализация торговой системы"""
        self.isLive = False  # Сначала будут приходить исторические данные

        # To keep track of pending orders
        self.order = None
        self.orders = defaultdict(list)

        self.dataclose = None

        self.orders_bar_executed = defaultdict(list)

        print(self.p.lots)

        self.sma_all1 = defaultdict(list)
        self.sma_all2 = defaultdict(list)

        for i in range(len(self.datas)):
            ticker = list(self.dnames.keys())[i]    # key name is ticker name
            self.sma_all1[ticker] = bt.indicators.SMA(self.datas[i], period=50)
            self.sma_all2[ticker] = bt.indicators.SMA(self.datas[i], period=100)


        # self.sma1 = bt.indicators.SMA(self.data, period=50)
        # self.sma2 = bt.indicators.SMA(self.data, period=100)
        #
        # self.sma3 = bt.indicators.SMA(self.data1, period=50)
        # self.sma4 = bt.indicators.SMA(self.data1, period=100)


    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(
            self.datas[0].datetime[0]) if dt is None else dt  # Заданная дата или дата последнего бара первого тикера ТС
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def next(self):
        """
        Приход нового бара тикера
        """
        if self.p.name != '':  # Если указали название торговой системы, то будем ждать прихода всех баров
            lastdatetimes = [bt.num2date(data.datetime[0]) for data in self.datas]  # Дата и время последнего бара каждого тикера
            if lastdatetimes.count(lastdatetimes[0]) != len(lastdatetimes):  # Если дата и время последних баров не идентичны
                return  # то еще не пришли все новые бары. Ждем дальше, выходим
            #print(self.p.name)

        for data in self.datas:  # Пробегаемся по всем запрошенным тикерам
            # print('\n', data._dataname, " \n", sep=" ")
            if self.p.symbols == '' or data._dataname in self.p.symbols:  # Если торгуем все тикеры или данный тикер
                self.log(f'{data._dataname} - {bt.TimeFrame.Names[data.p.timeframe]} {data.p.compression} - Open={data.open[0]:.2f}, High={data.high[0]:.2f}, Low={data.low[0]:.2f}, Close={data.close[0]:.2f}, Volume={data.volume[0]:.0f}',
                     bt.num2date(data.datetime[0]))
                # print("[", data._dataname, self.sma1[0], self.sma2[0], "]")
                print("[", data._dataname, self.sma_all1[data._dataname][0], self.sma_all2[data._dataname][0], "]")



                # https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
                # pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
                _ticker = data._dataname
                _current_close = data.close[0]
                _idx = data.line.idx
                _dd = data.close.array
                _kk = np.array(_dd)
                # print(_dd, _kk)
                _sma1 = ta.SMA(_kk, timeperiod=50); _sma2 = ta.SMA(_kk, timeperiod=100)
                print("[", data._dataname, _sma1[_idx], _sma2[_idx], "]")


                # print("close: ", data._dataname, data.close[0])

                # self.dataclose = data.close
                #
                # # Check if an order is pending ... if yes, we cannot send a 2nd one
                # if self.orders[data._dataname]:
                #     return
                #
                # print(self.data._dataname, "##", self.sma1[0], self.sma2[0])

                # Check if we are in the market
                # if not self.position:

                self.dataclose = data.close

                # if not self.orders[data._dataname]:
                #     if self.sma1[0] > self.sma2[0]:
                #         print(data._dataname, "***", self.sma1[0], self.sma2[0])
                #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
                #         self.buy(data=data, exectype=bt.Order.Market)  # , size=size)
                #         self.orders[data._dataname] = True
                #
                # if self.orders[data._dataname]:
                #     if self.sma1[0] < self.sma2[0]:
                #         self.log('SELL CREATE, %.2f' % self.dataclose[0])
                #         self.sell(data=data, exectype=bt.Order.Market)  # , size=size)
                #         self.orders[data._dataname] = False



    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)
            self.orders_bar_executed[order.data._name] = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_data(self, data, status, *args, **kwargs):
        """Изменение статсуса приходящих баров"""
        dataStatus = data._getstatusname(status)  # Получаем статус (только при LiveBars=True)
        print(f'{data._dataname} - {dataStatus}')  # Статус приходит для каждого тикера отдельно
        self.isLive = dataStatus == 'LIVE'  # В Live режим переходим после перехода первого тикера
