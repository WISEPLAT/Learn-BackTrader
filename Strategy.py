import backtrader as bt
from collections import defaultdict  # для списков в словарях
import functions


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

        self.dataclose = None

        self.orders_bar_executed = defaultdict(list)

        print(self.p.lots)

        sma1 = bt.indicators.SMA(self.data)
        ema1 = bt.indicators.EMA(self.data)

        close_over_sma = self.data.close > sma1
        close_over_ema = self.data.close > ema1
        sma_ema_diff = sma1 - ema1

        self.buy_sig = bt.And(close_over_sma, close_over_ema, sma_ema_diff > 0)


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
            if self.p.symbols == '' or data._dataname in self.p.symbols:  # Если торгуем все тикеры или данный тикер
                self.log(f'{data._dataname} - {bt.TimeFrame.Names[data.p.timeframe]} {data.p.compression} - Open={data.open[0]:.2f}, High={data.high[0]:.2f}, Low={data.low[0]:.2f}, Close={data.close[0]:.2f}, Volume={data.volume[0]:.0f}',
                     bt.num2date(data.datetime[0]))
                print("close: ", data.close[0])

                self.dataclose = data.close

                # Check if an order is pending ... if yes, we cannot send a 2nd one
                if self.order:
                    return

                # Check if we are in the market
                if not self.position:

                    print(self.buy_sig)

                    if self.buy_sig:
                        self.buy()

                    # # Not yet ... we MIGHT BUY if ...
                    # if self.dataclose[0] < self.dataclose[-1]:
                    #     # current close less than previous close
                    #
                    #     if self.dataclose[-1] < self.dataclose[-2]:
                    #         # previous close less than the previous close
                    #
                    #         # size, lots_can_buy = functions.calc_size(depo=self.cerebro.broker.get_cash(),
                    #         #                                          lot=self.p.lots[self.data._name],
                    #         #                                          percent=self.p.Percent,
                    #         #                                          ticker_price=self.dataclose[0])
                    #         # print(size, lots_can_buy)
                    #
                    #         # BUY, BUY, BUY!!! (with default parameters)
                    #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    #
                    #         # Keep track of the created order to avoid a 2nd order
                    #         self.order = self.buy(data=data) #, size=size)

                else:

                    # Already in the market ... we might sell
                    print(len(self), self.orders_bar_executed[data._name], data._name, self.orders_bar_executed)
                    try:
                        if len(self) >= (self.orders_bar_executed[data._name] + 5):
                            # SELL, SELL, SELL!!! (with all possible default parameters)
                            self.log('SELL CREATE, %.2f' % self.dataclose[0])

                            # Keep track of the created order to avoid a 2nd order
                            self.order = self.sell(data=data)
                    except:
                        pass

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
