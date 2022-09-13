import backtrader as bt
from collections import defaultdict  # для списков в словарях
import functions
import talib as ta
import numpy as np
import random


class NtimestrueOk(bt.Indicator):
    lines = ('ntimestrue',)
    params = dict(period=10)
    plotinfo = dict(plot=True, subplot=True, plotname='Ntimestrue', )

    def __init__(self):
        self.l.ntimestrue = bt.indicators.AllN(self.data1, period=self.p.period)


class Ntimestrue(bt.Indicator):
    lines = ('ntimestrue',)
    params = dict(period=10)
    plotinfo = dict(plot=True, subplot=True, plotname='Ntimestrue', )

    def __init__(self):
        #self.l.ntimestrue = bt.indicators.AllN(self.data, period=self.p.period)
        pass

    def next(self):
        print("hi", self.data[0], self.data1[0])   # -200 => 1

        if self.data1[0]:
            self.l.ntimestrue[0] = 1.0
        else:
            self.l.ntimestrue[0] = 0.0

        #self.l.ntimestrue[0] = random.randint(0, 1)


class And3(bt.Indicator):
    lines = ('and3',)
    params = dict(data2=1, data3=1)
    plotinfo = dict(plot=True)

    def __init__(self):
        self.l.and3 = bt.And(self.data, self.p.data2, self.p.data3)
        #self.l.and3 = bt.And(bt.And(self.data, self.p.data2), self.p.data3)


class OverUnder(bt.Indicator):
    lines = ('overunder',)
    params = dict(data2=20)
    plotinfo = dict(plot=True)

    def __init__(self):
        self.l.overunder = self.data > self.p.data2             # данные над data2 == 1


class UnderOver(bt.Indicator):
    lines = ('underover',)
    params = dict(data2=20)
    plotinfo = dict(plot=True)

    def __init__(self):
        self.l.underover = self.data < self.p.data2             # данные под data2 == 1


class UpDownTrend(bt.Indicator):
    lines = ('trend',)
    params = dict(period=20, )
    plotinfo = dict(plot=True)

    def __init__(self):
        y1 = self.data
        y2 = self.data(-self.p.period)
        #self.l.trend = cond = bt.Cmp(y1, y2)  # => 1 если y1 > y2       => 0 если y1 == y2      => -1 иначе
        self.l.trend = cond = y1 > y2  # => 1 если y1 > y2


class KC(bt.Indicator):
    lines = ('mid', 'top', 'bot',)
    params = dict(multiplier=2.0, period=20, movav=bt.indicators.MovAv.EMA, atr=bt.indicators.AverageTrueRange, )

    plotinfo = dict(subplot=False)
    plotlines = dict(
        mid=dict(ls='--'),
        top=dict(_samecolor=False),
        bot=dict(_samecolor=False),
    )

    def __init__(self):
        self.lines.mid = ma = self.p.movav(self.data, period=self.p.period)
        atr = self.p.atr(self.data, period=self.p.period)

        stddev = self.p.multiplier * atr
        self.lines.top = ma + stddev
        self.lines.bot = ma - stddev


class OverUnderMovAv(bt.Indicator):
    lines = ('overunder',)
    params = dict(period=20, movav=bt.indicators.MovAv.EMA)

    def __init__(self):
        movav = self.p.movav(self.data, period=self.p.period)
        self.l.overunder = bt.Cmp(self.data, movav)             # данные над sma => 1


class OverUnderMovAvMovAv(bt.Indicator):
    lines = ('overunder',)
    params = dict(period=20, period2=25, movav=bt.indicators.MovAv.EMA)

    def __init__(self):
        movav = self.p.movav(self.data, period=self.p.period)
        movav2 = self.p.movav(self.data, period=self.p.period2)
        self.l.overunder = bt.Cmp(movav, movav2)             # => 1 если EMA > EMA2


class Condition1(bt.Indicator):
    lines = ('overunder',)
    params = dict(period=20, period2=25, movav=bt.indicators.MovAv.EMA)

    def __init__(self):
        movav = self.p.movav(self.data, period=self.p.period)
        movav2 = self.p.movav(self.data, period=self.p.period2)
        cond1 = bt.Cmp(self.data, movav)    # данные над sma => 1
        cond2 = bt.Cmp(movav, movav2)       # => 1 если EMA > EMA2
        self.l.overunder = ((cond2 == 1) == cond1)             # => 1 если cond2 == cond1 == 1


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

        self.ema_all1 = defaultdict(list)
        self.ema_all2 = defaultdict(list)
        self.close_under_ema_all1 = defaultdict(list)
        self.ema_all1_over_ema_all2 = defaultdict(list)

        self.cond1 = defaultdict(list)
        self.test1 = defaultdict(list)

        self.macd = defaultdict(list)
        self.bbands = defaultdict(list)

        self.close_over_middle = defaultdict(list)

        self.crossover = defaultdict(list)

        self.crossover_80 = defaultdict(list)
        self.crossover_20 = defaultdict(list)
        self.crossover_DK = defaultdict(list)
        self.stoch = defaultdict(list)

        self.price_buy = defaultdict(list)
        self.size_buy = defaultdict(list)

        self.first_buy = defaultdict(list)

        self.my_logs = []

        self.ema_all1 = defaultdict(list)
        self.ema_all2 = defaultdict(list)
        self.close_under_ema_all10 = defaultdict(list)

        self.roc = defaultdict(list)
        self.kc = defaultdict(list)
        self.trend = defaultdict(list)
        self.roc_over_0 = defaultdict(list)
        self.close_over_kc_top = defaultdict(list)
        self.and3 = defaultdict(list)

        self.enter_long = defaultdict(list)
        self.close_long = defaultdict(list)

        for i in range(len(self.datas)):
            ticker = list(self.dnames.keys())[i]    # key name is ticker name

            self.ema_all1[ticker] = bt.indicators.ExponentialMovingAverage(self.datas[i], period=8)
            # self.ema_all2[ticker] = bt.indicators.ExponentialMovingAverage(self.datas[i], period=16)

            # self.close_under_ema_all10[ticker] = OverUnder(self.ema_all1[ticker].lines.ema, data2=self.ema_all2[ticker].lines.ema)

            self.roc[ticker] = bt.indicators.RateOfChange100(self.datas[i], period=100)

            self.kc[ticker] = KC(self.datas[i], period=200, multiplier=3.0)

            self.trend[ticker] = UpDownTrend(self.kc[ticker].lines.top, period=20)

            self.roc_over_0[ticker] = OverUnder(self.roc[ticker].lines.roc100, data2=0.0)

            self.close_over_kc_top[ticker] = OverUnder(self.datas[i].close, data2=self.kc[ticker].lines.top)

            self.and3[ticker] = And3(self.trend[ticker].lines.trend,
                                           data2=self.roc_over_0[ticker].lines.overunder,
                                           data3=self.close_over_kc_top[ticker].lines.overunder)

            self.enter_long[ticker] = NtimestrueOk(self.datas[i], self.and3[ticker].lines.and3, period=10)
            # self.enter_long[ticker] = bt.indicators.CrossUp(self.ema_all1[ticker].lines.ema,
            #                                                   self.kc[ticker].lines.bot)

            #self.close_long[ticker] = UnderOver(self.datas[i].close, data2=self.kc[ticker].lines.bot)
            self.close_long[ticker] = UnderOver(self.ema_all1[ticker].lines.ema, data2=self.kc[ticker].lines.mid)
            # self.close_long[ticker] = bt.indicators.CrossDown(self.ema_all1[ticker].lines.ema,
            #                                                   self.kc[ticker].lines.top)

            # self.sma_all1[ticker] = bt.indicators.SMA(self.datas[i], period=64)
            # self.sma_all2[ticker] = bt.indicators.SMA(self.datas[i], period=128)

            # self.ema_all1[ticker] = bt.indicators.ExponentialMovingAverage(self.datas[i], period=11)
            # self.ema_all2[ticker] = bt.indicators.ExponentialMovingAverage(self.datas[i], period=30)
            # #self.close_under_ema_all1[ticker] = bt.ind.Cmp(self.ema_all1[ticker], self.datas[i].close)
            # self.close_under_ema_all1[ticker] = OverUnderMovAv(self.datas[i].close, period=21)
            #
            # self.ema_all1_over_ema_all2[ticker] = OverUnderMovAvMovAv(self.datas[i].close, period=11, period2=30)
            #
            # self.cond1[ticker] = Condition1(self.datas[i].close, period=21, period2=30)
            #
            # # self.test1[ticker] = ((self.ema_all1_over_ema_all2[ticker] == 1) == self.close_under_ema_all1[ticker])
            #
            # self.stoch[ticker] = bt.indicators.Stochastic(self.datas[i], period=21, period_dfast=7, period_dslow=7)
            # self.crossover_80[ticker] = bt.ind.CrossOver(self.stoch[ticker].lines.percD, 80)
            # self.crossover_20[ticker] = bt.ind.CrossOver(self.stoch[ticker].lines.percD, 20)
            # self.crossover_DK[ticker] = bt.ind.CrossOver(self.stoch[ticker].lines.percD, self.stoch[ticker].lines.percK)
            #

            # self.macd[ticker] = bt.indicators.MACD(self.datas[i], period_me1=8, period_me2=16, period_signal=9)

            # self.bbands[ticker] = bt.indicators.BollingerBands(self.datas[i], period=20)
            # self.close_over_middle[ticker] = OverUnder(self.datas[i].close, data2=self.bbands[ticker].lines.mid)

            # self.crossover[ticker] = bt.ind.CrossOver(self.ema_all1[ticker], self.ema_all2[ticker])

            # #self.crossover[ticker] = bt.ind.UpDayBool(self.sma_all1[ticker], self.sma_all2[ticker])

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
        if self.p.name != '':  # Если указали название торговой системы, то будем ждать прихода всех баров
            lastdatetimes = [bt.num2date(data.datetime[0]) for data in self.datas]  # Дата и время последнего бара каждого тикера
            if lastdatetimes.count(lastdatetimes[0]) != len(lastdatetimes):  # Если дата и время последних баров не идентичны
                return  # то еще не пришли все новые бары. Ждем дальше, выходим
            #print(self.p.name)

        for data in self.datas:  # Пробегаемся по всем запрошенным тикерам
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

                #print(bool(self.trend[ticker]), bool(self.close_over_kc_top[ticker]), bool(self.roc_over_0[ticker]), bool(self.and3[ticker]))
                print(bool(self.enter_long[ticker]))


                #print(bool(self.cond1[ticker]), bool(self.test1[ticker]), self.cond1[ticker] == self.test1[ticker])
                #if self.cond1[ticker] != self.test1[ticker]: print("ERROR***")


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



                # условие на покупку
                if not self.orders[ticker]:
                    if self.enter_long[ticker]:       #
                        lot = self.p.lots[ticker]
                        percent = 3    # сколько % от депозита использовать на сделку
                        depo = self.cerebro.broker.get_cash()
                        ticker_price = _close

                        size = functions.calc_size(depo=depo, lot=lot, percent=percent, ticker_price=ticker_price)

                        self.log(f"BUY CREATE [{ticker}] {self.data.close[0]:.2f}")
                        self.log_csv(ticker=ticker, signal='BUY', signal_price=_close, size=size)

                        if type(self.first_buy[ticker]) == list:
                            self.first_buy[ticker] = True

                        self.buy(data=data, exectype=bt.Order.Market, size=size)
                        # if not self.first_buy[ticker]:
                        #     self.buy(data=data, exectype=bt.Order.Market, size=size)

                        self.first_buy[ticker] = False

                        self.orders[ticker] = True


                profit_percent = 1
                ratio_profit = 5        # 1/3 => 1%*3=3%
                stop_loss_percent = 5
                # условие на продажу
                if self.orders[ticker] and self.price_buy[ticker]:
                    # print(f"_close={_close} self.price_buy[ticker]={self.price_buy[ticker]} take_profit={self.price_buy[ticker]*(1+profit_percent*ratio_profit/100)} stop-loss={self.price_buy[ticker]*(1-profit_percent/100)}")
                    size = self.size_buy[ticker]
                    # условие на продажу stop-loss %
                    if _close <= self.price_buy[ticker] * (1 - stop_loss_percent / 100):
                        self.log(f"SELL STOP LOSS CREATE [{ticker}] {self.data.close[0]:.2f}")
                        self.log_csv(ticker=ticker, signal='STOP LOSS', signal_price=_close, size=size)
                        self.sell(data=data, exectype=bt.Order.Market, size=size)
                        self.orders[ticker] = False
                        self.first_buy[ticker] = True

                    # условие на продажу take-profit
                    if self.close_long[ticker] and self.orders[ticker]:       #
                        self.log(f"SELL CREATE [{ticker}] {self.data.close[0]:.2f}")
                        self.log_csv(ticker=ticker, signal='SELL', signal_price=_close, size=size)

                        self.sell(data=data, exectype=bt.Order.Market, size=size)
                        #self.sell(data=data, exectype=bt.Order.Market, size=size)

                        self.orders[ticker] = False
                    # if _close>=self.price_buy[ticker]*(1+profit_percent*ratio_profit/100):
                    #     self.log(f"SELL TAKE PROFIT CREATE [{ticker}] {self.data.close[0]:.2f}")
                    #     self.sell(data=data, exectype=bt.Order.Market, size=size)
                    #     self.orders[ticker] = False

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
