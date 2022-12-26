import backtrader as bt
from collections import defaultdict  # для списков в словарях
import functions
import talib as ta
import numpy as np
import random


class TestStrategy04(bt.Strategy):
    """
    - Отображает статус подключения
    - При приходе нового бара отображает его цены/объем
    - Отображает статус перехода к новым барам
    """
    params = (  # Параметры торговой системы
        ('name', ''),  # Название торговой системы
        ('symbols', ''),  # Список торгуемых тикеров. По умолчанию торгуем все тикеры
        ('Percent', 20),
        ('lots', ''),   # лоты
        # ('my_log', ''),  # лог
    )

    def __init__(self):
        """Инициализация торговой системы"""
        self.isLive = False  # Сначала будут приходить исторические данные

        # To keep track of pending orders
        self.order = None
        self.orders = defaultdict(list)

        self.dataclose = None

        print(self.p.lots)

        self.sma_all1 = defaultdict(list)
        self.sma_all2 = defaultdict(list)
        self.macd = defaultdict(list)
        self.bbands = defaultdict(list)
        #self.crossover = defaultdict(list)
        self.crossover_80 = defaultdict(list)
        self.crossover_20 = defaultdict(list)
        self.crossover_sma = defaultdict(list)
        self.stoch = defaultdict(list)
        self.stoch2 = defaultdict(list)

        self.fibo_pivpoint = defaultdict(list)

        self.price_buy = defaultdict(list)
        self.size_buy = defaultdict(list)

        self.first_buy = defaultdict(list)

        self.my_logs = []

        for i in range(len(self.datas)):
            if self.datas[i].resampling == 0:
                ticker = f"{self.datas[i].classCode}.{self.datas[i].secCode}"
                if ticker in self.dnames.keys():
                    print(ticker)
                    self.sma_all1[ticker] = bt.indicators.SMA(self.datas[i], period=8)
                    self.sma_all2[ticker] = bt.indicators.SMA(self.datas[i], period=32)
            if self.datas[i].resampling == 1:
                self.fibo_pivpoint[ticker] = bt.indicators.FibonacciPivotPoint(self.datas[i])


        # for i in range(len(self.datas)):
        #     ticker = list(self.dnames.keys())[i]    # key name is ticker name
        #     self.sma_all1[ticker] = bt.indicators.SMA(self.datas[i], period=8)
        #     self.sma_all2[ticker] = bt.indicators.SMA(self.datas[i], period=32)
        #     #self.crossover_sma[ticker] = bt.ind.CrossOver(self.sma_all1[ticker], self.sma_all2[ticker])
        #     self.fibo_pivpoint[ticker] = bt.indicators.FibonacciPivotPoint(self.datas[i])
        #     #self.stoch[ticker] = bt.indicators.StochasticFull(self.datas[i], period=21, period_dfast=7, period_dslow=17)
        #     #self.crossover_80[ticker] = bt.ind.CrossOver(self.stoch[ticker].lines.percD, 80)
        #     #self.crossover_20[ticker] = bt.ind.CrossOver(self.stoch[ticker].lines.percD, 20)
        #     #self.macd[ticker] = bt.indicators.MACD(self.datas[i], period_me1=8, period_me2=16, period_signal=9)
        #     #self.bbands[ticker] = bt.indicators.BollingerBands(self.datas[i], period=20)

    def log(self, txt, dt=None):
        """Вывод строки с датой на консоль"""
        dt = bt.num2date(
            self.datas[0].datetime[0]) if dt is None else dt  # Заданная дата или дата последнего бара первого тикера ТС
        print(f'{dt.strftime("%d.%m.%Y %H:%M")}, {txt}')  # Выводим дату и время с заданным текстом на консоль

    def log_csv(self, ticker=None, signal=None, signal_price=None, order=None, order_price=None,
                    size=None, status=None, cost=None, comm=None, amount=None, pnl=None, dt=None):
        """Собираем логи для csv файла"""

        tradedate = bt.num2date(self.datas[0].datetime[0]) if dt is None else dt  # Заданная дата или дата последнего бара первого тикера ТС
        depo = f"{self.cerebro.broker.get_cash():.2f}"
        amount = f"{(self.cerebro.broker.get_value()):.2f}"  # - (self.cerebro.broker.get_cash()):.2f}"
        strategy_name = self.p.name
        info = ""
        if order == "BUY" and float(cost) < 0: info = "Warning"

        self.my_logs.append([tradedate, ticker, signal, signal_price, order, order_price, size, status,
                               cost, comm, pnl, amount, depo, strategy_name, info])

    def next(self):
        """
        Приход нового бара тикера
        """
        # if self.p.name != '':  # Если указали название торговой системы, то будем ждать прихода всех баров
        #     lastdatetimes = [bt.num2date(data.datetime[0]) for data in self.datas]  # Дата и время последнего бара каждого тикера
        #     if lastdatetimes.count(lastdatetimes[0]) != len(lastdatetimes):  # Если дата и время последних баров не идентичны
        #         return  # то еще не пришли все новые бары. Ждем дальше, выходим
        #     #print(self.p.name)

        #for data in self.datas:  # Пробегаемся по всем запрошенным тикерам
        for i in range(len(self.datas)):
            if self.datas[i].resampling == 0:           # не пробегаемся по клону данных
                data = self.datas[i]
                ticker = data._dataname

                if self.p.symbols == '' or ticker in self.p.symbols:  # Если торгуем все тикеры или данный тикер
                    self.log(f'{ticker} - {bt.TimeFrame.Names[data.p.timeframe]} {data.p.compression} - Open={data.open[0]:.2f}, High={data.high[0]:.2f}, Low={data.low[0]:.2f}, Close={data.close[0]:.2f}, Volume={data.volume[0]:.0f}',
                         bt.num2date(data.datetime[0]))

                    _close = data.close[0]  # текущий close
                    _low = data.low[0]  # текущий low
                    _high = data.high[0]  # текущий high
                    _open = data.open[0]
                    _oc2 = (_open + _close) / 2
                    _volume = data.volume  # ссылка на Объемы # print(volume[0])

                    self.r1, self.r2, self.r3 = self.fibo_pivpoint[ticker].lines.r1[0], self.fibo_pivpoint[ticker].lines.r2[0], self.fibo_pivpoint[ticker].lines.r3[0]
                    self.s1, self.s2, self.s3 = self.fibo_pivpoint[ticker].lines.s1[0], self.fibo_pivpoint[ticker].lines.s2[0], self.fibo_pivpoint[ticker].lines.s3[0]
                    print("self.r1, self.r2, self.r3: ", self.r1, self.r2, self.r3)
                    print("self.s1, self.s2, self.s3: ", self.s1, self.s2, self.s3)

                    # # https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
                    # # pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
                    # _ticker = ticker
                    # _current_close = data.close[0]
                    # _idx = data.line.idx
                    # _dd = data.close.array
                    # _kk = np.array(_dd)
                    # # print(_dd, _kk)
                    # _sma1 = ta.SMA(_kk, timeperiod=50); _sma2 = ta.SMA(_kk, timeperiod=100)
                    # print("[", ticker, _sma1[_idx], _sma2[_idx], "]")



                    # # условие на покупку
                    # if not self.orders[ticker]:
                    #     if self.crossover_sma[ticker]:       # снизу вверх пересекаем 20
                    #         lot = self.p.lots[ticker]
                    #         percent = 3    # сколько % от депозита использовать на сделку
                    #         depo = self.cerebro.broker.get_cash()
                    #         ticker_price = _close
                    #
                    #         size = functions.calc_size(depo=depo, lot=lot, percent=percent, ticker_price=ticker_price)
                    #
                    #         self.log(f"BUY CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.log_csv(ticker=ticker, signal='BUY', signal_price=_close, size=size)
                    #
                    #         if type(self.first_buy[ticker]) == list:
                    #             self.first_buy[ticker] = True
                    #
                    #         self.buy(data=data, exectype=bt.Order.Market, size=size)
                    #         # if not self.first_buy[ticker]:
                    #         #     self.buy(data=data, exectype=bt.Order.Market, size=size)
                    #
                    #         self.first_buy[ticker] = False
                    #
                    #         self.orders[ticker] = True
                    #
                    #
                    # profit_percent = 1
                    # ratio_profit = 5        # 1/3 => 1%*3=3%
                    # stop_loss_percent = 1
                    # # условие на продажу
                    # if self.orders[ticker] and self.price_buy[ticker]:
                    #     # print(f"_close={_close} self.price_buy[ticker]={self.price_buy[ticker]} take_profit={self.price_buy[ticker]*(1+profit_percent*ratio_profit/100)} stop-loss={self.price_buy[ticker]*(1-profit_percent/100)}")
                    #     size = self.size_buy[ticker]
                    #     # # условие на продажу stop-loss %
                    #     # if _close <= self.price_buy[ticker] * (1 - stop_loss_percent / 100):
                    #     #     self.log(f"SELL STOP LOSS CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #     #     self.log_csv(ticker=ticker, signal='STOP LOSS', signal_price=_close, size=size)
                    #     #     self.sell(data=data, exectype=bt.Order.Market, size=size)
                    #     #     self.orders[ticker] = False
                    #     #     self.first_buy[ticker] = True
                    #
                    #     # условие на продажу take-profit
                    #     if self.crossover_sma[ticker] == -1:       # сверху вниз пересекаем 80
                    #         self.log(f"SELL CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.log_csv(ticker=ticker, signal='SELL', signal_price=_close, size=size)
                    #
                    #         self.sell(data=data, exectype=bt.Order.Market, size=size)
                    #         # self.sell(data=data, exectype=bt.Order.Market, size=size)
                    #
                    #         self.orders[ticker] = False
                    #     # if _close>=self.price_buy[ticker]*(1+profit_percent*ratio_profit/100):
                    #     #     self.log(f"SELL TAKE PROFIT CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #     #     self.sell(data=data, exectype=bt.Order.Market, size=size)
                    #     #     self.orders[ticker] = False

                    # ==========================================================================================================================

                    # # условие на покупку
                    # if not self.orders[ticker]:
                    #     if self.sma_all1[ticker] > self.sma_all2[ticker]:
                    #         #print(self.bbands[ticker].lines.top, self.bbands[ticker].lines.mid, self.bbands[ticker].lines.bot)
                    #         self.log(f"BUY CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.buy(data=data, exectype=bt.Order.Market)  # , size=size)
                    #         self.orders[ticker] = True
                    #
                    # # условие на продажу
                    # if self.orders[ticker]:
                    #     if self.sma_all1[ticker] < self.sma_all2[ticker]:
                    #         self.log(f"SELL CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.sell(data=data, exectype=bt.Order.Market)  # , size=size)
                    #         self.orders[ticker] = False


                    # # ==========================================================================================================================
                    # # условие на покупку
                    # if not self.orders[ticker]:
                    #     if self.sma_all1[ticker] > self.sma_all2[ticker]:
                    #         #print(self.bbands[ticker].lines.top, self.bbands[ticker].lines.mid, self.bbands[ticker].lines.bot)
                    #
                    #         lot = self.p.lots[ticker]
                    #         percent = 3    # сколько % от депозита использовать на сделку
                    #         depo = self.cerebro.broker.get_cash()
                    #         ticker_price = _close
                    #
                    #         size = functions.calc_size(depo=depo, lot=lot, percent=percent, ticker_price=ticker_price)
                    #
                    #         self.log(f"BUY CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.log_csv(ticker=ticker, signal='BUY', signal_price=_close, size=size)
                    #         self.buy(data=data, exectype=bt.Order.Market, size=size)
                    #         self.orders[ticker] = True
                    #
                    # profit_percent = 1
                    # ratio_profit = 5        # 1/3 => 1%*3=3%
                    # stop_loss_percent = 1
                    # # условие на продажу
                    # if self.orders[ticker] and self.price_buy[ticker]:
                    #     # print(f"_close={_close} self.price_buy[ticker]={self.price_buy[ticker]} take_profit={self.price_buy[ticker]*(1+profit_percent*ratio_profit/100)} stop-loss={self.price_buy[ticker]*(1-profit_percent/100)}")
                    #     size = self.size_buy[ticker]
                    #     # условие на продажу stop-loss %
                    #     if _close <= self.price_buy[ticker] * (1 - stop_loss_percent / 100):
                    #         self.log(f"SELL STOP LOSS CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.log_csv(ticker=ticker, signal='STOP LOSS', signal_price=_close, size=size)
                    #         self.sell(data=data, exectype=bt.Order.Market, size=size)
                    #         self.orders[ticker] = False
                    #     # условие на продажу take-profit
                    #     elif self.sma_all1[ticker] < self.sma_all2[ticker]:
                    #         self.log(f"SELL CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.log_csv(ticker=ticker, signal='SELL', signal_price=_close, size=size)
                    #         self.sell(data=data, exectype=bt.Order.Market, size=size)
                    #         self.orders[ticker] = False
                    #     # if _close>=self.price_buy[ticker]*(1+profit_percent*ratio_profit/100):
                    #     #     self.log(f"SELL TAKE PROFIT CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #     #     self.sell(data=data, exectype=bt.Order.Market, size=size)
                    #     #     self.orders[ticker] = False
                    #
                    # # ==========================================================================================================================

                    # if not self.orders[ticker]:
                    #     if self.sma_all1[ticker] > self.sma_all2[ticker]:
                    #         #print(self.bbands[ticker].lines.top, self.bbands[ticker].lines.mid, self.bbands[ticker].lines.bot)
                    #         self.log(f"BUY CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.buy(data=data, exectype=bt.Order.Market)  # , size=size)
                    #         self.orders[ticker] = True

                    # if not self.orders[ticker]:
                    #     if random.randint(0, 10) > 8:
                    #         #print(self.bbands[ticker].lines.top, self.bbands[ticker].lines.mid, self.bbands[ticker].lines.bot)
                    #         self.log(f"BUY CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.buy(data=data, exectype=bt.Order.Market)  # , size=size)
                    #         self.orders[ticker] = True

                    #
                    # if self.orders[ticker]:
                    #     if _close < self.bbands[ticker].lines.mid:
                    #         self.log(f"SELL CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.sell(data=data, exectype=bt.Order.Market)  # , size=size)
                    #         self.orders[ticker] = False

                    # if not self.orders[ticker]:
                    #     if self.sma_all1[ticker] > self.sma_all2[ticker]:
                    #         #print(self.bbands[ticker].lines.top, self.bbands[ticker].lines.mid, self.bbands[ticker].lines.bot)
                    #         self.log(f"BUY CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.buy(data=data, exectype=bt.Order.Market)  # , size=size)
                    #         self.orders[ticker] = True
                    #
                    # if self.orders[ticker]:
                    #     if self.sma_all1[ticker] < self.sma_all2[ticker]:
                    #         self.log(f"SELL CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #         self.sell(data=data, exectype=bt.Order.Market)  # , size=size)
                    #         self.orders[ticker] = False

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def notify_order(self, order):

        ticker = order.data._name
        size = order.size

        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED [{order.data._name}], {order.executed.price:.2f} size={size}")
                self.log_csv(ticker=ticker, order='BUY', order_price=order.executed.price, size=size,
                             status=order.getstatusname(order.status), cost=f"{order.executed.value:.2f}",
                             comm=f"{order.executed.comm:.2f}")
                self.price_buy[ticker] = order.executed.price       # записываем цену покупки для тикера
                self.size_buy[ticker] = size                        # записываем объем покупки для тикера
            elif order.issell():
                self.log(f"SELL EXECUTED [{order.data._name}], {order.executed.price:.2f} size={size}")
                self.log_csv(ticker=ticker, order='SELL', order_price=order.executed.price, size=size,
                             status=order.getstatusname(order.status),
                             cost=f"{order.executed.value + order.executed.pnl:.2f}",
                             comm=f"{order.executed.comm:.2f}", pnl=f"{order.executed.pnl:.2f}")
                self.price_buy.pop(ticker, None)                    # удаляем цену покупки для тикера
                self.size_buy.pop(ticker, None)                     # удаляем объем покупки для тикера

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_data(self, data, status, *args, **kwargs):
        """Изменение статсуса приходящих баров"""
        dataStatus = data._getstatusname(status)  # Получаем статус (только при LiveBars=True)
        print(f'{data._dataname} - {dataStatus}')  # Статус приходит для каждого тикера отдельно
        self.isLive = dataStatus == 'LIVE'  # В Live режим переходим после перехода первого тикера
